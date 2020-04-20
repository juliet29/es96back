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
    return "ES96a Avocado Database"

# send some data about an avocado with the format in sample_data.json
@app.route('/send', methods=['POST'])
def post():
    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.testcol

    data = request.get_json() 
    if request.method == 'POST':
        # if valid data exists in the request, add to the database 
        if data.get('username', None) is not None and data.get('data', 
            None) is not None:
            col.insert_one(data)
            return jsonify({'ok': True, 'message': 'New Avocado created   successfully!'}), 200

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters! Need a "username" and some "data"'}), 400

# get some data about an avocado for use within this script only
@app.route('/userdata', methods=['GET'])  # this might not be nessecary tbh 
def userdata():
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
                # now we have a list of all the items (this is a list of dictionaries), and can just return that ... (not returning a response, so cannot print)
            #return render_template('userdata.html', all_items = all_items)
            return all_items # THIS IS NOT A VALID RESPONSE LMAO, ONLY FOR INTERNAL USE, GOING TO /USERDATA WILL GIVE AN ERROR!
        # otherwise return the specific item that was queried (only one though!)
        else:
            data = col.find_one(query)
            return all_items
            # return jsonify(data), 200


# get some data, run some code on it, and put it back in the database 
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    # get data based on the user this will be in the form of some json data 
    app.logger.info('just a log')
    datastore = userdata() # list of all our data

    # this is how we speak to the console (in soothing tones, not with print) lol 
    # app.logger.info('the user is %s', datastore)

    actual_data = [];
    for item in datastore:
        if 'data' in item:
            #app.logger.info('there is some data!')
            actual_data.append(item.get('data'))
    
    app.logger.info('there is some data! %s', actual_data)


    # return "transformed!"
    return render_template('freqdata.html', actual_data = actual_data)


################### OG route ##################
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
            return render_template('testdata.html', all_items = all_items)
       
        else:
             # otherwise return the specific item that was queried (only one though!)
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