import re

def to_lowercase(text):
    return text.lower()

# TODO put in file below to be able to choose
pl_stopwords = set(open("../data/pl_stopwords.txt", encoding="utf-8", mode='r').read().split("\n"))
def remove_stopwords(text, stopwords = pl_stopwords):
    return ' '.join([word for word in text.split(" ") if word not in stopwords])

def remove_mentions(text):
    return re.sub(r'\B\@([\w\-]+)','', text)    

def remove_hashtags(text):
    return re.sub(r'\B\#([\w\-]+)','', text)    

def remove_urls(text):
    return re.sub(r'http\S+','', text)    

def remove_emojis(text):
    regrex_pattern = re.compile(pattern = "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'', text)

# TODO in the future as emojis can deliver a lot of important informations
# def emojis_to_words(text):
#     return text

def remove_punctuation(text):
    return re.sub(r'[^\w\s]','', text)    

def remove_numbers(text):
    return re.sub(r' \d+','', text)    

def remove_n_length_words(text, n = 1):
    return ' '.join([word for word in text.split(" ") if len(word) > n])

def remove_duplicated_spaces(text):
    return " ".join(text.split())

def preprocess_text(text):
    text = to_lowercase(text)
    text = remove_stopwords(text)
    text = remove_mentions(text)
    text = remove_hashtags(text)
    text = remove_urls(text)
    text = remove_emojis(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_n_length_words(text)
    text = remove_duplicated_spaces(text)
    return text