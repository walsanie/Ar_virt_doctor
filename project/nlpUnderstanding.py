import pymongo
import nltk
import operator
from textblob import TextBlob
from svm import SVM
from lstm import LSTM


class NLPUnderstanding():

    def get_sequence_labeler_model(self, lang):
        """get the model of the sequence labeling

        Parameters
        ----------
        lang : str
            The language of the text


        Returns
        -------
        LSTM object
            The sequence labeler model
        """
        labeler = LSTM(lang);
        return labeler


    def get_classifier_model(self, lang):
        """get the model of the classifier

        Parameters
        ----------
        lang : str
            The language of the text


        Returns
        -------
        SVM object
            The classifier model
        """
        classifierModel = SVM(lang);
        return classifierModel
