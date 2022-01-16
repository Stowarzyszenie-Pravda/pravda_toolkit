from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd
from helper import generate_timestamp

from demagog import  demagog

if __name__ == '__main__':
    demagog_fakes = demagog("https://demagog.org.pl/fake_news/")
    demagog_fakes.to_csv('../../database/fact-checks/demagog.org.pl/'+generate_timestamp()+'.csv')

    demagog_statements = demagog("https://demagog.org.pl/wypowiedzi/")
    demagog_statements.to_csv('../../database/fact-checks/demagog.org.pl/'+generate_timestamp()+'.csv')
    


    