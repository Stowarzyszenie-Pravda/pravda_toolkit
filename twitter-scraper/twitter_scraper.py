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
    for i in range(1,2):
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
    with concurrent.futures.ProcessPoolExecutor(4) as exe:
        exe.map(scrape_keyword_weekly, keywords, [folder_name]*len(keywords))


def save_results(df, folder_name):
    """
    Takes dataframe and saves it to csv file with generated timestamp.
    """
    df.to_csv("../data/twitter-scraped-data/"+folder_name+'/'+str(datetime.datetime.now().date())+"-"+str(random.randint(0,1000000))+".csv", encoding = "utf-8")

if __name__ == "__main__":
    #Antisemitism
    batch_run(["??yd", "??ydzi", "??yda", "??yd??w", "??ydowi", "??ydom", "??yda", "??yd??w", "??ydem", "??ydami", "??ydzie", "??ydach", "??ydzie", "??ydzi", "??ydostwo", "??ydki", "??ydek", "Holocaust", "??ydowskie", "??ydowski", "??ydokomuna", "Auschwitz", "holokaust", "holokaust", "holokaustu", "holokaustowi", "holokaust", "holokaustem", "holokau??cie", "holokau??cie"], 'antisemitism')

    #Vaccines
    batch_run(["stopsegregacjisanitarnej","stopss","segregacja", "covid1984", "nwo", "szczepimysie","szczepimysi??","nieszczepimysi??","segregacj??", "segregacji", "segregacj??", "segregacji", "nieszczepimysie", "??miertelna substancja", "??miertelnej substancji", "??miertelnej substancji", "??mierteln?? substancj??", "nop", "stopnop", "stop nop", "norymberga20", "zajob",  "plandemia", "plandemii", "plandemie", "plandemi??", "niezaszczepiony", "niezaszczepiona", "niezaszczepioni", "niezaszczepieni", "niezaszczepi??", "niezaszczepi??", "nie zaszczepi??", "nie zaszczepiona", "nie zaszczepiony", "nie zaszczepi??", "zaszczepi??", "zaszczepieni", "zaszczepiona", "zaszczepiony", "zaszczepi??", "nieszczepimy", "szczepi??", "szczepi??", "szczepiona", "szczepieni", "szczepiony", "szczepionki", "szczeczepionek", "szczepionkom", "szczepionkami", "szczepionkach", "szczepionka", "szczepionki", "szczepionce", "szczepionk??", "paszport covidowy", "paszportu covidowego", "paszportowi covidowemu", "paszportem covidowym", "paszporcie covidowym", "paszporty covidowe", "paszport??w covidowych", "paszportom covidowym", "paszportami covidowymi", "paszportach covidowych", "certyfikat covid", "certyfikatu covid", "certyfikatowi covidowemu", "certyfikatem covidowym", "certyfikacie covidowym", "certyfikaty covidowe", "certyfikat??w covidowych", "certyfikatom covidowym", "certyfikatami covidowymi", "certyfikatach covidowych"], 'vaccines')
  
    # General Ukraine
    batch_run(["ukry", "banderowcy", "banderowcom", "banderowcach", "banderowcami", "banderowc??w", "banderowiec", "banderowca", "banderowcowi", "bandera", "banderowcem", "banderowcu", "faszysci", "faszyst??w", "faszystom", "faszystami", "faszystach", "faszysty", "faszysta", "faszy??cie", "faszyst??", "faszyst??", "faszysto", "nazi??ci", "nazist??w", "nazistom", "nazistami", "nazistach", "nazisty", "nazista", "nazist??", "nazist??", "nazisto", "nazi??cie", "wo??y??", "wo??ynia", "wo??yniowi", "wo??yniem", "wo??yniu", "wo??y??skie", "wo??y??ski", "wo??y??skiego", "wo??y??skiemu", "wo??y??skim", "upa", "upowcy", "upowc??w", "upowcami", "upowcach", "ludob??jcy", "ludob??jcom", "ludob??jcami", "ludob??jcach", "ludob??jc??w", "ludob??jstwo", "ludob??jstwa", "ludub??jstwu", "ludob??jstwie", "ludob??jstwem", "oun", "ounowcy", "ounowc??w", "ounowcom", "ounowcami", "africansinukraine", "#mieszkanieprawemnietowarem", "patroleobywatelskie", "dezinformacja", "roszczenia", "afga??czycy", "afga??czyk", "agresja", "agresji", "agresj??", "agresj??", "aids", "anonymous", "armia", "armie", "armii", "atak", "atakach", "atakami", "ataki", "atakiem", "ataku", "atom", "atomowa", "atomowego", "atomowej", "atomowemu", "atomowy", "atomowym", "bia??uscy", "bia??usi", "bia??usini", "bia??usinom", "bia??usi??", "bia??uskie", "bia??uskiej", "bia??u??", "biologiczna", "biologicznej", "bitwa", "bitwy", "boj??wce", "boj??wek", "boj??wka", "boj??wkach", "boj??wkami", "boj??wki", "boj??wkom", "boj??wk??", "cen", "ceny", "charkowa", "charkowem", "charkowie", "charkowo", "charkowowi", "chark??w", "ciapaci", "ci????ar??wka", "ci????ar??wki", "czarnobyl", "czarnobyla", "czarnobylem", "czarnobylu", "czarnuchy", "dary", "dar??w", "dezinfmacj??", "dezinfmacyjnie", "dezinfmacyjny", "donbas", "donbasem", "donbasie", "donbasowi", "donbasu", "drogi", "europejska", "europejskiej", "faszy??ci", "gaz", "gazem", "gazie", "gazu", "genetycznego", "genetyczny", "granica", "granice", "granicy", "granicznej", "granic??", "gru??lica", "gru??licy", "haplotyp", "hiv", "hrywny", "hub", "incydent", "kacapy", "kijowa", "kijowem", "kijowie", "kijowowi", "kij??w", "kolei", "kolej", "konflikcie", "konflikt", "konfliktem", "konfliktowi", "konfliktu", "ko??ciele", "ko??cio??a", "ko??cio??em", "ko??cio??owi", "ko??ci????", "krym", "krymem", "krymie", "krymowi", "krymski", "krymu", "kryzys", "kryzysem", "kryzysie", "kryzysowi", "kryzysu", "lotos", "lotosu", "lugola", "lwowa", "lwowem", "lwowi", "lwowie", "lw??w", "majdan", "mieszkania", "mieszkaniach", "mieszkaniami", "mieszkanie", "mieszkaniom", "mieszkaniu", "mieszka??", "mig-29", "mig29", "migranci", "migrant", "migrant??w", "murzyni", "nato", "ndstream2", "odessa", "odessie", "odessy", "odess??", "odess??", "onuca", "onuce", "onuceonuc??", "onz", "operacja", "operacje", "operacji", "pa??stwa", "pa??stwem", "pa??stwie", "pa??stwo", "pa??stwu", "pesel", "pisokomuna", "pkp", "poci??gi", "pokomuna", "polacy", "polak", "polaka", "polakach", "polakami", "polakiem", "polakom", "polakowi", "polaku", "polak??w", "poland", "polish", "polishbder", "polsce", "polska", "polski", "polskich", "polskie", "polskiego", "polskiemu", "polskim", "polskimi", "polsko", "polsk??", "polsk??", "pomoc", "pomocy", "potyczka", "potyczke", "potyczki", "potyczk??", "putin", "putina", "putinem", "putinie", "putinowi", "putler", "radiacja", "radiacyjne", "radiacyjnego", "rasistach", "rasistami", "rasistom", "rasist??w", "rasizm", "rasizmem", "rasizmie", "rasizmowi", "rasizmu", "rasi??ci", "reakt", "reakta", "reaktze", "ropa", "ropie", "ropy", "rop??", "rosja", "rosjanie", "rosje", "rosji", "rosj??", "roszczeniach", "roszczeniami", "roszczeniem", "roszczeniom", "roszczeniu", "roszcze??", "rozbojami", "rozboje", "rozboj??w", "rozszczenie", "ruskaagentura", "ruskibot", "ruskieonuce", "rz??d", "rz??du", "rz??dzie", "rz??dz??cy", "samoloty", "samolot??w", "sankcjach", "sankcjami", "sankcje", "sankcji", "sankcjom", "segregacja", "segregacje", "segregacji", "segregacj??", "segregacj??", "socjal", "socjalem", "socjalowi", "socjalu", "syryjczycy", "syryjczyk", "szpital", "szpitala", "szpitalach", "szpitalami", "szpitale", "szpitalem", "szpitali", "szpitalom", "szpitalowi", "szpitalu", "terytialne", "terytialnego", "terytialnemu", "terytialny", "terytialnym", "tir", "tiry", "tir??w", "traktowania", "traktowanie", "traktowaniu", "traktowa??", "traktuj??", "uchod??ca", "uchod??cy", "uchod??c??w", "ucieczce", "ucieczka", "ue", "ukraina", "ukraince", "ukrainc??w", "ukrainek", "ukrainie", "ukrainiec", "ukrainka", "ukrainkach", "ukrainki", "ukrainko", "ukrainkom", "ukraink??", "ukraink??", "ukraino", "ukrainy", "ukrain??", "ukrain??", "ukrai??ca", "ukrai??cach", "ukrai??cami", "ukrai??cem", "ukrai??com", "ukrai??cowi", "ukrai??cu", "ukrai??cy", "ukrai??c??w", "ukrai??ska", "ukrai??ski", "ukrai??skie", "ukrai??skiego", "ukrai??skiej", "ukrai??skiemu", "ukrai??skim", "ukrai??sk??", "ukra??c??w", "ukropolin", "urk", "urkom", "urkowie", "uzbrojenie", "warszawa", "warszawy", "wojna", "wojnanuklearna", "wojnie", "wojny", "wojn??", "wojsk", "wojska", "wojskach", "wojskami", "wojskiem", "wojsko", "wojskom", "wojsku", "wschodem", "wschodowi", "wschodu", "wschodzie", "wsch??d", "wyjazd", "wyjazdu", "zabiera", "zabieraj??", "zabierzecie", "zabierzemy", "zabierzesz", "zabior??", "zabior??", "zasi??ki", "zasi??kiem", "zasi??kom", "zasi??kowi", "zasi??ku", "zasi??k??w", "zdrajcach", "zdrajcami", "zdrajcom", "zdrajcy", "zdrajc??w", "znajoma", "??ugasku", "??uga??sk", "??uga??ska", "??uga??skim", "??uga??skowi", "??ukaszence", "??ukaszenka", "??ukaszenki", "??ukaszenko", "??ukaszenk??", "??ukaszenk??", "??ydach", "??ydami", "??ydom", "??ydzi", "??yd??w"],'general-ukraine')

    # General Polish Economy
    batch_run(["PolskiLad_PiS", "Polski??ad", "socjal", "rozdawnictwo", "??wiadczenia", "trzynastka", "socjalny", "Nowy Wa??", "Wa??", "??ad", "Straci", "Straci??em", "Straci??a", "Straci??", "Pensja", "Pensji", "Pensj??", "#wojna", "Ruski ??ad", "derusyfikacja", "emerytura", "policjant", "g??rnicy", "sprz??taczki", "podatek", "podatki", "podatk??w", "p??aca", "praca", "sk??adki", "sk??adek", "sk??adka", "pit Ulga", "Ulgi", "Uldze", "Tarcza", "Dro??yzna", "ceny", "drozyznapis", "inflacja", "inflacja", "inflacji", "inflacje", "dro??yzna", "dro??yzny", "dro??y??nie", "kryzys gospodarczy", "Trzaskowski", "szamz??d", "samz??dy", "Firma", "Firmy", "firmom", "przedsi??bic??", "przedsi??bica", "przedsi??bicy", "Zad??u??enie", "Zad??u??enia", "Zad??u??e??", "Kaczy??ski", "Morawiecki", "PiS", "PISu", "Kaczy??skiego", "Kaczy??skiemu", "Mawieckiemu", "Mawieckiego", "PMM", "PJK", "Premiera", "ho??ownia", "Platfma", "Platformie", "Platfmy", "PO", "Arlukowicz", "bbudka", "MichalSzczerba", "sikskiradek", "KLubnauer", "Dariusz_Jonski", "dudslaw", "Lewica", "Lewicy", "Razem", "ZandbergRAZEM", "Czarzasty", "K_Smiszek", "RobertBiedron", "Nauczycielom", "Nauczyciele", "Nauczycieli", "Nauczyciel", "Policjant", "Policjanci", "Policjantom", "sprz??taczki", "ochroniarze", "piel??gniarki", "lekarze", "zdrowie", "ochrona", "zdrowia", "Rodzina", "Rodzinom", "Rodzin", "rodziny", "rodzine", "rodzinie", "rodzinne", "Mieszkanie", "Mieszkania", "Mieszka??", "mieszkaniu", "Dom", "Domu", "Dom??w", "domy", "samotni", "samotny", "Inwestycja", "Inwestycji", "inwestycjom", "Ziemia", "Ziemii", "Rolnictwo", "Rolnictwa", "Rolnik", "Rolnicy", "Rolnik??w", "Infolinia", "Infolinii", "infolini??", "MF_gov_pl", "ZUS", "MRiPS_GOV_PL", "MRiPS_GOV_PL", "MRiTGOVPL", "z??ot??wka", "z??ot??wk??", "G??rnicy", "G??rnikom", "G??rniczych", "KGHM", "socjal", "rozdawnictwo", "??wiadczenia", "trzynastka", "socjalny", "stopy procentowe", "kredyty", "kredyt", "wzrost", "PKB", "d??ug", "gospodarczy", "ekonomiczny", "d??ug", "kryzys", "e-pit", "e-PIT", "wynajem", "mieszkania", "wymiana", "waluty", "k??amteusz"],'economy')