# -*- coding: utf-8 -*-
import os
import sys
from abc import ABC, abstractmethod

    
class SequenceLabeler(ABC):

    @abstractmethod
    def __init__(self, lang):
        """abstract class initialization method

        Parameters
        ----------
        lang : str
            The language of the text
        """   
        pass


    @abstractmethod
    def extract_focus(self, user_input):
        """abstract method which extract focus from the user input

        Parameters
        ----------
        user_input : str
            The input of the user
        """
        pass
