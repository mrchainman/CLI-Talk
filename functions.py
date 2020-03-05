#!/usr/bin/python3
# import some modules
import requests
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
    # Check if we have a cache file
    try:
        with open('conversations.json','r') as lf:
            m_conversations = json.load(lf)
    except:
        # API request
        print("Fetching your conversations ...")
        r_conversations = requests.get(f"{url}/room", headers=headers, auth=(user, password))
        m_conversations = (r_conversations.json())
        with open('conversations.json','w') as df:
            json.dump(m_conversations, df)

    if bool(dict_token_participant) == "False":
        print("Creating dictionary ...")
        number_of_conversations = range(len(m_conversations["ocs"]["data"]))
        for i in number_of_conversations:
            token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
            #TODO: need to hanlde group chats
            r_participants = requests.get(f"{url}/room/{token_i}/participants", headers=headers, auth=(user, password))
            m_participants = (r_participants.json())

            try:
                participant_i = (m_participants["ocs"]["data"][1]["displayName"])
            except:
                # TODO: We need to catch public conversations here, otherwise we get a "Index out of range" error, needs to be fixed.
                participant_i = "public"
            dict_token_participant.update({token_i : participant_i})
        with open('dictionary.json','w') as df:
            json.dump(dict_token_participant, df)

def list_conversations():
    """List the users conversations."""
    print("Youre Conversations:")
    # TODO: We need to sort the conversations by date of last message
    for k, v in dict_token_participant.items():
        print(v)
    print("\n")

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
    try:
        with open('messages.json','r') as lf:
            m_messages = json.load(lf)
    except:
        # API request
        print("Fetching new messages ...")
        r_messages = requests.get( f"{url}/chat/{token}", headers=headers, auth=(user, password), params=data_chat)
        m_messages = (r_messages.json())
        with open('messages.json','w') as df:
            json.dump(m_messages, df)

    print(f"{conversation}:\n")
    number_of_messages = range(len(m_messages["ocs"]["data"]))
    # Iterate through the messages and print them
    for i in reversed(number_of_messages):
        # Ptint messages themself
        print(m_messages["ocs"]["data"][i]["message"])
    print("\n")

def send_msg(conversation, msg):
    """Send a message to a chat, takes conversation and msg as arguments."""
    for key, value in dict_token_participant.items():
        if value == conversation:
            token = key
            break
    send = requests.post(f"{url}/chat/{token}",
                         headers=headers, auth=(user, password),
                         params={'message':msg})
