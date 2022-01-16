import datetime
import random
from selenium import webdriver
import requests
import zipfile
import wget
import subprocess
import os

def generate_timestamp():
    """
    Generates timestamp XXXX-XX-XX.
    """
    return str(datetime.datetime.now().date())

def random_user_agent():
    """
    Returns random user agent from user-agents.txt
    """
    return random.choice(list(open('../../database/ext/user-agents.txt')))

CHROMEDRIVER_PATH =  '../ext/'
CHROMEDRIVER_FOLDER = os.path.dirname(CHROMEDRIVER_PATH)
LATEST_DRIVER_URL = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"

def download_latest_version(version_number):
    print("Attempting to download latest driver online......")
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    # Download zip file
    latest_driver_zip = wget.download(download_url, out=CHROMEDRIVER_FOLDER)
    # Read & extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
        # You can chose the folder path to extract to below:
        downloaded_zip.extractall(path=CHROMEDRIVER_FOLDER)
    # Delete the zip file downloaded above
    os.remove(latest_driver_zip)


def check_driver():
    # Run cmd line to check for existing web-driver version locally
    cmd_run = subprocess.run("chromedriver --version", capture_output=True, text=True, shell=True)
    # Extract driver version as string from terminal output

    # Check for latest chromedriver version online
    response = requests.get(LATEST_DRIVER_URL)
    online_driver_version = response.text
    try:
        local_driver_version = cmd_run.stdout.split()[1]
        print(f"Local driver version: {local_driver_version}")
        print(f"Latest online chromedriver version: {online_driver_version}")
        if local_driver_version == online_driver_version:
            return True
        else:
            download_latest_version(online_driver_version)
    except:
        download_latest_version(online_driver_version)