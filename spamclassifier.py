from __future__ import print_function, division
import os
import random
from collections import Counter
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier, classify

MODULE_DIR = os.path.abspath(os.path.join('.'))
CORPUS_DIR = os.path.join(MODULE_DIR, '', 'corpus2')

stoplist = stopwords.words('english')

def init_lists(folder):
    a_list = []
    file_list = os.listdir(folder)
    for a_file in file_list:
        f = open(folder + a_file, 'r')
        a_list.append(f.read())
    f.close()
    return a_list

def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(unicode(sentence, errors='ignore'))]

def get_features(text, setting):
    if setting=='bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}

def train(features, samples_proportion):
    train_size = int(len(features) * samples_proportion)
    # initialise the training and test sets
    train_set, test_set = features[:train_size], features[train_size:]
    print ('Training set size = ' + str(len(train_set)) + ' documents')
    print ('Test set size = ' + str(len(test_set)) + ' documents')
    # train the classifier
    classifier = NaiveBayesClassifier.train(train_set)
    return train_set, test_set, classifier

def evaluate(train_set, test_set, classifier):
    # check how the classifier performs on the training and test sets
    print ('Accuracy on the training set = ' + str(classify.accuracy(classifier, train_set)))
    print ('Accuracy of the test set = ' + str(classify.accuracy(classifier, test_set)))
    # check which words are most informative for the classifier
    classifier.show_most_informative_features(20)


def trainer():

    spamdirectory = os.path.join(CORPUS_DIR, 'spam/')
    hamdirectory = os.path.join(CORPUS_DIR, 'ham/')

    spam = init_lists(spamdirectory)
    ham = init_lists(hamdirectory)
    all_messages = [(message, 'spam') for message in spam]
    all_messages += [(message, 'ham') for message in ham]
    random.shuffle(all_messages)
    all_features = [(get_features(message, ''), label) for (message, label) in all_messages]
    return train(all_features, 0.8)


if __name__ == '__main__' :
    # initialise the data
    spam = init_lists('corpus2/spam/')
    ham = init_lists('corpus2/ham/')
    all_messages = [(message, 'spam') for message in spam]
    all_messages += [(message, 'ham') for message in ham]
    random.shuffle(all_messages)
    print ('Corpus size = ' + str(len(all_messages)) + ' documents')

    # extract the features
    all_features = [(get_features(message, ''), label) for (message, label) in all_messages]
    print ('Collected ' + str(len(all_features)) + ' feature sets')

    # train the classifier
    train_set, test_set, classifier = train(all_features, 0.8)

    # evaluate its performance
    evaluate(train_set, test_set, classifier)