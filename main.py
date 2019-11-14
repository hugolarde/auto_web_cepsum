from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

username = config.username
password = config.password
sport = config.sport
number_partner = config.number_partner
date = config.date
time_min = config.time_min
time_max = config.time_max
time_preference = config.time_preference
start_program_time = config.start_program_time


def time_string_to_int(time_string):
    return int(time_string[:2]) + int(time_string[-2:])/60


def wait_reservation_avalable(browser):
    while len(browser.find_elements_by_class_name('important')) == 0:
        time.sleep(1)
    return


def wait_start_program_time():
    start_program = time_string_to_int(start_program_time)
    current_time_string_list = datetime.now().strftime("%H %M").split()
    current_time = int(current_time_string_list[0]) + int(current_time_string_list[1]) / 60
    while current_time < start_program:
        time.sleep(10)
        now = datetime.now()
        current_time = now.hour + now.minute/60 + now.second/3600
    return


time_range = [time_string_to_int(time_min), time_string_to_int(time_max)]

wait_start_program_time()

browser = webdriver.Firefox()

browser.get("https://interactif.cepsum.umontreal.ca/capnet/login.coba")
browser.find_element_by_xpath("//input[contains(@id,'_txtCodeUsager')]").send_keys(username)
browser.find_element_by_xpath("//input[contains(@id,'_txtMotDePasse')]").send_keys(password)
browser.find_element_by_xpath("//button[contains(@id, '_btnConnecter')]").click()

WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, 'lnkPRALIBRE'))).click()
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@id,'_grdReservations-ajouter')]"))).click()
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@id,'image07TENNIS')]"))).click()
# WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@id,'image02BAD')]"))).click()
date_field_value = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'txtDate')]"))).get_attribute('value')
while date_field_value != date:
    WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@id,'_btnDateSuiv')]"))).click()
    date_field_value = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'txtDate')]"))).get_attribute('value')
wait_reservation_avalable(browser)
plage_element_list = WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id,'_btnPlage')]")))
if time_preference == "desc":
    plage_element_list.reverse()
heure_debut_choisie = ''
heure_fin_choisie = ''
for plage_element in plage_element_list:
    text_list = plage_element.text.split()
    heure_debut = int(text_list[0][:2]) + int(text_list[0][-2:])/60
    heure_fin = int(text_list[2][:2]) + int(text_list[2][-2:])/60
    if heure_debut >= time_range[0] and heure_fin <= time_range[1]:
        plage_element.click()
        heure_debut_choisie = text_list[0]
        heure_fin_choisie = text_list[2]
        break
partner_select_element = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'_CTRL_CBOPARTENAIRE1')]")))
for option in partner_select_element.find_elements_by_tag_name('option'):
    if number_partner in option.get_attribute('value'):
        option.click()
        break
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'_btnConfirmer')]"))).click()
print("session reservee de " + heure_debut_choisie + " a " + heure_fin_choisie)
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'_btnFermer')]"))).click()
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@id,'lnkDecEnt')]"))).click()
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'popup-boutons')]"))).find_element_by_class_name('primaire').click()
browser.quit()
