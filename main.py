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
        while True:
            print("Loading messages ...")
            get_messages(conversation)
            msg = input("Send message (type 'quit' to exit, 'load' to reload the messages) : ")
            if msg == "quit":
                break
            elif msg == "load":
                continue
            else:
                send_msg(conversation, msg)
