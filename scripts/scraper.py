import pandas as pd
import numpy as np
import twint

import random
import datetime

def scrape_keyword(keyword):
    """
    Takes keyword and outputs dataframe of scraped tweets.
    """
    c = twint.Config()
    c.Lang = "pl"
    c.Limit = 5000
    c.Search = keyword
    c.Count = True
    c.Stats = True   
    c.Since = str((datetime.datetime.now() - datetime.timedelta(days=7)).date())
    c.Hide_output = True
    
    # Set to True to display full user information. By default, only usernames are shown.
    c.User_full = True
    c.Pandas = True

    try:
        twint.run.Search(c)
    except:
        return False
    return twint.storage.panda.Tweets_df

def scrape_user(username):

    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Hide_output = True

    try:
        twint.run.Lookup(c)
    except:
        return False
    return twint.storage.panda.User_df

def generate_timestamp():
    """
    Generates timestamp XXXX-XX-XX.
    """
    return str(datetime.datetime.now().date())

def batch_run(keywords):
    """
    Takes list of keywords and runs scrape_keyword() function on them. Outputs merged dataframe.
    """
    for e, keyword in enumerate(keywords):
        print(f"Scraping -> {keyword}")
        # Adds to previous dataframe
        if e == 0:
            df = scrape_keyword(keyword)
        else:
            df = df.append(scrape_keyword(keyword), ignore_index=True,sort=False)
    return df

def batch_run_user(users):
    """
    Takes list of users and runs scrape_user() function on them. Outputs merged dataframe.
    """
    for e, user in enumerate(users):
        print(f"Scraping -> {user}")
        # Adds to previous dataframe
        if e == 0:
            df = scrape_user(user)
        else:
            df = df.append(scrape_user(user), ignore_index=True,sort=False)
    return df

def save_results(df):
    """
    Takes dataframe and saves it to excel file with generated timestamp.
    """
    df.to_excel("database/"+generate_timestamp()+"-"+str(random.randint(0,10000))+".xlsx",engine='xlsxwriter', encoding = "utf-8")

if __name__ == "__main__":
    df = batch_run(["segregacja", "covid1984", "nwo", "szczepimysie","szczepimysię","nieszczepimysię","segregację", "segregacji", "segregacją", "segregacji", "nieszczepimysie", "śmiertelna substancja", "śmiertelnej substancji", "śmiertelnej substancji", "śmiertelną substancją", "nop", "stopnop", "stop nop", "norymberga20", "zajob",  "plandemia", "plandemii", "plandemie", "plandemią", "niezaszczepiony", "niezaszczepiona", "niezaszczepioni", "niezaszczepieni", "niezaszczepię", "niezaszczepią", "nie zaszczepię", "nie zaszczepiona", "nie zaszczepiony", "nie zaszczepią", "zaszczepię", "zaszczepieni", "zaszczepiona", "zaszczepiony", "zaszczepią", "nieszczepimy", "szczepię", "szczepią", "szczepiona", "szczepieni", "szczepiony", "szczepionki", "szczeczepionek", "szczepionkom", "szczepionkami", "szczepionkach", "szczepionka", "szczepionki", "szczepionce", "szczepionką", "paszport covidowy", "paszportu covidowego", "paszportowi covidowemu", "paszportem covidowym", "paszporcie covidowym", "paszporty covidowe", "paszportów covidowych", "paszportom covidowym", "paszportami covidowymi", "paszportach covidowych", "certyfikat covid", "certyfikatu covid", "certyfikatowi covidowemu", "certyfikatem covidowym", "certyfikacie covidowym", "certyfikaty covidowe", "certyfikatów covidowych", "certyfikatom covidowym", "certyfikatami covidowymi", "certyfikatach covidowych"])

    # Saves results to the file
    save_results(df)




