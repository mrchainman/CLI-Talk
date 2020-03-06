#!/usr/bin/python3
from functions import *
if __name__ == "__main__":
    check_config()
    get_conversations()
    # TODO: This nested while loop is ugly, find a better way to handle it
    while True:
        list_conversations()
        # TODO: Implement autocompletion
        conversation = input("Please enter the name of a conversation (type 'q' to exit) : ")
        if conversation == "q":
            print("Exiting ...")
            break
        while True:
            get_messages(conversation)
            msg = input("Send message (type 'q' to go back, 'l' to reload the messages) : ")
            if msg == "q":
                break
            elif msg == "l":
                # Remove cache file to force refetching of messages
                os.remove(f"{jsondir}/{conversation}.json")
                continue
            else:
                send_msg(conversation, msg)
