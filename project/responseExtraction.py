import pymongo
import nltk
import operator
from textblob import TextBlob
from dataConnector import DataConnector
from extractionMethod import ExtractionMethod as e

class ResponseExtraction():

    def __init__(self):
        """initialize the data connector object which will be used by the class

        """
        self.__dc = DataConnector();

    def __no_focus(self, input_class, input_txt):
        """If the focus is not extracted from the input, then retrieve the response based on the class only

        Parameters
        ----------
        input_class : str
            The class of the user input
        input_txt : str
            The user input


        Returns
        -------
        str
            The response
        """
        col = self.__dc.get_collection(input_class)       #Choosing the collection based on the class given

        #col.create_index([('Output', 'text')])

        if any ([input_class=="عام", input_class=="General request"]):       #This class has only one document, and text similarties won't work with this case
            docs = col.find({}, { "Output": 1, "_id": 0})                    #So we'll simply retrieve that document
            docs = list(docs)
            str = docs[0]
            str = str['Output']
            return str;


        docs=col.find({}, {"Output":1, "_id":0} )           #Retrieve all documents to compare using Jaccard method
        docs= list(docs)

        if not docs:                    #Empty lists = False
            str="Sorry, no answer found"
            return str;

        dic = {}
        for doc in docs:
            dic[doc['Output']] = e.computeSimilarity(doc['Output'], input_txt)

        sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)          #Sort based on the score

        answer = col.find({"Output": sorted_dic[0][0]}, {"Output": 1, "_id": 0})
        answer=list(answer)

        str=answer[0]
        str=str['Output']
        return str;


    def get_response(self, input_class, focus, input_txt):
        """retrieve the response based on the class and focus

        Parameters
        ----------
        input_class : str
            The class of the user input
        focus : str
            The focus of the user input
        input_txt : str
            The user input


        Returns
        -------
        str
            The response
        """
        col = self.__dc.get_collection(input_class)           #Choosing the collection based on the class given

        if input_class == "General request":            # Since the English module gives a focus for this case, which should not have a focus, we removed it
            focus = ""

        if not focus:
            
            str=self.__no_focus(input_class, input_txt)
            return str;


        #col.create_index([('Focus', 'text')])        # ** If you didn't created the index, Run this code one time for each collection to create the text index
        docs=col.find({"$text": {"$search": focus}}, {"Output":0, "_id":0} )   #id:0 to remove the id from the output
        docs= list(docs)

        dic = {}

        if not docs:                    #Empty lists = False, if no answer was found we'll retreive all and use Jaccard method
            docs = col.find({}, {"_id": 0})
            docs = list(docs)
            similar = []

            for doc in docs:
                dic[doc['Focus']]=nltk.edit_distance(focus, doc['Focus'])  # zero if equal, 1 is totally different
                if  dic[doc['Focus']] ==1:                                  # Checking if the value of the Focus score is 1
                    similar.append(doc['Focus'])                            # Add to list


            if TextBlob(input_txt).detect_language() == "ar":
                 if similar:
                     str="هل تقصد"
                     for s in similar:
                         str+=s+"؟"
                     return str;

                 else:
                    str="عذراً، لم أستطع إيجاد إجابة مناسبة لسؤالك"
                    return str;


            else:
                if similar:
                    str= "Do you mean"
                    for s in similar:
                        #print(s, "؟")
                        str += s + "?"
                    return str;
                else:
                     str= "Sorry, no answer found"
                     return str;



        for doc in docs:        # if some documents were found, sort based on the similarity score
            dic[doc['Focus']]=e.computeSimilarity(doc['Focus'], focus)

        sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

        answer=col.find({"Focus": sorted_dic[0][0]}, { "Output":1, "_id":0} )

        str = answer[0]           #Hieghest score will be at the first index
        str = str['Output']
        return str;

