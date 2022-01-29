import spacy
import re

def count_capital_letters(doc) -> int:
    """Counts number of capital letters in a document

    Args:
        doc (spaCy document): spaCy document

    Returns:
        int: Number of capital letters in a document
    """
    return len(re.findall(r'[A-Z]', doc.text))

def count_words_starting_with_capital_letter(doc) -> int:
    """Counts number of words starting with capital letter

    Args:
        doc (spaCy document): spaCy document

    Returns:
        int: Number of words starting with capital letter
    """
    return len([word for word in words_from_doc(doc) if word[0].isupper()])

def count_syllables(word: str, vowels: str = "aeiouy") -> int:
    """Takes word and counts number of syllables in it (algorithm is based on heuristics and not 100% accurate)

    Args:
        word (str): Word to count number of syllables in
        vowels (str, optional): List of vowels. Defaults to "aeiouy".

    Returns:
        int: Number of syllables in the given word
    """
    # Splits vowels to make a list
    vowels = list(vowels)

    number_of_syllables = 0
    if word[0] in vowels:
        number_of_syllables += 1
    
    # Iterates over letters
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            number_of_syllables += 1

    if number_of_syllables == 0:
        number_of_syllables += 1      
    return number_of_syllables

def words_from_doc(doc, not_word_pos_list: list = ["PUNCT", "SYM", "X"]) -> list:
    """Takes spaCy doc and returns words. Based on https://universaldependencies.org/docs/u/pos/.

    Args:
        doc (spaCy document): spaCy document
        not_word_pos_list (list, optional): List of part of speech that are not considered words. Defaults to ["PUNCT", "SYM", "X"].

    Returns:
        list: List of words from the given document
    """
    words = []
    for token in doc:
        if token.pos_ not in not_word_pos_list:
            words.append(token.text)
    return words

def words_from_pos(doc, pos: list) -> list:
    """Takes spaCy document and returns certain parts of speech. Based on https://universaldependencies.org/docs/u/pos/.

    Args:
        doc (spaCy document): spaCy document
        pos (list): List of part of speech to be returned.

    Returns:
        list: List of certain part of speech
    """
    words = []
    for token in doc:
        if token.pos_ == pos:
            words.append(token.text)
    return words

def percent_of_complex_nouns(doc):
    """
    Takes spaCy document and returns percent of complex nouns. 
    """
    return len(filter(is_complex, words_from_pos(doc, "NOUN")))/count_words(doc)*100

def percent_of_nouns(doc):
    """
    Takes spaCy document and returns percent of nouns. 
    """
    return len(words_from_pos(doc, "NOUN"))/count_words(doc)*100

def percent_of_complex_verbs(doc):
    """
    Takes spaCy document and returns percent of complex verbs. 
    """
    return len(filter(is_complex, words_from_pos(doc, "VERB")))/count_words(doc)*100

def percent_of_verbs(doc):
    """
    Takes spaCy document and returns percent of verbs. 
    """
    return len(words_from_pos(doc, "VERB"))/count_words(doc)*100

def percent_of_complex_adjectives(doc):
    """
    Takes spaCy document and returns percent of complex adjectives. 
    """
    return len(filter(is_complex, words_from_pos(doc, "ADJ")))/count_words(doc)*100

def percent_of_adjectives(doc):
    """
    Takes spaCy document and returns percent of adjectives. 
    """
    return len(words_from_pos(doc, "ADJ"))/count_words(doc)*100

def noun_to_verb_ratio(doc):
    """
    Takes spaCy document and returns noun to verb ratio.
    """
    return percent_of_nouns(doc)/percent_of_verbs(doc)

def count_words(doc):
    """
    Takes spaCy doc and returns number of words.
    """
    return len(words_from_doc(doc))

def is_complex(word):
    """
    Takes word and returns number boolean whether is complex or not. Complex words are words that have 3 or more than 3 syllables.
    """
    return count_syllables(word) >= 4

def count_complex_words(doc):
    """
    Takes spaCy document and returns number of complex words. 
    """
    number_of_complex_words = 0
    for word in words_from_doc(doc):
        if is_complex(word):
            number_of_complex_words += 1
    return number_of_complex_words

def percent_of_complex_words(doc):
    """
    Takes spaCy document and returns percent of complex words. 
    """
    return count_complex_words(doc)/count_words(doc)*100

def sentences_from_doc(doc):
    """
    Takes spaCy doc and returns sentences.
    """
    return list(doc.sents)

def count_sentences(doc):
    """
    Takes spaCy doc and returns number of sentences.
    """
    return len(sentences_from_doc(doc))

def average_sentence_length(doc):
    """
    Takes spaCy doc and returns average sentence length.
    """
    return sum(len(sentence) for sentence in sentences_from_doc(doc))/count_sentences(doc)

def fog_index(doc):
    """
    Takes spaCy document and returns FOG readability index. The FOG index is can be used to confirm that text can be read easily by the intended audience.
    """
    return 0.4 * (count_words(doc) / count_sentences(doc) + 100 * count_complex_words(doc) / count_words(doc))     

def pisarek_index(doc, linear = False):
    """
    Takes spaCy document and returns Pisarek's index.
    """
    if linear == True:
        return 1 / 3 * count_words(doc) / count_sentences(doc) + 1 / 3 * 100 * count_complex_words(doc) / count_words(doc) + 1
    # If is non-linear
    else:
        return 1 / 2 *  ((count_words(doc) / count_sentences(doc)) ** 2 + (100 * count_complex_words(doc) / count_words(doc)) ** 2)**(1/2)

