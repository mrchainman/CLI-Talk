#!/usr/bin/python3
import json
# Headers
headers = {'OCS-APIRequest': 'true',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
          }
# Set some parameters for requesting chat messages, limit to 3 to make it fast for testing
data_chat = {'lookIntoFuture':0, 'setReadMarker':0, 'limit':3}
jsondir = "../json"
# Try to load the dictionary from the json file, else we create an empty dictionary
# TODO: There will be a problem, if to conversations have the same participant name, we have to handle that
try:
    with open(f"{jsondir}/dictionary.json",'r') as lf:
        dict_token_participant = json.load(lf)
except:
    dict_token_participant = {}
