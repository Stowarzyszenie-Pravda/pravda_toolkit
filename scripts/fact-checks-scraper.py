from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import random
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
    #wait for site to load
    time.sleep(5)

    data = []

    # checks if there is next page if there is
    next_page_selector = "#__next > div > div > div.Container-sc-1gspdc4-0.cjdLzL > section > div.Pagination__PaginationWrapper-cr5t78-0.ephzDL > ul > li.next > a"   
    while driver.find_element_by_css_selector(next_page_selector).get_attribute('aria-disabled') == 'false':
        #wait for page to load
        time.sleep(5)
        
        # returns all links with articles
        for link in driver.find_elements_by_css_selector("a.ListItem__TitleLink-q70zzz-10"):
            print(link.get_attribute('href'))
            article_driver.get(link.get_attribute('href'))

            #wait for article to load
            time.sleep(5)


            data.append([article_driver.find_element_by_css_selector("h1.id__DetailsTitle-sc-131d89h-1").text, article_driver.find_element_by_css_selector(".Verdict__VerdictStatus-sc-18ha1uh-1 p").text, article_driver.find_element_by_css_selector("p.Typography__Text-wn1ri9-3").text])

        print("Next page!")
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(next_page_selector))

    driver.quit()

    return pd.DataFrame(data, columns=['title', 'verdict', 'short_justification'])

if __name__ == '__main__':
    dataframe = scrape_fakehunter()
    dataframe.to_csv("out.csv", encoding='utf-8')