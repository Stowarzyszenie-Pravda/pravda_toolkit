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
    batch_run(["Żyd", "Żydzi", "Żyda", "Żydów", "Żydowi", "Żydom", "Żyda", "Żydów", "Żydem", "Żydami", "Żydzie", "Żydach", "Żydzie", "Żydzi", "Żydostwo", "Żydki", "Żydek", "Holocaust", "Żydowskie", "Żydowski", "Żydokomuna", "Auschwitz", "holokaust", "holokaust", "holokaustu", "holokaustowi", "holokaust", "holokaustem", "holokauście", "holokauście"], 'antisemitism')

    #Vaccines
    batch_run(["stopsegregacjisanitarnej","stopss","segregacja", "covid1984", "nwo", "szczepimysie","szczepimysię","nieszczepimysię","segregację", "segregacji", "segregacją", "segregacji", "nieszczepimysie", "śmiertelna substancja", "śmiertelnej substancji", "śmiertelnej substancji", "śmiertelną substancją", "nop", "stopnop", "stop nop", "norymberga20", "zajob",  "plandemia", "plandemii", "plandemie", "plandemią", "niezaszczepiony", "niezaszczepiona", "niezaszczepioni", "niezaszczepieni", "niezaszczepię", "niezaszczepią", "nie zaszczepię", "nie zaszczepiona", "nie zaszczepiony", "nie zaszczepią", "zaszczepię", "zaszczepieni", "zaszczepiona", "zaszczepiony", "zaszczepią", "nieszczepimy", "szczepię", "szczepią", "szczepiona", "szczepieni", "szczepiony", "szczepionki", "szczeczepionek", "szczepionkom", "szczepionkami", "szczepionkach", "szczepionka", "szczepionki", "szczepionce", "szczepionką", "paszport covidowy", "paszportu covidowego", "paszportowi covidowemu", "paszportem covidowym", "paszporcie covidowym", "paszporty covidowe", "paszportów covidowych", "paszportom covidowym", "paszportami covidowymi", "paszportach covidowych", "certyfikat covid", "certyfikatu covid", "certyfikatowi covidowemu", "certyfikatem covidowym", "certyfikacie covidowym", "certyfikaty covidowe", "certyfikatów covidowych", "certyfikatom covidowym", "certyfikatami covidowymi", "certyfikatach covidowych"], 'vaccines')
  
    # General Ukraine
    batch_run(["ukry", "banderowcy", "banderowcom", "banderowcach", "banderowcami", "banderowców", "banderowiec", "banderowca", "banderowcowi", "bandera", "banderowcem", "banderowcu", "faszysci", "faszystów", "faszystom", "faszystami", "faszystach", "faszysty", "faszysta", "faszyście", "faszystę", "faszystą", "faszysto", "naziści", "nazistów", "nazistom", "nazistami", "nazistach", "nazisty", "nazista", "nazistę", "nazistą", "nazisto", "naziście", "wołyń", "wołynia", "wołyniowi", "wołyniem", "wołyniu", "wołyńskie", "wołyński", "wołyńskiego", "wołyńskiemu", "wołyńskim", "upa", "upowcy", "upowców", "upowcami", "upowcach", "ludobójcy", "ludobójcom", "ludobójcami", "ludobójcach", "ludobójców", "ludobójstwo", "ludobójstwa", "ludubójstwu", "ludobójstwie", "ludobójstwem", "oun", "ounowcy", "ounowców", "ounowcom", "ounowcami", "africansinukraine", "#mieszkanieprawemnietowarem", "patroleobywatelskie", "dezinformacja", "roszczenia", "afgańczycy", "afgańczyk", "agresja", "agresji", "agresją", "agresję", "aids", "anonymous", "armia", "armie", "armii", "atak", "atakach", "atakami", "ataki", "atakiem", "ataku", "atom", "atomowa", "atomowego", "atomowej", "atomowemu", "atomowy", "atomowym", "białuscy", "białusi", "białusini", "białusinom", "białusią", "białuskie", "białuskiej", "białuś", "biologiczna", "biologicznej", "bitwa", "bitwy", "bojówce", "bojówek", "bojówka", "bojówkach", "bojówkami", "bojówki", "bojówkom", "bojówkę", "cen", "ceny", "charkowa", "charkowem", "charkowie", "charkowo", "charkowowi", "charków", "ciapaci", "ciężarówka", "ciężarówki", "czarnobyl", "czarnobyla", "czarnobylem", "czarnobylu", "czarnuchy", "dary", "darów", "dezinfmacją", "dezinfmacyjnie", "dezinfmacyjny", "donbas", "donbasem", "donbasie", "donbasowi", "donbasu", "drogi", "europejska", "europejskiej", "faszyści", "gaz", "gazem", "gazie", "gazu", "genetycznego", "genetyczny", "granica", "granice", "granicy", "granicznej", "granicą", "gruźlica", "gruźlicy", "haplotyp", "hiv", "hrywny", "hub", "incydent", "kacapy", "kijowa", "kijowem", "kijowie", "kijowowi", "kijów", "kolei", "kolej", "konflikcie", "konflikt", "konfliktem", "konfliktowi", "konfliktu", "kościele", "kościoła", "kościołem", "kościołowi", "kościół", "krym", "krymem", "krymie", "krymowi", "krymski", "krymu", "kryzys", "kryzysem", "kryzysie", "kryzysowi", "kryzysu", "lotos", "lotosu", "lugola", "lwowa", "lwowem", "lwowi", "lwowie", "lwów", "majdan", "mieszkania", "mieszkaniach", "mieszkaniami", "mieszkanie", "mieszkaniom", "mieszkaniu", "mieszkań", "mig-29", "mig29", "migranci", "migrant", "migrantów", "murzyni", "nato", "ndstream2", "odessa", "odessie", "odessy", "odessą", "odessę", "onuca", "onuce", "onuceonucą", "onz", "operacja", "operacje", "operacji", "państwa", "państwem", "państwie", "państwo", "państwu", "pesel", "pisokomuna", "pkp", "pociągi", "pokomuna", "polacy", "polak", "polaka", "polakach", "polakami", "polakiem", "polakom", "polakowi", "polaku", "polaków", "poland", "polish", "polishbder", "polsce", "polska", "polski", "polskich", "polskie", "polskiego", "polskiemu", "polskim", "polskimi", "polsko", "polską", "polskę", "pomoc", "pomocy", "potyczka", "potyczke", "potyczki", "potyczkę", "putin", "putina", "putinem", "putinie", "putinowi", "putler", "radiacja", "radiacyjne", "radiacyjnego", "rasistach", "rasistami", "rasistom", "rasistów", "rasizm", "rasizmem", "rasizmie", "rasizmowi", "rasizmu", "rasiści", "reakt", "reakta", "reaktze", "ropa", "ropie", "ropy", "ropę", "rosja", "rosjanie", "rosje", "rosji", "rosją", "roszczeniach", "roszczeniami", "roszczeniem", "roszczeniom", "roszczeniu", "roszczeń", "rozbojami", "rozboje", "rozbojów", "rozszczenie", "ruskaagentura", "ruskibot", "ruskieonuce", "rząd", "rządu", "rządzie", "rządzący", "samoloty", "samolotów", "sankcjach", "sankcjami", "sankcje", "sankcji", "sankcjom", "segregacja", "segregacje", "segregacji", "segregacją", "segregację", "socjal", "socjalem", "socjalowi", "socjalu", "syryjczycy", "syryjczyk", "szpital", "szpitala", "szpitalach", "szpitalami", "szpitale", "szpitalem", "szpitali", "szpitalom", "szpitalowi", "szpitalu", "terytialne", "terytialnego", "terytialnemu", "terytialny", "terytialnym", "tir", "tiry", "tirów", "traktowania", "traktowanie", "traktowaniu", "traktować", "traktują", "uchodźca", "uchodźcy", "uchodźców", "ucieczce", "ucieczka", "ue", "ukraina", "ukraince", "ukrainców", "ukrainek", "ukrainie", "ukrainiec", "ukrainka", "ukrainkach", "ukrainki", "ukrainko", "ukrainkom", "ukrainką", "ukrainkę", "ukraino", "ukrainy", "ukrainą", "ukrainę", "ukraińca", "ukraińcach", "ukraińcami", "ukraińcem", "ukraińcom", "ukraińcowi", "ukraińcu", "ukraińcy", "ukraińców", "ukraińska", "ukraiński", "ukraińskie", "ukraińskiego", "ukraińskiej", "ukraińskiemu", "ukraińskim", "ukraińską", "ukrańców", "ukropolin", "urk", "urkom", "urkowie", "uzbrojenie", "warszawa", "warszawy", "wojna", "wojnanuklearna", "wojnie", "wojny", "wojną", "wojsk", "wojska", "wojskach", "wojskami", "wojskiem", "wojsko", "wojskom", "wojsku", "wschodem", "wschodowi", "wschodu", "wschodzie", "wschód", "wyjazd", "wyjazdu", "zabiera", "zabierają", "zabierzecie", "zabierzemy", "zabierzesz", "zabiorą", "zabiorę", "zasiłki", "zasiłkiem", "zasiłkom", "zasiłkowi", "zasiłku", "zasiłków", "zdrajcach", "zdrajcami", "zdrajcom", "zdrajcy", "zdrajców", "znajoma", "ługasku", "ługańsk", "ługańska", "ługańskim", "ługańskowi", "łukaszence", "łukaszenka", "łukaszenki", "łukaszenko", "łukaszenką", "łukaszenkę", "żydach", "żydami", "żydom", "żydzi", "żydów"],'general-ukraine')

    # General Polish Economy
    batch_run(["PolskiLad_PiS", "PolskiŁad", "socjal", "rozdawnictwo", "świadczenia", "trzynastka", "socjalny", "Nowy Wał", "Wał", "Ład", "Straci", "Straciłem", "Straciła", "Stracił", "Pensja", "Pensji", "Pensję", "#wojna", "Ruski ład", "derusyfikacja", "emerytura", "policjant", "górnicy", "sprzątaczki", "podatek", "podatki", "podatków", "płaca", "praca", "składki", "składek", "składka", "pit Ulga", "Ulgi", "Uldze", "Tarcza", "Drożyzna", "ceny", "drozyznapis", "inflacja", "inflacja", "inflacji", "inflacje", "drożyzna", "drożyzny", "drożyźnie", "kryzys gospodarczy", "Trzaskowski", "szamząd", "samządy", "Firma", "Firmy", "firmom", "przedsiębicą", "przedsiębica", "przedsiębicy", "Zadłużenie", "Zadłużenia", "Zadłużeń", "Kaczyński", "Morawiecki", "PiS", "PISu", "Kaczyńskiego", "Kaczyńskiemu", "Mawieckiemu", "Mawieckiego", "PMM", "PJK", "Premiera", "hołownia", "Platfma", "Platformie", "Platfmy", "PO", "Arlukowicz", "bbudka", "MichalSzczerba", "sikskiradek", "KLubnauer", "Dariusz_Jonski", "dudslaw", "Lewica", "Lewicy", "Razem", "ZandbergRAZEM", "Czarzasty", "K_Smiszek", "RobertBiedron", "Nauczycielom", "Nauczyciele", "Nauczycieli", "Nauczyciel", "Policjant", "Policjanci", "Policjantom", "sprzątaczki", "ochroniarze", "pielęgniarki", "lekarze", "zdrowie", "ochrona", "zdrowia", "Rodzina", "Rodzinom", "Rodzin", "rodziny", "rodzine", "rodzinie", "rodzinne", "Mieszkanie", "Mieszkania", "Mieszkań", "mieszkaniu", "Dom", "Domu", "Domów", "domy", "samotni", "samotny", "Inwestycja", "Inwestycji", "inwestycjom", "Ziemia", "Ziemii", "Rolnictwo", "Rolnictwa", "Rolnik", "Rolnicy", "Rolników", "Infolinia", "Infolinii", "infolinię", "MF_gov_pl", "ZUS", "MRiPS_GOV_PL", "MRiPS_GOV_PL", "MRiTGOVPL", "złotówka", "złotówkę", "Górnicy", "Górnikom", "Górniczych", "KGHM", "socjal", "rozdawnictwo", "świadczenia", "trzynastka", "socjalny", "stopy procentowe", "kredyty", "kredyt", "wzrost", "PKB", "dług", "gospodarczy", "ekonomiczny", "dług", "kryzys", "e-pit", "e-PIT", "wynajem", "mieszkania", "wymiana", "waluty", "kłamteusz"],'economy')