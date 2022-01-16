from operator import index
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time

from helper import random_user_agent, check_driver

def click_allow_cookies(driver):
    try:
        allow_cookies_selector = "a#cn-accept-cookie"
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(allow_cookies_selector))
        time.sleep(5)
    except:
        pass

# Block date in format XX.XX.XXXX
def demagog(block_date, starting_page):
    opts = Options()
    opts.add_argument("user-agent="+random_user_agent())
    opts.add_argument("--headless")

    check_driver()
    driver = webdriver.Chrome('../ext/chromedriver.exe', options=opts)
    article_driver = webdriver.Chrome('../ext/chromedriver.exe', options=opts)

    # Get starting page
    driver.get(starting_page)

    # Wait for site to load
    time.sleep(10)

    # Click accepts cookies if exists
    click_allow_cookies(driver)

    # For storing temporary data later saved in dataframe
    data = []

    # Checks if there is next page
    next_page_selector = "a.next" 

    try:  
        while driver.find_element_by_css_selector(next_page_selector):
            # Wait for page to load
            time.sleep(5)
            
            # Returns all links with articles
            for link in driver.find_elements_by_css_selector("h2.title-archive a"):
                print(link.get_attribute('href'))

                # Get article page
                article_driver.get(link.get_attribute('href'))

                # Wait for article to load
                time.sleep(10)

                click_allow_cookies(article_driver)

                # Start temporary data list with 'Organization' and then 'URL'
                temp_data = ["Demagog", link.get_attribute('href')]

                # Selectors in order 'Statement', 'Statement author', 'Statement date', 'Verdict', 'Article body', 'Article publish date'
                selectors = ["blockquote.hyphenate p", "div.person-name a", "div.date-content a", "p.ocena", "div.content-editor", "p.date"]
                for selector in selectors:
                    try:
                        temp_data.append(article_driver.find_element_by_css_selector(selector).text.replace('\xad',''))
                    except:
                        temp_data.append('0')
            
                if time.strptime(temp_data[7].split(" ")[0], "%d.%m.%Y") > time.strptime(block_date, "%d.%m.%Y"):  
                    data.append(temp_data)
                else:
                    return pd.DataFrame(data, columns=['Organization','URL', 'Statement', 'Statement author', 'Statement date', 'Verdict', 'Article body', 'Article publish date'])


            print("Next page!")
            driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(next_page_selector))
    except:
        pass

    driver.quit()    

    return pd.DataFrame(data, columns=['Organization','URL', 'Statement', 'Statement author', 'Statement date', 'Verdict', 'Article body', 'Article publish date'])
