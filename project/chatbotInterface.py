# -*- coding: utf-8 -*-
import os
import sys
from textblob import TextBlob
from flask import Flask, request, render_template, jsonify
import json
from nlpUnderstanding import NLPUnderstanding
from responseExtraction import ResponseExtraction 

class ChatbotInterface():

    def __init__(self):
        """create the variables which will be used by the class
        """

        self.__input = ''
        self.__lang = ''
        self.__executed = False


    def start_chat(self, user_in):
        """handle the chat process by getting the user input and returning the response to him/her

        Parameters
        ----------
        user_in : str
            The user input


        Returns
        -------
        str
            The chatbot response
        """
    
        self.__input=user_in
        NLPU = NLPUnderstanding()
        re =ResponseExtraction()
        #This code will be excuted only once at the begining of the program to detect the language for loading the corresponding modules """
        if not self.__executed:
            self.__select_lan()
            self.executed=True
        _focus = NLPU.get_sequence_labeler_model(self.__lang).extract_focus(self.__input)
        _class = NLPU.get_classifier_model(self.__lang).classify(self.__input)
        output = re.get_response(_class,_focus,self.__input)
        return output;



    def __select_lan(self):
        """select the language of the user input
        """

        if TextBlob(self.__input).detect_language() == "ar":
            self.__lang = "ar"

        else:     
            self.__lang = "en"



    def get_input(self):
        """return the user input

        Returns
        -------
        str
            User input

        """
        return self.__input
    
        return self.__input


