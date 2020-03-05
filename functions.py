#!/usr/bin/python3
# import some modules
import requests
import json
import time
import os
from variables_and_stuff import *
# try to import the config, else pass, means we run it for the first time
try:
    from config import *
except:
    pass

def check_config():
    """Checks if config file is there, else creates it."""
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
        print("We need to restart the app now, sorry. Just rerunn it and everything will be fine :D")
        exit(0)

def get_conversations():
    """Get the users conversations."""
    # API request
    r_conversations = requests.get(f"{url}/room", headers=headers, auth=(user, password))
    m_conversations = (r_conversations.json())
    # print(m_conversations) #DEBUG CODE
    # exit(0) #DEBUG CODE

    # ITerate through the conversations
    number_of_conversations = range(len(m_conversations["ocs"]["data"]))
    # print(number_of_conversations) # DEBUG CODE
    for i in number_of_conversations:
        # print(i) # DEBUG CODE
        # Get the token
        token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
        # print(token_i) # DEBUG CODE
        # Get the participants of each chat,
        #TODO: need to hanlde group chats
        r_participants = requests.get(f"{url}/room/{token_i}/participants", headers=headers, auth=(user, password))
        m_participants = (r_participants.json())
        try:
            participant_i = (m_participants["ocs"]["data"][1]["displayName"])
        except:
            # TODO: We need to catch public conversations here, otherwise we get a "Index out of range" error, needs to be fixed.
            participant_i = "public"
        # print(participant_i) # DEBUG CODE
        dict_token_participant.update({token_i : participant_i})
    # for k, v in dict_token_participant.items(): # DEBUG CODE
    #     print(k) # DEBUG CODE
    #     print(v) # DEBUG CODE
    # exit(0) # DEBUG CODE

def list_conversations():
    """List the users conversations."""
    print("Youre Conversations:")
    # TODO: We need to sort the conversations by date of last message
    for k, v in dict_token_participant.items():
        print(v)

def get_messages(conversation):
    """Get the messages of a specific conversation. Takes the Displayname of the user in the conversation as an argument"""
    for key, value in dict_token_participant.items():
        if value == conversation:
            token = key
            break
            # print(token) # DEBUG CODE
    else:
        print(f"{conversation} does not exist as a conversation!")

    # Get the messages of the chat
    r_messages = requests.get( f"{url}/chat/{token}", headers=headers, auth=(user, password), params=data_chat)
    m_messages = (r_messages.json())
    print(f"{conversation}\n\n")
    number_of_messages = range(len(m_messages["ocs"]["data"]))
    # Iterate through the messages and print them
    for i in reversed(number_of_messages):
        # Ptint messages themself
        print(m_messages["ocs"]["data"][i]["message"])

def send_msg(conversation, msg):
    """Send a message to a chat, takes conversation and msg as arguments."""
    for key, value in dict_token_participant.items():
        if value == conversation:
            token = key
            break
    send = requests.post(f"{url}/chat/{token}",
                         headers=headers, auth=(user, password),
                         params={'message':msg})
