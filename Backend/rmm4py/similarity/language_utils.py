"""
Module for simple NL functions
"""

import enum
import re
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer
from nltk.stem.snowball import GermanStemmer
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
nltk.download('omw-1.4')


class Language(enum.Enum):
    """
    Enum for languages
    """
    ENGLISH = "english"
    GERMAN = "german"


def tokenize(sentence):
    """
    Tokenizes a sentence

    Parameters
    ----------
    sentence : str
        sentence to tokenize

    Returns
    -------
    tokens : list of str
        resulting tokens
    """
    token_words = sentence.split()
    return token_words


def remove_stopwords(word_tokens, language):
    """
    Removes all stopwords of a list of tokens

    Parameters
    ----------
    word_tokens : list of str
        given tokens
    language : language
        language to use

    Returns
    -------
    filtered_tokens : list of str
        tokens without stopwords
    """
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    stop_words = set(stopwords.words(language.value))

    filtered_sentence = [w for w in word_tokens if w.lower() not in stop_words]

    return filtered_sentence


def stem_tokens(word_tokens, language, stemmer=None):
    """
    Stemms all tokens

    Parameters
    ----------
    word_tokens : list of str ord
        tokens to stem
    language : language
        language to use
    stemmer : stemmer, optional
        stemmer to use

    Returns
    -------
    stemmed_tokens : list of str
        resulting tokens
    """

    stemmed_word_tokens = []

    for word_token in word_tokens:
        stemmed_word_tokens.append(stem_word(word_token, language, stemmer))

    return stemmed_word_tokens


def nounify(verb_word):
    """
    Transforms a verb in a noun: die -> death
    Parameters
    ----------
    verb_word: string
        the word as a verb

    Returns
    -------
    list:
        the possible nouns for that verb

    """
    verb_synsets = wn.synsets(verb_word, pos="v")

    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets \
                   for l in s.lemmas() if s.name().split('.')[1] == 'v']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in verb_lemmas]

    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset().name().split('.')[1] == 'n']

    # Extract the words from the lemmas

    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])
    re = [r[0] for r in result]

    # return all the possibilities sorted by probability
    return re


def verbify(noun_word):
    """
    Transforms a noun in a verb: Death -> die
    Parameters
    ----------
    noun_word: string
    the word as a noun

    Returns
    -------
    list:
    the possible verbs for that noun
    """

    noun_synsets = wn.synsets(noun_word, pos="v")

    # Word not found
    if not noun_synsets:
        return []

    # Get all noun lemmas of the word
    noun_lemmas = [l for s in noun_synsets \
                   for l in s.lemmas() if s.name().split('.')[1] == 'n']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in noun_lemmas]

    # filter only the verbs
    related_verb_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset().name().split('.')[1] == 'v']

    # Extract the words from the lemmas

    words = [l.name() for l in related_verb_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])
    re = [r[0] for r in result]

    # return all the possibilities sorted by probability
    return re


def stem_word(word, language, stemmer=None):
    """
    Stems a word

    Parameters
    ----------
    word : str
        word to stem
    language : language
        language to use
    stemmer : stemmer, optional
        stemmer to use

    Returns
    -------
    stemmed: str
        stemmed word
    """
    if stemmer is None:

        if language is language.ENGLISH:
            stemmer = PorterStemmer()
        else:
            stemmer = GermanStemmer()

    stemmed = stemmer.stem(word)

    return stemmed


def check_synonym(word1, word2):
    """
    Function verifies whether two strings are synonyms or not.

    Parameters
    ----------
    word1 : str
        This word.
    word2 : str
        Other word, to be compared.

    Returns
    -------
    result : bool
        Returns True if words are synonyms, False otherwise.
    """
    try:
        nltk.data.find('corpora/wordnet.zip')
        nltk.data.find('corpora/wordnet_ic.zip')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('wordnet_ic')

    for syn in wordnet.synsets(word1):
        for lem in syn.lemmas():
            if lem.name() == word2:
                return True

    return False


def remove_special_chars(tokenized_sentence):
    """
    Function removes special characters from the given, tokenized string.

    Parameters
    ----------
    tokenized_sentence: list
        List of tokenized string that represents label of the node of the process model.

    Returns
    -------
    result: list
        List of strings without special characters.
    """
    result = []
    for item in tokenized_sentence:
        string = str(re.sub('[^A-Za-z0-9]+', ' ', item).strip())
        if string == '':
            continue
        result.append(string)

    return result
