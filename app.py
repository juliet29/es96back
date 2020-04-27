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
            return jsonify(all_items), 200, all_items

        # otherwise return the specific item that was queried (only one though!)
        else:
            data = col. find_one(query)
            return data, jsonify(data), 200
            # return jsonify(data), 200

# get some data, run some code on it, (TODO: and put it back in the database )
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    # get data based on the user this will be in the form of some json data 
    app.logger.info('just a log')
    datastore = userdata() # list of all our data

    # this is how we speak to the console (in soothing tones, not with print) 
    app.logger.info('the user is %s', datastore)

    actual_data = [];
    for item in datastore[2]:
        if 'data' in item:
            #app.logger.info('there is some data!')
            actual_data.append(item.get('data'))
    
    app.logger.info('there is some data! %s', actual_data)

    # return an html template of this data 
    return render_template('freqdata.html', actual_data = actual_data)



# returns the actual data in JSON format 
@app.route('/justdata', methods=['GET'])  
def justdata():
    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.es96_april

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
        else:
            all_items = [] 
            for items in col.find(query):
                # find all items that match the query 
                all_items.append(items)

            return jsonify(all_items), 200
        # otherwise return the specific item that was queried (only one though!)



################### OG route ##################
@app.route('/test', methods=['GET', 'POST', 'PATCH'])
def test():
    # connect to a database with PyMongo Client 
    db = client.testdb
    # retrive the collection within the database we will be working with 
    col = db.es96_april

    # return items in a collection in a pretty format
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
            all_items = [] 
            for items in col.find(query):
                # find all items that match the query 
                all_items.append(items)
            return jsonify(data), 200


    # make a new avocado
    # get the data from the request! 
    data = request.get_json() 
    if request.method == 'POST':
        # if valid data exists in the request, add to the database 
        if data.get('data', None) is not None and data.get('time', 
            None) is not None:
            col.insert_one(data)
            return jsonify({'ok': True, 'message': 'New Avocado created   successfully!'}), 200

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters! Need "data" and a "time"'}), 400


    # patch request
    data = request.get_json() 
    if request.method == 'PATCH':
        # find the one document to patch 
        query = request.args

        # update it 
        # set new values to be updates
        #new_values = {$set: data}
        new_values = {$set: {'session_id': 'test3'}}
        try:
            col.update_one(query, new_values)
        except NameError as err:
            return jsonify({"error w/ request"})

        path_item = []
        for x in col.find():
            patch_item.append(x)
        return jsonify({'ok': True, 'message': 'New Avocado patched successfully!'}), 200


        # iterate through the query items and update





            # # find this one item in the db
        # try:
        #     find_result = col.find_one(query)
        # except NameError as err:
        #     find_result = None
        #     print("item not found in this collection")
        # if find_result != None and type(find_result) == dict:
        #     print ("found doc:", find_result)
        




        # # if valid data exists in the request, add to the database 
        # if data.get('data', None) is not None and data.get('time', 
        #     None) is not None:
        #     col.insert_one(data)
        #     return jsonify({'ok': True, 'message': 'New Avocado patched  successfully!'}), 200

        # else:
        #     return jsonify({'ok': False, 'message': 'Bad request parameters! Need "data" and a "time"'}), 400
    
if __name__ == '__main__':
    app.run()

# port=8000