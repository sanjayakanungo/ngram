"""Defines a class to create a Language Model, train it and generate sentences

It requires the nltk module, the nltk.tokenize.treebank module and the random
module

Classes
-------
    LanguageModel

Functions
---------
    tokenize(text)
    sent_segment(text)
    detokenize(tokens)
"""

from corpus import *
from random import randint


class LanguageModel:
    """Class that is used to create a Language Model

    Attributes
    ----------
    n : int
        The number of tokens to concatenate in an n-gram
    text : str
        The training corpus enriched with beginning and end-of-sentence tokens
    tokens : list
        The tokens extracted from the corpus
    n_grams : list
        The n-grams formed with the corpus' tokens
    stats : dict
        The (n-1)-gram and n-gram counts and the relative frequency of n-grams

    Methods
    -------
    train(file)
        Trains language model on corpus
    p_next(token_seq)
        Calculates probability distribution of tokens occurring after a
        specific token sequence
    generate()
        Generates random sentence from the language model
    """

    def __init__(self, n):
        """
        Parameters
        ----------
        n : int
            The number of tokens to concatenate in an n-gram
        """

        self.n = n

    def train(self, file):
        """Trains language model on corpus

        Parameters
        ----------
        file : TextIOWrapper (file)
            The corpus used to train the language model
        """

        # Load corpus file and segment text into sentences
        f = open(file)
        self.text = f.read()
        f.close()
        sentences = sent_segment(self.text)

        # Add beginning-of-sentence and end-of-sentence markers (and PAD tokens
        # for n-gram models with n > 3)
        if self.n > 2:
            self.text = 'PAD ' * (self.n-3) + 'EOS '
        else:
            self.text = ''

        for sent in sentences:
            self.text += 'BOS ' + sent + ' EOS '

        if self.n > 2:
            self.text += 'BOS ' + 'PAD ' * (self.n-3)

        #BOS Once Up EOS
        #Up On a Time
        #On a Time there
        #a Time there lived
        #Time there lived 4

        #BOS There lived 4 pigs <BOS> <EOS>

        # Tokenize text and form ngrams
        self.tokens = tokenize(self.text)
        self.n_grams = [tuple(self.tokens[i: i + self.n])
                        for i in range(len(self.tokens) - self.n + 1)]

        # Create dictionary of (n-1)-gram and n-gram counts
        self.stats = {}
        for ngram in self.n_grams:
            if ngram[:-1] not in self.stats:
                self.stats[ngram[:-1]] = {'CNT': 1, ngram[-1]: {'CNT': 1}}
            elif ngram[-1] not in self.stats[ngram[:-1]]:
                self.stats[ngram[:-1]]['CNT'] += 1
                self.stats[ngram[:-1]][ngram[-1]] = {'CNT': 1}
            else:
                self.stats[ngram[:-1]]['CNT'] += 1
                self.stats[ngram[:-1]][ngram[-1]]['CNT'] += 1

        # Add relative frequency of n-grams to dictionary
        for ngram, dict in self.stats.items():
            for token in dict:
                if token == 'CNT':
                    continue
                self.stats[ngram][token]['FRQ'] = \
                    self.stats[ngram][token]['CNT'] / self.stats[ngram]['CNT']
                
        print("Training complete")

    def p_next(self, token_seq):
        """Calculates probability distribution of tokens occurring after a
        specific token sequence

        This method can be called only after training the model with train()

        Parameters
        ----------
        token_seq : list
            The token sequence ((n-1)-gram) for which the probability
            distribution is calculated

        Returns
        -------
        list
            The list containing the probability distribution (all possible
            tokens and their relative frequency)
        """

        # Create list of all possible tokens and their relative frequency
        prob_d = []
        for token, dict in self.stats[tuple(token_seq)].items():
            if token == 'CNT':
                continue
            prob_d.append(tuple([token,
                                 self.stats[tuple(token_seq)][token]['FRQ']]))

        # Sort list from word with highest probability to lowest (needed only
        # to display the probability distribution)
        # prob_dist.sort(key=lambda a: a[1], reverse = True)

        return prob_d

    def generate(self):
        """Generates random sentence from the language model

        This method can be called only after training the model with train()

        Returns
        -------
        string
            A sentence generated from the language model
        """

        # Define first token sequence to be used to start generation process
        if self.n == 2:
            sent = ['BOS']
        elif self.n == 3:
            sent = ['EOS', 'BOS']
        else:
            begin = []
            for ngram in self.stats.keys():
                if ngram[-1] == 'BOS':
                    begin.append(ngram)
            sent = list(begin[randint(0, len(begin) - 1)])

        # Generate sentence one token at a time until an end-of-sentence marker
        # is reached
        while True:
            complete = False
            try:
                prob_dist = self.p_next(sent[1-self.n:])
                sent = sent + [prob_dist[randint(0, len(prob_dist) - 1)][0]]

                if sent[-1] == 'EOS':
                    complete = True
                    sent = detokenize(sent[self.n-1: -1])

                elif sent[-1] == 'BOS':
                    complete = True
                    sent = detokenize(sent[self.n-1: -2])

                elif sent[-1] == 'PAD':
                    complete = True
                    pads = 0
                    for token in sent:
                        if token == 'PAD':
                            pads += 1
                    sent = detokenize(sent[self.n-1: -2-pads])

                if complete is True:
                    if sent == '':
                        sent = list(begin[randint(0, len(begin) - 1)])
                        continue
                    elif ' .' in sent:
                        p1, punct, p2 = sent.partition(' .')
                        sent = p1 + '.' + p2
                        return sent
                    else:
                        return sent

            except KeyError:
                sent = list(begin[randint(0, len(begin) - 1)])
                continue
