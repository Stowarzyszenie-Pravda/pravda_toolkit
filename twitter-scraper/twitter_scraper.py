import pandas as pd
import numpy as np
import twint

import random
import datetime

import concurrent.futures

def scrape_keyword(keyword, from_day):
    """
    Takes keyword and outputs dataframe of scraped tweets
    """
    c = twint.Config()
    c.Lang = "pl"
    c.Limit = 200000
    c.Search = keyword
    c.Count = True
    c.Hide_output = True
    c.Stats = True   
    c.Since = str((datetime.datetime.now() - datetime.timedelta(days=from_day)).date())
    if from_day >= 1:
        c.Until = str((datetime.datetime.now() - datetime.timedelta(days=from_day-1)).date())
    
    # Set to True to display full user information. By default, only usernames are shown.
    c.User_full = True
    c.Pandas = True

    try:
        twint.run.Search(c)
    except:
        return False
    return twint.storage.panda.Tweets_df

def scrape_keyword_weekly(keyword, folder_name):
    for i in range(1,8):
            print(f'Day -{i} for {keyword}')
            # Adds to previous dataframe
            if i == 1:
                df = scrape_keyword(keyword, i)
            else:
                try:
                    df = df.append(scrape_keyword(keyword, i), ignore_index=True,sort=False)
                except:     
                    continue

    try:
        # Deleting not polish tweets
        df = df[df['language'] == 'pl']
    except:
        pass

    # Deleting not important columns
    df = df.drop(columns=['created_at','timezone','place','language','cashtags', 'retweet', 'quote_url', 'thumbnail', 'video', 'day', 'hour', 'near', 'geo', 'source', 'user_rt_id',
                'user_rt', 'retweet_id','retweet_date','translate','trans_src','trans_dest', 'user_id'])

    # Delete duplicates
    df = df.drop_duplicates(subset = ['id'])

    save_results(df, folder_name)

def batch_run(keywords, folder_name):
    """
    Takes list of keywords and runs scrape_keyword() function on them. Outputs merged dataframe.
    """
    with concurrent.futures.ProcessPoolExecutor(8) as exe:
        exe.map(scrape_keyword_weekly, keywords, [folder_name]*len(keywords))


def save_results(df, folder_name):
    """
    Takes dataframe and saves it to csv file with generated timestamp.
    """
    df.to_csv("../data/twitter-scraped-data/"+folder_name+'/'+str(datetime.datetime.now().date())+"-"+str(random.randint(0,1000000))+".csv", encoding = "utf-8")

if __name__ == "__main__":
    # Antisemitism
    #batch_run(["Żyd", "Żydzi", "Żyda", "Żydów", "Żydowi", "Żydom", "Żyda", "Żydów", "Żydem", "Żydami", "Żydzie", "Żydach", "Żydzie", "Żydzi", "Żydostwo", "Żydki", "Żydek", "Holocaust", "Żydowskie", "Żydowski", "Żydokomuna", "Auschwitz", "holokaust", "holokaust", "holokaustu", "holokaustowi", "holokaust", "holokaustem", "holokauście", "holokauście"], 'antisemitism')

    # Vaccines
    #batch_run(["stopsegregacjisanitarnej","stopss","segregacja", "covid1984", "nwo", "szczepimysie","szczepimysię","nieszczepimysię","segregację", "segregacji", "segregacją", "segregacji", "nieszczepimysie", "śmiertelna substancja", "śmiertelnej substancji", "śmiertelnej substancji", "śmiertelną substancją", "nop", "stopnop", "stop nop", "norymberga20", "zajob",  "plandemia", "plandemii", "plandemie", "plandemią", "niezaszczepiony", "niezaszczepiona", "niezaszczepioni", "niezaszczepieni", "niezaszczepię", "niezaszczepią", "nie zaszczepię", "nie zaszczepiona", "nie zaszczepiony", "nie zaszczepią", "zaszczepię", "zaszczepieni", "zaszczepiona", "zaszczepiony", "zaszczepią", "nieszczepimy", "szczepię", "szczepią", "szczepiona", "szczepieni", "szczepiony", "szczepionki", "szczeczepionek", "szczepionkom", "szczepionkami", "szczepionkach", "szczepionka", "szczepionki", "szczepionce", "szczepionką", "paszport covidowy", "paszportu covidowego", "paszportowi covidowemu", "paszportem covidowym", "paszporcie covidowym", "paszporty covidowe", "paszportów covidowych", "paszportom covidowym", "paszportami covidowymi", "paszportach covidowych", "certyfikat covid", "certyfikatu covid", "certyfikatowi covidowemu", "certyfikatem covidowym", "certyfikacie covidowym", "certyfikaty covidowe", "certyfikatów covidowych", "certyfikatom covidowym", "certyfikatami covidowymi", "certyfikatach covidowych"], 'vaccines')

    # Bad Ukraine
    batch_run(["Ukry", "Banderowcy", "Banderowcom", "Banderowcach", "Banderowcami", "Banderowców", "Banderowiec", "Banderowca", "Banderowcowi", "Bandera", "Banderowcem", "Banderowcu", "Faszysci", "Faszystów", "Faszystom", "Faszystami", "Faszystach", "Faszysty", "Faszysta", "Faszysty", "Faszyście", "Faszystę", "Faszystą", "Faszysto", "Naziści", "Nazistów", "Nazistom", "Nazistami", "Nazistach", "Nazisty", "Nazista", "Nazisty", "Naziści", "Nazistę", "Nazistą", "Nazisto", "Naziście", "Wołyń", "Wołynia", "Wołyniowi", "Wołyniem", "Wołyniu", "Wołyńskie", "Wołyński", "Wołyńskiego", "Wołyńskiemu", "Wołyńskim", "UPA", "UPowcy", "UPowców", "UPowcami", "Upowcach", "Ludobójcy", "Ludobójcom", "Ludobójcami", "Ludobójcach", "Ludobójców", "Ludobójstwo", "Ludobójstwa", "Ludubójstwu", "Ludobójstwie", "Ludobójstwem", "OUN", "OUnowcy", "OUnowców", "OUNowcom", "OUnowcami"], 'bad-ukraine')
