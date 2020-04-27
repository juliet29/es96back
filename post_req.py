import requests
from requests.exceptions import HTTPError
import json

# to run, type python post_req.py into the console 

# api url that can handle post and get methods --> can also go here to see all existing requests 
url = "https://es96app.herokuapp.com/test"

# information to send in json format --> more on this here: https://requests.readthedocs.io/en/master/user/quickstart/

payload = {
    "_id": "128", # can not have the same id as another avocado already in the database. if not sure, just don't include and mongodb will autogenerate an id that can be modified later;
    "name" : "newname12", # nessecary param 
    "birthplace" : "atx4", # nessecary param 
    "time": "2020-04-02:23:27",
    "username": "Jamie AvoScanner",
    "device": "spectrometer_1",
    "tags": [
        {
            "tag_1": "austin",
            "tag_2": "HEB",
            "tag_3": "california"
        }
    ],
    "data": [
        {
            "freq1": "80",
            "freq2": "70",
            "freq3": "60",
            "freq4": "50"
        }
    ]
}

# need to let api know we are sending data that is in json
headers = {
  'Content-Type': 'application/json',
}

# use an exceptions to raise errors and print to the console should they happen  
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    # if this is succesful, then you will see {"message":"New Avocado created   successfully!","ok":true}
    print(response.text.encode('utf8'))
    # If the response was successful, no Exception will be raised
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  
else:
    print('Success!')



