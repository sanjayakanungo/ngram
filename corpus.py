"""Provides tokenization, sentence segmentation and detokenization functions

It requires the nltk module and the nltk.tokenize.treebank module

Functions
---------
    tokenize(text)
    sent_segment(text)
    detokenize(tokens)
"""

from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk
nltk.download('punkt')

def tokenize(text):
    """Extracts tokens from a text

    Parameters
    ----------
    text : str
        The corpus to be tokenized

    Returns
    -------
    list
        The list of tokens extracted from the text
    """

    return word_tokenize(text)


def sent_segment(text):
    """Segments a text into sentences

    Parameters
    ----------
    text : str
        The corpus to be segmented into sentences

    Returns
    -------
    list
        The list of sentences segmented from the text
    """

    return sent_tokenize(text)


def detokenize(tokens):
    """Joins a list of tokens into a sentence

    Parameters
    ----------
    tokens : list
        The list of tokens to be detokenized

    Returns
    -------
    str
        The sentence obtained by joining the tokens
    """

    return TreebankWordDetokenizer().detokenize(tokens)
