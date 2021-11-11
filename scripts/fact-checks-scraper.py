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

def scrape_fakehunter():
    driver = webdriver.Chrome('ext/chromedriver.exe')
    article_driver = webdriver.Chrome('ext/chromedriver.exe')


    driver.get('https://fakehunter.pap.pl/')
    # wait for site to load
    time.sleep(5)

    # for storing temp data later saved in dataframe
    data = []

    # checks if there is next page
    next_page_selector = "#__next  div > div > div.Container-sc-1gspdc4-0.cjdLzL > section > div.Pagination__PaginationWrapper-cr5t78-0.ephzDL > ul > li.next > a"   
    while driver.find_element_by_css_selector(next_page_selector).get_attribute('aria-disabled') == 'false':
        # wait for page to load
        time.sleep(5)
        
        # returns all links with articles
        for link in driver.find_elements_by_css_selector("a.ListItem__TitleLink-q70zzz-10"):
            print(link.get_attribute('href'))
            article_driver.get(link.get_attribute('href'))

            # wait for article to load
            time.sleep(3)
            
            temp_data = [link.get_attribute('href')]
            selectors = ["h1.id__DetailsTitle-sc-131d89h-1", ".Verdict__VerdictStatus-sc-18ha1uh-1 p", "p.Typography__Text-wn1ri9-3", "p.d__StyledDate-sc-131d89h-7"]
            for selector in selectors:
                try:
                    temp_data.append(article_driver.find_element_by_css_selector(selector).text)
                except:
                    temp_data.append('0')
            data.append(temp_data)

        print("Next page!")
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(next_page_selector))

    driver.quit()

    return pd.DataFrame(data, columns=['url','title', 'verdict', 'short_justification', 'date'])

def scrape_demagog():
    driver = webdriver.Chrome('ext/chromedriver.exe')
    article_driver = webdriver.Chrome('ext/chromedriver.exe')

    driver.get('https://demagog.org.pl/wypowiedzi/')
    # wait for site to load
    time.sleep(5)

    # for storing temp data later saved in dataframe
    data = []

    # checks if there is next page
    next_page_selector = "a.next"   
    while driver.find_element_by_css_selector(next_page_selector):
        #wait for page to load
        time.sleep(5)
        
        # returns all links with articles
        for link in driver.find_elements_by_css_selector("h2.title-archive a"):
            print(link.get_attribute('href'))
            article_driver.get(link.get_attribute('href'))

            # wait for article to load
            time.sleep(3)

            temp_data = [link.get_attribute('href')]
            selectors = ["blockquote.hyphenate", "p.ocena", "div.date-content a"]
            for selector in selectors:
                try:
                    temp_data.append(article_driver.find_element_by_css_selector(selector).text)
                except:
                    temp_data.append('0')
            data.append(temp_data)

        print("Next page!")
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(next_page_selector))
        
    driver.quit()
    return pd.DataFrame(data, columns=['url','statement', 'verdict', 'date'])

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
        next_page_selector = "li.next"   
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
        
    driver.quit()
    return pd.DataFrame(data, columns=['url', 'title', 'verdict', 'date'])

if __name__ == '__main__':
    demagog = scrape_demagog()
    demagog.to_csv('../database/fact-checks/demagog.org.pl/'+generate_timestamp()+'.csv')

    fakehunter = scrape_fakehunter()
    fakehunter.to_csv('../database/fact-checks/fakehunter.pap.pl/'+generate_timestamp()+'.csv')

    fakenews = scrape_fakenews()
    fakehunter.to_csv('../database/fact-checks/fakenews.pl/'+generate_timestamp()+'.csv')