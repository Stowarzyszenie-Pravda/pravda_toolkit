import pandas as pd

def top_n_sisters(n, text, df):
    # text musy be proccessed
    df['similarity_to_text'] = df['nlp_title'].apply(lambda new_text: new_text.similarity(text))
    return df.sort_values(by=['similarity_to_text'], ascending=False).head(n)