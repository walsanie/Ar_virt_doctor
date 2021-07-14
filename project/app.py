# -*- coding: utf-8 -*-
import os
import sys
from textblob import TextBlob
from flask import Flask, request, render_template, jsonify
import json
import pymongo
from chatbotInterface import ChatbotInterface


app = Flask(__name__)

def __load_database_with_indices():
    try:   

        uri="mongodb://127.0.0.1:27017"
        client= pymongo.MongoClient(uri)    #Database connection
        db = client["response"] #Database 
        dbnames = client.list_database_names()
    
        client.server_info() # will throw an exception


    except:

        print ("connection error")



    if not db.list_collection_names():

        # use Python's open() function to load a JSON file
        with open('../db/Complaint.json') as f:

            col = db["Complaint"]

            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/General_health_questions.json') as f:

            col = db["General_health_questions"]
            __create(f, col) 

        # use Python's open() function to load a JSON file
        with open('../db/General_request.json') as f:
 
            col = db["General_request"]
       
            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/Goodbye.json') as f:

            col = db["Goodbye"]

            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/Greetings.json') as f:

            col = db["Greetings"]

            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/أسئلة_طبية.json') as f:

            col = db["أسئلة_طبية"]

            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/ترحيب.json') as f:

            col = db["ترحيب"]

            __create(f, col) 

        # use Python's open() function to load a JSON file
        with open('../db/شكوى.json') as f:

            col = db["شكوى"]

            __create(f, col) 

        # use Python's open() function to load a JSON file
        with open('../db/عام.json') as f:

            col = db["عام"]

            __create(f, col)

        # use Python's open() function to load a JSON file
        with open('../db/وداع.json') as f:

            col = db["وداع"]

            __create(f, col)
 
                
    
    client.close()  


def __create(f, col):

    for line in f:
        json_doc = json.loads(line)
        col.insert(json_doc)

    # iterate the MongoDB collection object's attributes
    for num, item in enumerate(dir(col)):
        # look for all of the methods with "index"
        if not "index" in item:
            col.create_index([('Output', 'text'), ('Focus', 'text')]) 
 
       

@app.route('/')
def home():
    """redirect user to the home page

    Returns
    -------
    html
        home page of the chatbot application

    """
    return render_template("Home.html")


@app.route('/get')
def get_bot_response():
    """return chatbot respone to the user

    Returns
    -------
    str
        response from the chatbot

    """
    UI = ChatbotInterface()
    userText = request.args.get('msg')
    output=UI.start_chat(userText)
    if not output:
        return str("No output found")
    return str(output)


if __name__ == "__main__":
    __load_database_with_indices()
    app.debug=True
    app.run(host = '0.0.0.0', port = 5000)
    
