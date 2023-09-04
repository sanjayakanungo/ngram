"""Allows the user to create a Language Model and generate texts from it

The program allows you to create an n-gram language model with an n of your
choice, train it on a corpus and generate random texts from it using Maximum
Likelihood Estimation

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

from lm import *

print('\nThis program allows you to create an n-gram language model with an ' +
      'n of your choice, train it on a corpus and generate random texts ' +
      'from it. You only need a text file for the program to access.')
trained = False

# Ask user whether they want to train language model or generate text(s)
while True:
    if trained is False:
        choice = input('\nEnter \'t\' to train the language model on a ' +
                       'corpus. Type \'q\' to quit. > ')

    else:
        choice = input('\nEnter \'t\' to train the language model on a ' +
                       'corpus or \'g\' to generate text(s) from a trained ' +
                       'language model. Type \'q\' to quit. > ')

    if choice == 'q' or choice == 'Q':
        break

    # Ask user for n and corpus filename to train language model
    elif choice == 't' or choice == 'T':
        while True:
            try:
                ng = input('\nEnter the number of tokens (n) to concatenate ' +
                           'in an n-gram. Type \'b\' to go back. > ')
                if ng == 'b' or ng == 'B':
                    break

                elif int(ng) > 1:
                    while True:
                        try:
                            file = input('\nEnter the filename for the ' +
                                         'corpus you want to train the ' +
                                         'language model on. Type \'b\' to ' +
                                         'go back. > ')
                            if file == 'b' or file == 'B':
                                break

                            # Train language model
                            print('\nProcessing...')
                            LaM = LanguageModel(int(ng))
                            LaM.train(file)
                            trained = True
                            print('\nTraining completed!')

                            break

                        except FileNotFoundError:
                            print('\nInvalid entry. Enter the name of an ' +
                                  'existing text file in your folder.')

                    break

                else:
                    print('\nInvalid entry. Enter an integer greater than 1.')

            except ValueError:
                print('\nInvalid entry. Enter an integer greater than 1.')

    # Ask user whether they want to print a text or write text(s) to a file
    elif choice == 'g' or choice == 'G':
        if trained is False:
            print('\nInvalid entry.')
            continue

        while True:
            choice = input('\nEnter \'p\' to print a text to the screen or ' +
                           'enter \'w\' to write text(s) to a file. Type ' +
                           '\'b\' to go back. > ')
            if choice == 'b' or choice == 'B':
                break

            # Generate a text and print it to the screen
            elif choice == 'p' or choice == 'P':
                if int(ng) == 2:
                    ns = 2
                else:
                    ns = 9

                text = '\n'
                for i in range(0, ns):
                    text += LaM.generate() + ' '
                text += LaM.generate()

                while True:
                    if ' .' in text:
                        p1, punct, p2 = text.partition(' .')
                        text = p1 + '.' + p2
                    else:
                        break

                print(text)

            # Ask user for the number of texts they want the model to write
            # and the name of the file they want to create
            elif choice == 'w' or choice == 'W':
                while True:
                    try:
                        nt = input('\nEnter the number of texts you want to ' +
                                   'write to a file. Type \'b\' to go back. ' +
                                   '> ')

                        if nt == 'b' or nt == 'B':
                            break

                        elif int(nt) > 0:
                            while True:
                                name = input('\nEnter the name of the text ' +
                                             'file you want to write the ' +
                                             'text(s) to. Type \'b\' to go ' +
                                             'back. > ')

                                if name == 'b' or name == 'B':
                                    break

                                elif name.endswith('.txt'):
                                    try:
                                        # Generate text(s) and write them to
                                        # the file
                                        f = open(name, 'w')
                                        for i in range(0, int(nt)):
                                            if int(ng) == 2:
                                                ns = 2
                                            else:
                                                ns = 9

                                            text = ''
                                            for i in range(0, ns):
                                                text += LaM.generate() + ' '
                                            text += LaM.generate() + '\n'

                                            while True:
                                                if ' .' in text:
                                                    p1, punct, p2 = \
                                                        text.partition(' .')
                                                    text = p1 + '.' + p2
                                                else:
                                                    break

                                            f.write(text)
                                            f.write('\n')
                                        f.close()
                                        print('\nFile successfully written!')

                                        break

                                    except PermissionError:
                                        print('\nInvalid entry. Enter a ' +
                                              'valid .txt filename.')

                                else:
                                    print('\nInvalid entry. Enter a valid ' +
                                          '.txt filename.')

                        else:
                            print('\nInvalid entry. Enter a number greater ' +
                                  'than 0.')

                    except ValueError:
                        print('\nInvalid entry. Enter a number greater than ' +
                              '0.')

            else:
                print('\nInvalid entry.')

    else:
        print('\nInvalid entry.')
        continue
