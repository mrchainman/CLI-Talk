#!/usr/bin/python3
# import some modules
from variables_and_stuff import *
# try to import the config, else pass, means we run it for the first time
try:
    from config import *
except:
    pass

def check_config(debug="False"):
    """
    Checks if config file is there, else creates it.

    The configfile is a .py file which gets imported as a module.
    If it cant be found, it will be created by getting the users input and storing those values in the file.
    The values are: url, user, password.
    By passing debug="True" to the function, it will return wheter the config file was found or needed to be created
    """
    # Check if config file is there
    try:
        open("config.py",'r')
        if debug == "True":
            return 'Found config'
    # Else we create it
    except:
        print("No config file found, let's create it!")
        # Get the parameters
        url = input('Enter your nextcloud url: ')
        user = input('Enter your username: ')
        password = input('Enter your password: ')
        # Write parameters to a file
        with open ("config.py",'a') as f:
            f.write(f"#!/usr/bin/python3\n \
                    url = \"{url}/ocs/v2.php/apps/spreed/api/v1\"\n \
                    user = \"{user}\"\n \
                    password = \"{password}\"")
        # TODO: Find way to import the configs without restarting
        print("We need to restart the app now, sorry. \
              Just rerunn it and everything will be fine :D")
        if debug == "True":
            return 'Needed to create config'
        exit(0)

def get_conversations(debug="False"):
    """
    Get the users conversations.

    Tries to load the conversations list from a json file (cache).
    If the file cannot be found it fetches the conversations through the api and dumps them to a file.
    It will also check if there is a dictionary dict_token_participant stored in a json file.
    This dictionary contains the tokens of conversations as keys and the Displayname as a value.
    If the file does not exist, it creates the dictionary through the api and dumps it to a file.
    If debug="True" is passed as an argument, it returns the conversations in json format.
    """
    # Check if we have a cache file
    try:
        with open(f"{jsondir}/conversations.json",'r') as lf:
            m_conversations = json.load(lf)
    # Else we fetch the conversations and create the cache file
    except:
        print("Fetching your conversations ...")
        r_conversations = requests.get(f"{url}/room", \
                                       headers=headers, \
                                       auth=(user, password))
        m_conversations = (r_conversations.json())
        with open(f"{jsondir}/conversations.json",'w') as df:
            json.dump(m_conversations, df)

    # Check if the dictionary was populated by a cache file,
    # else we create it and write it to a cache file
    if bool(dict_token_participant) == False:
        print("Creating dictionary ...")
        # Get the number of conversations from the json file
        number_of_conversations = range(len(m_conversations["ocs"]["data"]))
        for i in number_of_conversations:
            token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
            # TODO: Read participants from conversations.json instead of making
            # a new request
            #TODO: need to hanlde group chats
            r_participants = requests.get(f"{url}/room/{token_i}/participants",\
                                          headers=headers, \
                                          auth=(user, password))
            m_participants = (r_participants.json())

            # TODO: We need to catch public conversations here, otherwise we get
            # a "Index out of range" error, needs to be fixed.
            try:
                participant_i = (m_participants["ocs"]["data"][1]["displayName"])
            except:
                participant_i = f"Public Conversation {i}"
            dict_token_participant.update({token_i : participant_i})
        # Write the dictionary to a json file for caching
        with open(f"{jsondir}/dictionary.json",'w') as df:
            json.dump(dict_token_participant, df)

    if debug == "True":
        return m_conversations

def list_conversations():
    """
    List the users conversations.

    Creates an empty list called list_of_conversations, than populates it with the tokens and participants from the dict_token_participant dictionary.
    The function returns the list.
    """
    print("Youre Conversations:")
    # TODO: We need to sort the conversations by date of last message
    list_of_conversations = []
    for k, v in dict_token_participant.items():
        print(v)
        list_of_conversations.append(v)
    print("\n")
    return list_of_conversations

def get_messages(conversation):
    """
    Get the messages of a specific conversation.

    The function takes the Displayname of the user in the conversation as an argument.
    It than looks up the corresponding token for the conversation.
    It checkes wheter a file containing the messages already exists, else it fetches them through the api.
    In the end they are printed in reversed order.
    """
    # Find the token for a conversation in the dictionary
    for key, value in dict_token_participant.items():
        if value == conversation:
            token = key
            break
    # Catch error if the conversation does not exist
    else:
        print(f"{conversation} does not exist as a conversation!")

    # Try to read the messages from a cache file
    try:
        with open(f"{jsondir}/{conversation}.json",'r') as lf:
            m_messages = json.load(lf)
    # If there is no cache file, we fetch the messages and create the cache file
    except:
        print(f"Fetching new messages for {conversation}...")
        r_messages = requests.get( f"{url}/chat/{token}", \
                                  headers=headers, \
                                  auth=(user, password), \
                                  params=data_chat)
        m_messages = (r_messages.json())
        with open(f"{jsondir}/{conversation}.json",'w') as df:
            json.dump(m_messages, df)

    print(f"{conversation}:\n")
    # Get the number of messages from the json file
    number_of_messages = range(len(m_messages["ocs"]["data"]))
    for i in reversed(number_of_messages):
        print(m_messages["ocs"]["data"][i]["message"])
    print("\n")

def send_msg(conversation, msg):
    """
    Send a message to a chat.

    The funciton takes the conversation and the message as arguments.
    It looks up the token for the conversation in the dictionary dict_token_participant and send the message through the api.
    """
    # Get the token for a conversation from the dictionary
    for key, value in dict_token_participant.items():
        if value == conversation:
            token = key
            break
    # Send the message
    send = requests.post(f"{url}/chat/{token}",
                         headers=headers, auth=(user, password),
                         params={'message':msg})

def autocomplete(input_string, choose_from):
    """
    Autocomplete a string.

    This functions autocompletes a given string with a list of options.
    The parameters are input_string, which is the input to autocomplete
    and choose_from, which is the list of options.
    """
    filter_input = list(filter(lambda x: x.startswith(input_string), choose_from))
    return filter_input[0]
def autofetch_messages():
    """
    WIP: Autofetch messages periodically

    This function will automatically refetch messages in the background, it is not yet ready.
    """
    for key, value in dict_token_participant.items():
        print(f"Polling token {key} conversation {value}")
        r_autofetch = requests.get( f"{url}/chat/{key}", \
                                   headers=headers, \
                                   auth=(user, password), \
                                   params=data_chat)
        m_autofetch = (r_autofetch.json())
        with open(f"{jsondir}/{value}.json",'w') as df:
            json.dump(m_autofetch, df)
