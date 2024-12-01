"""This module provides with functions for calculating the word similarities"""

import numpy as np
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic


__INDEX_ERROR_MSG = "list index out of range"
__ic_brown = 'ic-brown.dat'


def damerau_levenshtein_dist():
    """
    Functions returns the function calculate_damerau_levenshtein_distance which just requires two words as inputs.

    Returns
    -------
    function

    """

    def calculate_damerau_levenshtein_distance(word1, word2):
        """

        Parameters
        ----------
        word1: str
            first string
        word2: str
            second string

        Returns
        -------
        distance: int
            resulting Damerau-Levenshtein Distance
        """

        max_edit_distance = len(word1) + len(word2)

        matrix = [[max_edit_distance for n in range(len(word2) + 2)]]
        matrix = matrix + [[max_edit_distance] + list(range(len(word2) + 1))]
        matrix = matrix + [[max_edit_distance, m] + [0] * len(word2) for m in range(1, len(word1) + 1)]

        last_row = {}

        for row in range(1, len(word1) + 1):
            current_character_word1 = word1[row - 1]

            last_matching_column = 0

            for column in range(1, len(word2) + 1):
                current_character_word2 = word2[column - 1]

                last_matching_row = last_row.get(current_character_word2, 0)

                costs = 0 if current_character_word1 == current_character_word2 else 1

                matrix[row + 1][column + 1] = min(
                    matrix[row][column] + costs,
                    matrix[row + 1][column] + 1,
                    matrix[row][column + 1] + 1,

                    matrix[last_matching_row][last_matching_column]
                    + (row - last_matching_row - 1) + 1
                    + (column - last_matching_column - 1))

                if costs == 0:
                    last_matching_column = column

            last_row[current_character_word1] = row

        return matrix[-1][-1]

    return calculate_damerau_levenshtein_distance


def damerau_levenshtein_sim():
    """
    Functions returns the function calculate_damerau_levenshtein_similarity which just requires two words as inputs.

    Returns
    -------
    function

    """

    def calculate_damerau_levenshtein_similarity(word1, word2):
        """
        Calculates the Damerau-Levenshtein Similarity between two words.

        Parameters
        ----------
        word1 : str
            first string
        word2 : str
            second string

        Returns
        -------
        distance: float
            resulting Damerau-Levenshtein Similarity
        """
        dist_fun = damerau_levenshtein_dist()
        dist = dist_fun(word1, word2)
        return 1 - (dist / (max(word1.__len__(), word2.__len__())))

    return calculate_damerau_levenshtein_similarity


def levenshtein_dist(case_sensitive=False):
    """
    Functions returns the function __calculate_levenshtein_distance which just requires two words as inputs,
    with parameter case_sensitive set.

    Parameters
    ----------
    case_sensitive : bool, optional
        default False, if True, levenshtein_sim is case sensitive.

    Returns
    -------
    function

    """

    def calculate_levenshtein_distance(word1, word2):
        """
        Calculates the Levenshtein Distance between two words

        Parameters
        ----------
        word1 : str
            first string
        word2 : str
            second string

        Returns
        -------
        distance: float
            resulting Levenshtein Distance

        """
        size_x = len(word1) + 1
        size_y = len(word2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if (case_sensitive and word1[x - 1].__eq__(word2[y - 1])) or \
                        (not case_sensitive and word1[x - 1].casefold().__eq__(word2[y - 1].casefold())):
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )

        return matrix[size_x - 1, size_y - 1]

    return calculate_levenshtein_distance


def levenshtein_sim(case_sensitive=False):
    """
    Functions returns the function calculate_levenshtein_similarity which just requires two words as inputs,
    with parameter case_sensitive set.

    Parameters
    ----------
    case_sensitive : bool, optional
        default False, if True, levenshtein_sim is case sensitive.

    Returns
    -------
    function

    """

    def calculate_levenshtein_similarity(word1, word2):
        """
        Calculates the Levenshtein Similarity between two words.

        Parameters
        ----------
        word1 : str
            first string
        word2 : str
            second string

        Returns
        -------
        distance: float
            resulting Levenshtein Similarity
        """
        dist_fun = levenshtein_dist(case_sensitive)
        dist = dist_fun(word1, word2)
        return 1 - (dist / (max(word1.__len__(), word2.__len__())))
    return calculate_levenshtein_similarity


def max_sim(sim1, sim2):
    """
    Function returns the function calculate_max_similarity which just requires two words as inputs,
    with parameters sim1 and sim2 set.

    Parameters
    ----------
    sim1 : function
        word similarity function, taking only two str as input
    sim2 : function
        word similarity function, taking only two str as input

    Returns
    -------
    function
    """

    def calculate_max_similarity(word1, word2):
        """
        Calculates the max similarity.

        Parameters
        ----------
        word1 : str
            first string
        word2 : str
            second string

        Returns
        -------
        float
        """
        score1 = sim1(word1, word2)
        score2 = sim2(word1, word2)

        return max(score1, score2)

    return calculate_max_similarity


def __initiate_wordnet():
    """
    Function downloads wordnet files, if not already available.

    Returns
    -------
    None
    """
    try:
        nltk.data.find('corpora/wordnet.zip')
        nltk.data.find('corpora/wordnet_ic.zip')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('wordnet_ic')


