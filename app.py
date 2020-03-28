from flask import Flask, request, jsonify
from flask_pymongo import pymongo
import pprint

# create an instance of the Flask class for a single module
app = Flask(__name__) 

# handle things for the database yo
CONNECTION_STRING = "mongodb+srv://juliet:juliet1234@es96-avo-cluster-xo415.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)

# set the current database to be the airbnb one for now 
db = client.get_database('sample_airbnb')
collection = pymongo.collection.Collection(db, 'listingsAndReviews')
mycol = pymongo.collection.Collection(db, 'listingsAndReviews')

# define what the home page looks like 
@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas! hi"

#test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John"})
    mycol.insert_one({'x': 1})
    hello = db.listingsAndReviews.find({})
    # pprint(hello)
    # for k in hello:
    #     pprint(k)
    # return jsonify(books= [b.serialize for b in hello])

    return "Connected to the data base!"
    

if __name__ == '__main__':
    app.run(port=8000)

