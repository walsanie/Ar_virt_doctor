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
from sequenceLabeler import SequenceLabeler
    
class LSTM(SequenceLabeler):


    def __init__(self, lang):
        """initialize the variables and create LSTM model which will be used by the class

        Parameters
        ----------
        lang : str
            The language of the text

        """

        #Global variables for the model files
        self.__LSTM_Model=""
        self.__word2idx=""
        self.__tag2idx=""
        


        # Load arabic language model
        if lang == "ar":
            LSTM_Model_filename = 'LSTM_Model.h5'
            self.__LSTM_Model = load_model(LSTM_Model_filename,
                                custom_objects={'precision': precision, 'recall': recall, 'fmeasure': fmeasure})

            self.__word2idx = np.load('word2idx.npy', allow_pickle=True).item()
            self.__tag2idx = np.load('tag2idx.npy', allow_pickle=True).item()
            print("test")



        # load English modules, all files starts with E
        else:
            LSTM_Model_filename = 'E_LSTM_Model.h5'
            self.__LSTM_Model = load_model(LSTM_Model_filename,
                                custom_objects={'precision': precision, 'recall': recall, 'fmeasure': fmeasure})

            self.__word2idx = np.load('E_word2idx.npy', allow_pickle=True).item()
            self.__tag2idx = np.load('E_tag2idx.npy', allow_pickle=True).item()



    def extract_focus(self,user_input):
        """extract the focus from user input

        Parameters
        ----------
        user_input : str
            The user input


        Returns
        -------
        str
            The focus
        """

        """ input processing """
        ns = nltk.word_tokenize(user_input)
        st_list = user_input.split()
        nwords = list(set(ns))
        nwords.append("ENDPAD")
        n_words = len(nwords)
        max_len = 12
        nword2idx = {w: i + 1 for i, w in enumerate(nwords)}

        X_tee = []
        for w in st_list:
            try:
                X_tee.append(self.__word2idx[w])
            except:
                X_tee.append(self.__word2idx["OOV"])

        XX_tee = [X_tee]
        XX_tee = pad_sequences(maxlen=max_len, sequences=XX_tee, padding="post", value=0)

        tags = []

        for key, value in self.__tag2idx.items():
            tags.append(key)

        i = 0
        """ model predicts the focus of the input"""
        p = self.__LSTM_Model.predict(np.array([XX_tee[i]]))
        p = np.argmax(p, axis=-1)

        _focus=''
        """ struct the focus """
        for w, pred in zip(st_list, p[0]):
            if w != 0 and tags[pred]!='O':
                _focus += " " + w

        return _focus