def path_sim():
    """
    Functions returns the function calculate_path_similarity which just requires two words as inputs.

    Returns
    -------
    function

    """

    def calculate_path_similarity(word1, word2):
        """
        The Path Similarity treats words as a graph. The number of edges between edges is a measure
        of conceptual distance between terms.
        So the function gives a measure of how similar the senses of word1 and word2 are.

        Parameters
        ----------
        word1 : str
            first string
        word2 : str
            second string

        Returns
        -------
        float
            distance between terms
        """
        __initiate_wordnet()

        if word1 == word2:
            return 1

        syns1 = wn.synsets(word1)
        syns2 = wn.synsets(word2)

        best_value = 0

        for syn1 in syns1:
            for syn2 in syns2:
                current = wn.path_similarity(syn1, syn2)

                if current is not None and current > best_value:
                    best_value = current

        return best_value

    return calculate_path_similarity


def leacock_chodorow_sim():
    """
    Functions returns the function calculate_leacock_chodorow_similarity which just requires two words as inputs.

    Returns
    -------
    function

    """

    def calculate_leacock_chodorow_similarity(word1, word2):
        """
        Leacock-Chodorow Similarity computes the scaled semantic_sim similarity between two concepts in WordNet.
        The function gives the shortest path and maximum depth of the sense of word1 and word2.

        Parameters
        ----------
        word1, word2 : str
            name of the node

        Returns
        -------
        normalized path length : float
        """
        __initiate_wordnet()

        try:
            syn1 = wn.synsets(word1)[0]
            syn2 = wn.synsets(word2)[0]

            return wn.lch_similarity(syn1, syn2)

        except IndexError:
            print(__INDEX_ERROR_MSG)

            return 0

    return calculate_leacock_chodorow_similarity


def wu_palmer_sim():
    """
    Functions returns the function calculate_wu_palmer_similarity which just requires two words as inputs.

    Returns
    -------
    function

    """

    def calculate_wu_palmer_similarity(word1, word2):
        """
        Wu-Palmer Similarity measures the position of word1 and word2 to the position of the
        most specific common concept.

        Parameters
        ----------
        word1, word2 : str
            name of the node

        Returns
        -------
        conceptual similarity : float
        """
        __initiate_wordnet()

        if word1 == word2:
            return 1

        elif word1 == '' or word2 == '':
            return 0

        else:
            syn1 = wn.synsets(word1)[0]
            syn2 = wn.synsets(word2)[0]
            return wn.wup_similarity(syn1, syn2)
    return calculate_wu_palmer_similarity


def resnik_sim(information_corpus=None):
    """
    Functions returns the function calculate_resnik_similarity which just requires two words as inputs,
    with parameter information_corpus set.

    Parameters
    ----------
    information_corpus: dict
        Dictionary with two keys, noun and verb, whose values are dictionaries that map from
        synsets to information content values.

    Returns
    -------
    function

    """

    def calculate_resnik_similarity(word1, word2):
        """
        Resnik Similarity is the measure of information shared between two words.
        Is based on the Information Corpus of the of the Least Common Subsumer.

        Parameters
        ----------
        word1, word2 : str
            Name of the node.

        Returns
        -------
        information content : float
        """
        __initiate_wordnet()

        nonlocal information_corpus
        if information_corpus is None:
            information_corpus = wordnet_ic.ic(__ic_brown)

        try:
            syn1 = wn.synsets(word1)[0]
            syn2 = wn.synsets(word2)[0]
            return wn.res_similarity(syn1, syn2, information_corpus)

        except IndexError:
            print(__INDEX_ERROR_MSG)

            return 0

    return calculate_resnik_similarity


def jiang_conrath_sim(information_corpus=None):
    """
    Functions returns the function calculate_jiang_conrath_similarity which just requires two words as inputs,
    with parameter information_corpus set.

    Parameters
    ----------
    information_corpus : dict
        Dictionary with two keys, noun and verb, whose values are dictionaries that map from
        synsets to information content values.

    Returns
    -------
    function

    """

    def calculate_jiang_conrath_similarity(word1, word2):
        """
        The Jiang-Conrath function measures the score of the sens of two words, basing on the Information Content.

        Parameters
        ----------
        word1, word2 : str
            Name of the node.

        Returns
        -------
        similarity of two words sense : float
        """
        __initiate_wordnet()

        nonlocal information_corpus
        if information_corpus is None:
            information_corpus = wordnet_ic.ic(__ic_brown)

        if word1 == word2:
            return 1

        elif word1 == '' or word2 == '':
            return 0

        else:
            syn1 = wn.synsets(word1)[0]
            syn2 = wn.synsets(word2)[0]

            return wn.jcn_similarity(syn1, syn2, information_corpus)

    return calculate_jiang_conrath_similarity


def lin_sim(information_corpus=None):
    """
    Functions returns the function calculate_lin_similarity which just requires two words as inputs,
    with parameter case_sensitive set.

    Parameters
    ----------
    information_corpus : dict
        Dictionary with two keys, noun and verb, whose values are dictionaries that map from
        synsets to information content values.

    Returns
    -------
    function

    """

    def calculate_lin_similarity(word1, word2):
        """
        Lin Similarity measures the meaning between word1 and word2.

        Parameters
        ----------
        word1, word2 : str
            name of the node

        Returns
        -------
        similarity of two words sense : float
        """
        __initiate_wordnet()

        nonlocal information_corpus
        if information_corpus is None:
            information_corpus = wordnet_ic.ic(__ic_brown)

        try:
            syns1 = wn.synsets(word1)
            syns2 = wn.synsets(word2)

            best_fit = 0

            try:
                for syn1 in syns1:
                    for syn2 in syns2:
                        current = wn.lin_similarity(syn1, syn2, information_corpus)

                        if current > best_fit:
                            best_fit = current

                return best_fit

            except nltk.corpus.reader.wordnet.WordNetError:

                return best_fit

        except IndexError:
            print(__INDEX_ERROR_MSG)

        return 0

    return calculate_lin_similarity
