from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re

def initialize_screenshooter():
    """
    Initializes screenshooter based on selenium webdriver. Returns selenium web driver.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    screenshooter =  webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    return screenshooter

def make_screenshoot(url, id, screenshooter):
    # URL validation
    # TODO explore other test cases of dealing with validation (goo.gl etc.)
    pattern = "((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
    if re.match(pattern, url) == False:
        return False

    # Goes to given URL
    screenshooter.get(url)
    time.sleep(2)

    # Sets up required height
    required_height = screenshooter.execute_script('return document.body.parentNode.scrollHeight')
    screenshooter.set_window_size(1920, required_height)
    time.sleep(5)

    # Timestamp generation
    file_name = str(id) + '.png'

    # Makes screenshot and saves it
    # TODO what if there is popup? How to solve this problem?
    screenshooter.find_element_by_tag_name('body').screenshot("../screenshots/" + file_name)

    # Quits driver
    screenshooter.quit()

if __name__ == '__main__':
    screenshooter = initialize_screenshooter()
    test_url = "https://www.wochenblick.at/nobelpreistraeger-warnt-in-jedem-land-folgt-die-todeskurve-der-impfkurve/?fbclid=IwAR1jLe_vJ6xXKBRXB7Apo49EAYZbO83a5HHeE-WHIgHT_aXd7G0XrDMohtA"
    test_id = 123113242
    make_screenshoot(test_url, test_id, screenshooter)
