# -*- coding: utf-8 -*-
import os
import sys

    
class ExtractionMethod():

    def computeSimilarity(list1, list2):
        """compute the jaccard similarity between the collection's responses and the input

        Parameters
        ----------
        
        list1 : str[]
            The user input
        list2 : str[]
            The responses


        Returns
        ----------
        
        float
            The similarity value
        """
      
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection / union)



