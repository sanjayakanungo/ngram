# ngram-language-model

## 1 Overview

The program allows the user to create an *n*-gram language model with an *n* of their choice, train it on a corpus and generate random texts from it using Maximum Likelihood Estimation.

## 2 Functionality

The program makes use of functions `word_tokenize()`, `sent_tokenize()` and `TreebankWordDetokenizer.detokenize()` from the `nltk` (Natural Language Toolkit) library, plus function `randint()` from the `random` module.

The process consists of two main steps: model training and sentence generation.

### 2.1 Training

Firstly, a language model object is created and the number of tokens (*n*) to concatenate in an *n*-gram is specified by the user. In order to train the model, the program opens the text file provided, stores it in a variable of type string and proceeds to segment it into sentences using the NLTK sentence segmentation function, which returns a list of sentence strings. This allows to add beginning-of-sentence and end-of-sentence markers (`BOS` and `EOS`) before and after every sentence. The text is recomposed into a long string by combining the sentences one by one, together with beginning and end-of-sentence markers. `PAD` tokens are also added at the beginning and at the end of the text in the case of *n*-grams with *n* > 3.

At this point, the text is tokenized using the NLTK word tokenizer function, which returns a list of token strings that are used to form *n*-grams, stored in a list of tuples of *n* strings. Finally, when *n*-grams are created, the program counts the instances of all unique *n*-grams and (*n*-1)-grams
and stores everything in a dictionary. Then, the *n*-grams’ relative frequency is calculated by dividing the *n*-gram counts by the counts of the corresponding (*n*-1)-gram (which contains the same tokens up to *n*-1).

### 2.2 Generation

The model allows to generate sentences based on the training corpus’ *n*-gram sequences. When prompted to generate a sentence, a token sequence is chosen to serve as the input to begin the process. In the case of a bigram model, the first token is `BOS`; for a trigram model, the first sequence is `EOS BOS`; for *n*-grams with *n* > 3, a random token sequence ending with `EOS BOS` is chosen.

Then, the model starts generating the sentence one token at a time, each time choosing a token randomly among the probability distribution of tokens occurring after the preceding (*n*-1)-gram, until it encounters an end-of-sentence marker. The final string, obtained from the detokenization of the resulting token sequence, is sliced in order to cut off any sentence markers and `PAD` tokens. This process is repeated several times for
creating texts of multiple sentences.

## 3 Testing

The program was tested using the `pytest` module, as well as manually, in order to avoid or minimize possible errors. Three possible language model types were considered: *n*-gram models with *n* = 2, *n* = 3 and *n* = 4 (the latter represents all models with *n* > 3). For each of these, a test file was created to check that the results from the model trained on a small test text were correct. The user interface, given the interactive aspect of `input` functions, was tested manually.

## 4 Documentation

The program can be started by running the file `main.py` from the terminal, which allows the user to interact with it by entering commands in the console. After opening it, they are asked to train a new language model in order to generate texts from it. By entering `t`, they will get to choose the number of tokens *n* to concatenate in an *n*-gram and the file they want to open and train the model on, and start the training process. When this is completed, the user can make the trained model generate random texts (`g`), or they can decide to create and train a new model (`t`). If they go for the former, they can choose between printing a text to the screen (`p`) or writing a certain number of texts to a file (`w`); in this case, they need to specify the number of texts that they want the model to write and the name of the file they want to create.

## 5 Conclusion

Some modifications could be implemented to improve the language model’s performance.

As it is now, the program creates one sentence at a time, every time starting from scratch. The code could be modified to create more than one sentence at a time, so that each sentence is linked to the previous one, or, more precisely, the first word(s) of a sentence are chosen considering the last word(s) of the previous sentence. Also, beginning and end-of-sentence markers (`BOS` and `EOS`) could be joined into a single sentence boundary marker that marks both beginning and end of sentence. These changes would improve the performance of *n*-gram models with *n* > 2.

Moreover, the program uses non-customized tokenization, detokenization and sentence segmentation functions. With certain corpora, especially with uncommon or non-standard punctuation, a precise segmentation cannot be ensured; ideally, an analysis of the specific corpus is needed to fix any issues that can arise while training the model on it.


The above repo is accessible from here: https://github.com/ni-kozen/ngram-language-model/