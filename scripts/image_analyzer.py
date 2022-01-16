from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import re
import os

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from ext.image_copy_move_detection import detect


def clone_detection(image_path, block_size = 32):
    """
    Performs clone detection on given image (by filepath and block size).
    """
    folder_path = os.path.dirname(image_path)
    detect.detect(image_path, folder_path, block_size)

def ela(image_path, image_quality = 95):
    """
    Performs Error Level Analysis on given image (by filepath and quality).
    """
    folder_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)

    resaved_image_path = folder_path + '/resaved_' + image_name
    ela_image_path = folder_path + '/ela_' + image_name

    # Saving and resaving in different image_quality in order to see the difference in quality
    image = Image.open(image_path)
    image.save(fp = resaved_image_path, quality = image_quality)
    resaved_image = Image.open(resaved_image_path)

    # Calculates difference in quality
    ela_image = ImageChops.difference(image, resaved_image)
    extrema = ela_image.getextrema()
    max_difference = max([ex[1] for ex in extrema])
    scale = 255.0/max_difference

    # Creates new image black and white with brightness corresponding to difference to highlight changes 
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    print(f'Maximum difference was {max_difference}')

    ela_image.save(ela_image_path)

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
