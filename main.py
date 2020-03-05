#!/usr/bin/python3
from functions import *
if __name__ == "__main__":
    check_config()
    print("Fetching your conversations ...")
    get_conversations()
    # TODO: This nested while loop is ugly, find a better way to handle it
    while True:
        list_conversations()
        conversation = input("Please enter the name of a conversation (type 'quit' to exit) : ")
        if conversation == "quit":
            print("Exiting ...")
            break
        print("Loading messages ...")
        get_messages(conversation)
        while True:
            msg = input("Send message (type 'quit' to exit) : ")
            if msg == "quit":
                break
            send_msg(conversation, msg)
