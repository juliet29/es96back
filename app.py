"""
To execute locally:
1.) In command line type "source venv/bin/activate" to turn on the virtual environment 
2.)To enable debugging (i.e. get more helpful error messages, and things print to command line):
export FLASK_APP=app
export FLASK_ENV=development
flask run
3.) If no need debugging, can just type "python app.py"



app.py is the brain of the API, a lightweight Flask application that takes advantages of the following:

Flask: python framework for creating web applications: https://flask.palletsprojects.com/en/1.1.x/

MongoDB: database that handles unstructured (non-SQL like) data: https://www.mongodb.com/ 
    Atlas: a MongoDB cloud service, that allows the database to be hosted online rather than locally: https://api.mongodb.com/python/current/

PyMongo: library that allows Python projects to connect to mongodb: https://api.mongodb.com/python/current/

Postman: (not actually in this program) used for testing API links: https://www.postman.com/

Heroku: allow this to project to be accessed as from any computer by hosting it online @ https://es96app.herokuapp.com/: https://www.heroku.com/what

"""

from flask import Flask, request, jsonify
from flask_pymongo import pymongo
import pprint
import os 
import glob                      
import json                       
import datetime                       
from bson.objectid import ObjectId
from flask import render_template

# create an instance of the Flask class for a single module
app = Flask(__name__) 

# extend JSONencoder class to convert all responses to JSON string to allow cross-platform data interpretation 
class JSONEncoder(json.JSONEncoder):                           
    ''' extend json-encoder class'''
    def default(self, o):                               
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

# set app to use this extended class 
app.json_encoder = JSONEncoder

# connect to online database (Atlas) using PyMongo client feature 
CONNECTION_STRING = "mongodb+srv://juliet:juliet1234@es96-avo-cluster-xo415.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)


# define what the home page looks like 
@app.route('/')
def home():
    return "Welcome to the ES96a Avocado Database"


@app.route('/test', methods=['GET', 'POST', 'PATCH'])
def test():
    "Handle GET, POST, PATCH requests. Returns a HTML template for GET method, message for POST method, and the patched item for PACTH method"

    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.es96_april

    # return items in a collection in an HTML doc
    if request.method == 'GET':
        query = request.args
        # if no query is given, then return everything in the collection 
        if not query:
            all_items = [] 
            for items in col.find():
                all_items.append(items)
            return render_template('testdata.html', all_items = all_items)
       
        else:
            # find all items that match the query 
            all_items = [] 
            for items in col.find(query):
                all_items.append(items)
            return render_template('testdata.html', all_items = all_items)


    # retrieve data from the request if it is not a GET method
    data = request.get_json()  

    # if valid data exists in the request, create a new document in the collection
    if request.method == 'POST':   
        if data.get('data', None) is not None and data.get('time', 
            None) is not None:
            col.insert_one(data)
            return jsonify({'ok': True, 'message': 'New Avocado created   successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters! Need "data" and a "time"'}), 400


    if request.method == 'PATCH':
        # find this document to patch based on an a query
        query = request.args
        # replace a few parameters in the document based on data from the request 
        new_values = {"$set": data}

        try:
            col.update_one(query, new_values)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        patched_item = col. find_one(query)
        
        return jsonify(patched_item), 200




# returns the actual data in JSON format 
@app.route('/justdata', methods=['GET'])  
def justdata():
    "Return only the data inside the database"
    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.es96_april

    # return items in a collection 
    if request.method == 'GET':
        query = request.args
        # if no query is given, then return everything in the collection 
        if not query:
            all_items = [] 
            for items in col.find():
                all_items.append(items)
            return jsonify(all_items), 200
        else:
            # find all items that match the query 
            all_items = [] 
            for items in col.find(query):                
                all_items.append(items)

            return jsonify(all_items), 200


if __name__ == '__main__':
    app.run()
