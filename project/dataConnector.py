import pymongo
import nltk
import operator
from textblob import TextBlob



class DataConnector():

    def __init__(self):
        """initialize the variables which will be used by the class

        """
        self.__uri="mongodb://127.0.0.1:27017"
        self.__client= pymongo.MongoClient(self.__uri)    #Database connection
        self.__db = self.__client['response']              #Database  


    def get_collection(self, input_class):
        """retrieve the collections from the database

        Parameters
        ----------
        user_class : str
            The class of the user input


        Returns
        -------
        str[]
            The collection
        """

        return self.__db[input_class] 



