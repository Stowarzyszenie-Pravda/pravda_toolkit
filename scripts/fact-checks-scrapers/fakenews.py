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

def scrape_fakenews():
    driver = webdriver.Chrome('ext/chromedriver.exe')
    article_driver = webdriver.Chrome('ext/chromedriver.exe')

    # for storing temp data later saved in dataframe
    data = []

    sites = ["https://fakenews.pl/polityka/", "https://fakenews.pl/spoleczenstwo/", "https://fakenews.pl/technologia/", "https://fakenews.pl/zdrowie/"]
    for site in sites:
        driver.get(site)
        
        # wait for site to load
        time.sleep(5)
        
        # checks if there is next page
        next_page_selector = "li.next a"
        try:
            while driver.find_element_by_css_selector(next_page_selector):
                #wait for page to load
                time.sleep(5)
                
                # returns all links with articles
                for link in driver.find_elements_by_css_selector(".post-title h2 a"):
                    print(link.get_attribute('href'))
                    article_driver.get(link.get_attribute('href'))

                    # wait for article to load
                    time.sleep(3)

                    temp_data = [link.get_attribute('href')]
                    selectors = [".title-post h1", ".verdict-wrapper .content h2", "div.subheader li"]
                    for selector in selectors:
                        try:
                            temp_data.append(article_driver.find_element_by_css_selector(selector).text)
                        except:
                            temp_data.append('0')
                    data.append(temp_data)

                print("Next page!")
                driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(next_page_selector))
        except:
            continue

    driver.quit()
    return pd.DataFrame(data, columns=['url', 'title', 'verdict', 'date'])