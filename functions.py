#!/usr/bin/python3
# import some modules
import requests
import json
import time
import os
# try to import the config, else pass, means we run it for the first time
from settings import *
try:
    from config import *
except:
    pass

# Checks if config file is there, else creates it
def check_config():
    # Check if config file is there
    try:
        open("config.py",'r')
    # Else we create it
    except:
        print("No config file found, let's create it!")
        # Get the parameters
        url = input('Enter your nextcloud url: ')
        user = input('Enter your username: ')
        password = input('Enter your password: ')
        # Write parameters to a file
        with open ("config.py",'a') as f:
            f.write(f"#!/usr/bin/python3\nurl = \"{url}/ocs/v2.php/apps/spreed/api/v1\"\nuser = \"{user}\"\npassword = \"{password}\"")
        # TODO: Find way to import the configs without restarting
        print("We need to restart the app now, sorry ;)")
        exit(0)

# Gets the messages
def get_data():
    # Get the users conversations
    r_conversations = requests.get(f"{url}/room", headers=headers, auth=(user, password))
    # Load the json response
    m_conversations = (r_conversations.json())
    # ITerate through the conversations
    for i in range(len(m_conversations["ocs"]["data"])):
        # Get the token
        token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
        # Tet the participants of each chat,TODO: need to hanlde group chats
        r_participants = requests.get(f"{url}/room/{token_i}/participants", headers=headers, auth=(user, password))
        m_participants = (r_participants.json())
        participant_i = (m_participants["ocs"]["data"][1]["displayName"])
        # TODO: Store tokens and participants in a dictionary for later referencing
        # Set some parameters for requesting chat messages, limit to 3 to make it fast for testing
        data_chat = {'lookIntoFuture':0, 'setReadMarker':0, 'limit':3}
        # Get the messages of the chat
        r_messages = requests.get(
            f"{url}/chat/{token_i}",
            headers=headers, auth=(user, password),
            params=data_chat)
        m_messages = (r_messages.json())
        # Iterate through the messages and print them
        for i in range(len(m_messages["ocs"]["data"])):
            # Print participants of chat
            print(f"{participant_i}\n\n")
            # Ptint messages themself
            print(m_messages["ocs"]["data"][i]["message"])
        # Visual indicator for new chat
        print("-----------------------------------------\n-----------------------------------------\n-----------------------------------------\n")
# Send a message to a chat, takes token and msg as arguments
def send_msg(token, msg):
    send = requests.post(f"{url}/chat/{token}", headers=headers, auth=(user, password), params={'message':msg})
