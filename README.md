# Usage
Allows one to place a reservation for a sport court automatically on CEPSUM website.

# Supported platforms
This programs works on Windows and Linux (not tested for MacOs) with Chrome and Firefox

# Set up project
1. [Optional]
    * Install python : recommended version 3.6
    * Install venv
        - (Linux & MacOS)
            ```shell script
            python3 -m pip install --user virtualenv
            ```
        - (Windows)
            ```shell script
            py -m pip install --user virtualenv
            ```
1. Create virtual environment 
    - (Linux & MacOS)
        ```shell script
        python3 -m venv venv        
        ```
    - (Windows)
        ```shell script
        py -m venv venv
        ```
1. Activate virtual environment
    - (Linux & MacOS)
        ```shell script
        source venv/bin/activate
        ```
    - (Windows)
        ```shell script
        .\venv\Scripts\activate
        ```
1. Install required packages
    ```shell script
    pip install -r requirements.txt
    ```
1. Browser :
    - Chrome : Download **chromedriver** from https://chromedriver.chromium.org/downloads and place it into */venv/include*
    - Firefox : Download **geckodriver** from https://github.com/mozilla/geckodriver/releases and place it into */venv/include*


# How to use
1. Edit *config_template.py* **and** rename it to *config.py*
1. run program 
    - (Linux & MacOS)
        ```shell script
        python3 -m main
        ```
    - (Windows)
        ```shell script
        py -m main
        ```
