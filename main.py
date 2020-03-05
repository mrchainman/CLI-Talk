#!/usr/bin/python3
from functions import *
if __name__ == "__main__":
    check_config()
    print("Fetching your conversations ...")
    get_conversations()
    list_conversations()
    conversation = input("Please enter the name of a conversation: ")
    get_messages(conversation)
    while True:
        msg = input("Send: ")
        if msg == "quit":
            print("Bye")
            # TODO: How do we get back tu list_conversations ???
            exit(0)
        send_msg(conversation, msg)
