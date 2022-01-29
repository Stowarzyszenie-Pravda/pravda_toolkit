from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time

from helper import random_user_agent

def fakehunter(starting_page = "https://fakehunter.pap.pl/", block_date = "01.01.1999"):
    opts = Options()
    opts.add_argument("user-agent="+random_user_agent())
    opts.add_argument("--headless")

    driver = webdriver.Chrome('../ext/chromedriver.exe', options=opts)
    article_driver = webdriver.Chrome('../ext/chromedriver.exe', options=opts)

    # Get starting page
    driver.get(starting_page)

    # Wait for site to load
    time.sleep(10)

    # For storing temporary data later saved in dataframe
    data = []

    # Checks if there is next page
    next_page_selector = "#__next  div > div > div.Container-sc-1gspdc4-0.cjdLzL > section > div.Pagination__PaginationWrapper-cr5t78-0.ephzDL > ul > li.next > a"   
    try:
        while driver.find_element_by_css_selector(next_page_selector).get_attribute('aria-disabled') == 'false':
            # Wait for page to load
            time.sleep(5)
            
            # Returns all links with articles
            for link in driver.find_elements_by_css_selector("a.ListItem__TitleLink-q70zzz-10"):
                print(link.get_attribute('href'))

                # Get article page
                article_driver.get(link.get_attribute('href'))

                # Wait for article to load
                time.sleep(10)
                
                # Start temporary data list with 'Organization' and then 'URL'
                temp_data = ["Fakehunter", link.get_attribute('href')]
                
                # Selectors in order 'Statement', 'Statement author', 'Statement date', 'Verdict', 'Article body', 'Article publish date'
                selectors = ["h1.id__DetailsTitle-sc-131d89h-1", ".Verdict__VerdictStatus-sc-18ha1uh-1 p", "p.Typography__Text-wn1ri9-3", "p.id__StyledDate-sc-131d89h-7"]
                for selector in selectors:
                    try:
                        temp_data.append(article_driver.find_element_by_css_selector(selector).text)
                    except:
                        temp_data.append('0')

                # Blocking scraping if before given block date
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
