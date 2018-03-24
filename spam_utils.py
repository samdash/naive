
import os

import bs4
import dill
from spamclassifier import get_features
APP = os.path.abspath(__file__)
APP_DIR, APP_NAME = os.path.split(APP)

classifier_file_path = os.path.join(APP_DIR, 'saved_classifier', 'spam_classifier.pickle')
classifier_file = open(classifier_file_path, 'rb')
classifier_object = dill.load(classifier_file)
classifier_file.close()


def ham_or_spam(input_text):
    """
    :param input_text: the passed input text to be classified
    :returns: Whether the passed input is a spam, ham or giving
              UnicodeEncodeError
    """
    try:
        input_text = bs4.UnicodeDammit.detwingle(
            input_text).decode('utf-8')
        input_text = input_text.encode('ascii', 'ignore')

        hamorspam = classifier_object.classify(get_features(input_text,''))
        response = {'category': hamorspam, 'status': 'ok'}

        print ("TEXT: '{0}' :: RESPONSE : '{1}'".format(
            input_text.replace("\n", " ").replace("\r", " "),
                    hamorspam
                ))

        return response
    except UnicodeEncodeError:
        hamorspam = 'UnicodeEncodeError'
        response = {'category': hamorspam, 'status': 'error'}
        return response
