from this import d
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd
from helper import generate_timestamp, check_driver

from demagog import  demagog
from fakehunter import fakehunter

if __name__ == '__main__':
    check_driver()

    # fakehunter = fakehunter()
    # fakehunter.to_csv('../../database/fact-checks/fakehunter.pap.pl/'+generate_timestamp()+'.csv')

    demagog_fakes = demagog("https://demagog.org.pl/fake_news/")
    demagog_fakes.to_csv('../../database/fact-checks/demagog.org.pl/'+generate_timestamp()+'.csv')

    # demagog_statements = demagog("https://demagog.org.pl/wypowiedzi/")
    # demagog_statements.to_csv('../../database/fact-checks/demagog.org.pl/'+generate_timestamp()+'.csv')
    


    