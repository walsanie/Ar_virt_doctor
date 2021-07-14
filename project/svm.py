# -*- coding: utf-8 -*-
import os
import sys
import os
import sys
import numpy as np
import nltk
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from textblob import TextBlob
from flask import Flask, request, render_template, jsonify
import json
scriptpath = "metrics3.py"
sys.path.append(os.path.abspath(scriptpath))
from metrics3 import precision, recall, fmeasure
from classifier import Classifier
    
class SVM(Classifier):


    def __init__(self, lang):

        """initialize the variables and create SVM model which will be used by the class

        Parameters
        ----------
        lang : str
            The language of the text

        """
        self.__SVM_Model=""
        self.__Tfidf_vect=""


        # Load arabic language model
        if lang == "ar":
            SVM_Model_filename = "Classifier.sav"

            with open(SVM_Model_filename, 'rb') as file:
                self.__SVM_Model = pickle.load(file)

            victor_filename = "Tfidf_vector.sav"
            with open(victor_filename, 'rb') as file1:
                self.__Tfidf_vect = pickle.load(file1)


        # load English modules, all files starts with E
        else:

            SVM_Model_filename = "E_Classifier.sav"

            with open(SVM_Model_filename, 'rb') as file:
                self.__SVM_Model = pickle.load(file)

            victor_filename = "E_Tfidf_vector.sav"
            with open(victor_filename, 'rb') as file1:
                self.__Tfidf_vect = pickle.load(file1)
        



    def classify(self, user_input):
        """classify the user input

        Parameters
        ----------
        user_input : str
            The user input


        Returns
        -------
        str
            The class
        """

        """ transform the input ti Tfidf vector"""
        Test_X = [user_input]
        Train_X_Tfidf = self.__Tfidf_vect.transform(Test_X).toarray()

        """ model predicts the class of the input"""
        predictions_SVM = self.__SVM_Model.predict(Train_X_Tfidf)

        """ name of classes """

        if TextBlob(user_input).detect_language()=="ar":
            target_names = ['أسئلة طبية', 'ترحيب', 'شكوى', 'عام', 'رفض', 'موافقة', 'وداع']
        else:
            target_names = ['Affirmation', 'Complaint', 'General health questions', 'General request', 'Goodbye', 'Greetings', 'Negation']

        _class = target_names[predictions_SVM[0]]

        return _class
