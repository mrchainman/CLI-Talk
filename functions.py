#!/usr/bin/python3
import requests
import json
import time
import os
from settings import *
try:
    from config import *
except:
    pass

def check_config():
    try:
        open("config.py",'r')
    except:
        print("No config file found, let's create it!")
        url = input('Enter your nextcloud url: ')
        user = input('Enter your username: ')
        password = input('Enter your password: ')
        with open ("config.py",'a') as f:
            f.write(f"#!/usr/bin/python3\nurl = \"{url}/ocs/v2.php/apps/spreed/api/v1\"\nuser = \"{user}\"\npassword = \"{password}\"")
        print("We need to restart the app now, sorry ;)")
        exit(0)

def get_data():
    r_conversations = requests.get(f"{url}/room", headers=headers, auth=(user, password))
    m_conversations = (r_conversations.json())
    for i in range(len(m_conversations["ocs"]["data"])):
        token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
        r_participants = requests.get(f"{url}/room/{token_i}/participants", headers=headers, auth=(user, password))
        m_participants = (r_participants.json())
        participant_i = (m_participants["ocs"]["data"][1]["displayName"])
        data_chat = {'lookIntoFuture':0, 'setReadMarker':0, 'limit':3}
        r_messages = requests.get(
            f"{url}/chat/{token_i}",
            headers=headers, auth=(user, password),
            params=data_chat)
        m_messages = (r_messages.json())
        for i in range(len(m_messages["ocs"]["data"])):
            print(f"{participant_i}\n\n")
            print(m_messages["ocs"]["data"][i]["message"])
        print("-----------------------------------------\n-----------------------------------------\n-----------------------------------------\n")
