from datetime import datetime
import atexit
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.chrome.options import Options as chrome_options
import config


SPORTS = ["Badminton", "Raquetball", "Salles d'activites diverses", "Squash et spikeball", "Tennis", "Tennis de table", "Wallyball"]
SPORT_IMAGES_NAME = ["image02BAD", "image03RACQUET", "image04SALLES", "image06SQUASH", "image07TENNIS", "image08PINGPONG", "image09WALLY"]


def select_sport():
    for index in range(len(SPORTS)):
        print(str(index + 1) + " - " + SPORTS[index])
    index = -1
    while index not in range(len(SPORTS)):
        index = int(input("Select sport : ")) - 1
    print("Selected sport : " + SPORTS[index])
    return index


def time_string_to_int(time_string):
    return int(time_string[:time_string.find(':')]) + int(time_string[time_string.find(':')+1:])/60


def wait_start_program_time():
    if config.start_program_time.find(':') == -1:
        return
    start_program = time_string_to_int(config.start_program_time)
    now = datetime.now()
    current_time = now.hour + now.minute/60 + now.second/3600
    if current_time < start_program:
        print("It's " + now.strftime("%H:%M:%S") + ", program will start at " + config.start_program_time)
    while current_time < start_program:
        try:
            time.sleep(10)
            now = datetime.now()
            current_time = now.hour + now.minute/60 + now.second/3600
        except KeyboardInterrupt:
            exit(0)
    return


def quit_browser(browser):
    browser.quit()


def start_browser():
    if config.browser == 'firefox':
        options = firefox_options()
        options.headless = config.headless
        if config.system == "linux":
            browser = webdriver.Firefox(options=options, executable_path=r"./include/geckodriver")
        elif config.system == "windows":
            browser = webdriver.Firefox(options=options, executable_path=r".\include\geckodriver.exe")
    elif config.browser == 'chrome' :
        options = chrome_options()
        if config.headless : 
            options.add_argument('--headless')
        if config.system == "linux":
            browser = webdriver.Chrome(options=options, executable_path=r"./include/chromedriver")
        elif config.system == "windows":
            browser = webdriver.Chrome(options=options, executable_path=r".\include\chromedriver.exe")
    else:
        print("Error : wrong browser configured")
        exit(1)
    atexit.register(quit_browser, browser)
    return browser


def log_in(browser):
    browser.get("https://interactif.cepsum.umontreal.ca/capnet/login.coba")
    browser.find_element_by_xpath("//input[contains(@id,'_txtCodeUsager')]").send_keys(config.username)
    browser.find_element_by_xpath("//input[contains(@id,'_txtMotDePasse')]").send_keys(config.password)
    browser.find_element_by_xpath("//button[contains(@id, '_btnConnecter')]").click()


def wait_reservation_available(browser):
    while len(browser.find_elements_by_class_name('important')) != 0:
        try:
            time.sleep(1)
            WebDriverWait(browser, 1).until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinnercontainer")))
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id,'_btnDatePrec')]"))).click()
            WebDriverWait(browser, 1).until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinnercontainer")))
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id,'_btnDateSuiv')]"))).click()
        except KeyboardInterrupt:
            exit(0)
    return


def place_reservation(browser, sport_index):
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.ID, 'lnkPRALIBRE'))).click()
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id,'_grdReservations-ajouter')]"))).click()
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@id,'" + SPORT_IMAGES_NAME[sport_index] + "')]"))).click()
    date_field_value = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'txtDate')]"))).get_attribute('value')
    while date_field_value != config.date:
        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id,'_btnDateSuiv')]"))).click()
        new_date_field_value = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'txtDate')]"))).get_attribute('value')
        if new_date_field_value != date_field_value:
            date_field_value = new_date_field_value
        else:
            print("Error : unable to access selected date.")
            exit(1)
    wait_reservation_available(browser)
    plage_element_list = WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id,'_btnPlage')]")))
    if config.time_preference == "desc":
        plage_element_list.reverse()
    heure_debut_choisie = ''
    heure_fin_choisie = ''
    for element_index in range(len(plage_element_list)):
        text_list = plage_element_list[element_index].text.split()
        heure_debut = int(text_list[0][:2]) + int(text_list[0][-2:]) / 60
        heure_fin = int(text_list[2][:2]) + int(text_list[2][-2:]) / 60
        if heure_debut >= time_string_to_int(config.time_min) and heure_fin <= time_string_to_int(config.time_max):
            plage_element_list[element_index].click()
            if len(browser.find_elements_by_id('tmrTimeOutReservation')) == 0:
                if len(browser.find_elements_by_class_name('erreur')) != 0:
                    plage_element_list = WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id,'_btnPlage')]")))
                    continue
                else:
                    print("Error : time slot selection went wrong")
                    exit(1)
                    break
            else:
                heure_debut_choisie = text_list[0]
                heure_fin_choisie = text_list[2]
                break
    if heure_debut_choisie == '' or heure_fin_choisie == '':
        print("No time slot available")
        exit(0)
    partner_select_element = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'_CTRL_CBOPARTENAIRE1')]")))
    for option in partner_select_element.find_elements_by_tag_name('option'):
        if config.number_partner in option.get_attribute('value'):
            option.click()
            break
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'_btnConfirmer')]"))).click()
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'_btnFermer')]"))).click()
    print("session reservée de " + heure_debut_choisie + " à " + heure_fin_choisie)


def log_out(browser):
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id,'lnkDecEnt')]"))).click()
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id,'popup-boutons')]"))).find_element_by_class_name('primaire').click()


if __name__ == "__main__":
    sport_index = select_sport()
    wait_start_program_time()
    browser = start_browser()
    log_in(browser)
    place_reservation(browser, sport_index)
    log_out(browser)
    exit(0)
    