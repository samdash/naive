from __future__ import division
import os
from datetime import datetime
import logging
# import pickle   ## importing dill instead
import random
from spamclassifier import trainer,get_features
import dill
from termcolor import colored
# current directory where create_pickle.py is situated
MODULE_DIR = os.path.abspath(os.path.join('.'))
CORPUS_DIR = os.path.join(MODULE_DIR, '', 'corpus2')
CLASSIFIER_DIR = os.path.join(MODULE_DIR, 'saved_classifier')
CLASSIFIER_FILE = os.path.join(CLASSIFIER_DIR, 'spam_classifier.pickle')

logging.basicConfig(
    filename='logfile.txt',
    level = logging.DEBUG,
    filemode = 'w',
    format = '%(asctime)s - %(levelname)s - %(message)s'
)


def save_pickle():
    directory = CORPUS_DIR

    logging.info("Testing the classifier on dataset : {0}".format(directory))

    ## training it
    starting_time = datetime.now()
    train_set, test_set, classifier = trainer()
    end_time = datetime.now()

    ## saving the classifier
    save_classifier = open(CLASSIFIER_FILE, "wb")
    dill.dump(classifier, save_classifier,protocol=2)
    save_classifier.close()

    elapsed = end_time - starting_time
    minutes_elapsed, seconds_elapsed = divmod(
        elapsed.total_seconds(), 60)[0], divmod(elapsed.total_seconds(), 60)[1]
    print (colored("Training took {min} minutes : {sec} seconds".format(
        min=minutes_elapsed,
        sec=seconds_elapsed
        ),'green'))
    logging.info("Training took {min} minutes : {sec} seconds".format(
        min=minutes_elapsed,
        sec=seconds_elapsed
        ))

def main():
    save_pickle()

if __name__ == "__main__":
    main()