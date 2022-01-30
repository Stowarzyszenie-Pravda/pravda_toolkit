from file_manager import merge_files
from gephi import generate_edge_list

import text_cleaning as tc
import lingustic as lg

import os

import spacy

TWITTER_SCRAPED_DATA_PATH = "../data/twitter-scraped-data/"

# Purpose of this file to push in processed data to specific folders and enriching it with lingustic features
if __name__ == '__main__':


    nlp = spacy.load("pl_core_news_lg")
    for subdir, dirs, files in os.walk(TWITTER_SCRAPED_DATA_PATH):
        for e, dir in enumerate(dirs):
            dirpath = TWITTER_SCRAPED_DATA_PATH + dir
            df = merge_files(dirpath, drop_duplicates_by='id').drop("Unnamed: 0", axis = 1)

            # Generating Gephi DataFrame
            gephi_df = generate_edge_list(df)
            gephi_df.to_csv(dirpath + "/gephi.csv", encoding="utf-8", index=False)

            # Adding score column based on social metrics 
            df['score'] = df['nlikes'] + df['nreplies'] + df['nretweets']
            
            # Applying non-reductive text cleaning
            df['cleaned_tweet'] = df['tweet'].apply(lambda tweet: tc.remove_duplicated_spaces(tc.remove_mentions(tc.remove_emojis(tc.remove_hashtags(tc.remove_urls(tweet))))))

            # Apply spaCy document on all cleaned tweets
            docs = list(nlp.pipe(df['cleaned_tweet']))

            # Adding lingustic features
            df['lg_number_of_capital_letters'] = [lg.count_capital_letters(doc) for doc in docs]
            df['lg_number_of_words_starting_with_capital_letters'] = [lg.count_words_starting_with_capital_letter(doc) for doc in docs]
            df['lg_percent_of_complex_nouns'] = [lg.percent_of_complex_nouns(doc) for doc in docs]
            df['lg_percent_of_nouns'] = [lg.percent_of_nouns(doc) for doc in docs]
            df['lg_percent_of_complex_verbs'] = [lg.percent_of_complex_verbs(doc) for doc in docs]
            df['lg_percent_of_verbs'] = [lg.percent_of_verbs(doc) for doc in docs]
            df['lg_percent_of_complex_adjectives'] = [lg.percent_of_complex_adjectives(doc) for doc in docs]
            df['lg_percent_of_adjectives'] = [lg.percent_of_adjectives(doc) for doc in docs]
            df['lg_noun_to_verb_ratio'] = [lg.noun_to_verb_ratio(doc) for doc in docs]
            df['lg_number_of_words'] = [lg.count_words(doc) for doc in docs]
            df['lg_number_of_complex_words'] = [lg.count_complex_words(doc) for doc in docs]
            df['lg_percent_of_complex_words'] = [lg.percent_of_complex_words(doc) for doc in docs]
            df['lg_number_of_sentences'] = [lg.count_sentences(doc) for doc in docs]
            df['lg_average_sentence_length'] = [lg.average_sentence_length(doc) for doc in docs]
            df['lg_fog_index'] = [lg.fog_index(doc) for doc in docs]
            df['lg_pisarek_index'] = [lg.pisarek_index(doc) for doc in docs]
            df['lg_contains_badword'] = [lg.check_if_has_badword(doc) for doc in docs]

            # Adding purified (meaning adding another layer of text cleaning with removal of some informantion and) text column
            df['purified_tweet'] = df['cleaned_tweet'].apply(lambda tweet: tc.remove_duplicated_spaces(tc.remove_stopwords(tc.remove_punctuation(tc.remove_numbers(tc.remove_n_length_words(tc.to_lowercase(tweet)))))))

            df.to_csv(dirpath + "/processed.csv", encoding="utf-8", index=False)

        