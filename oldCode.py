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
            data = col.find_one(query)
            return data, jsonify(data), 200
            # return jsonify(data), 200