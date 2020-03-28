"""app.py is the brain of the API, a lightweight Flask application that takes advantages of the following:

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
    return "ES96a Avocado Database"

@app.route('/test', methods=['GET', 'POST'])
def test():
    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.testcol

    # return items in a collection 
    if request.method == 'GET':
        query = request.args
        # if no query is given, then return everything in the collection 
        if not query:
            # appending all items in the Cursor to a list, not sure if this is the best way
            all_items = [] 
            for items in col.find():
                all_items.append(items)
            return jsonify(all_items), 200
        # otherwise return the specific item that was queried (only one though!)
        else:
            data = col.find_one(query)
            return jsonify(data), 200


    # make a new avocado
    # get the data from the request! 
    data = request.get_json() 
    if request.method == 'POST':
        # if valid data exists in the request, add to the database 
        if data.get('name', None) is not None and data.get('birthplace', 
            None) is not None:
            col.insert_one(data)
            return jsonify({'ok': True, 'message': 'New Avocado created   successfully!'}), 200

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters! Need a "name" and a "birthplace"'}), 400

    
if __name__ == '__main__':
    app.run()

# port=8000