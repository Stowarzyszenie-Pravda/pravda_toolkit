from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd

import time
import datetime

def generate_timestamp():
    """
    Generates timestamp XXXX-XX-XX.
    """
    return str(datetime.datetime.now().date())