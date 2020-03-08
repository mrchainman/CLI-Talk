#!/usr/bin/python3
from functions import *
if __name__ == "__main__":
    # Clear screen
    os.system('clear')
    # Check the config file
    check_config()
    # Fetch the conversations
    get_conversations()
    # TODO: This nested while loop is ugly, find a better way to handle it
    # Start infinite loop
    while True:
        os.system('clear')
        # Get the list of conversations
        printed_conversations = list_conversations()
        # Get user input of conversation
        user_input = input("Please enter the name of a conversation (type 'q' to exit) : ")
        # Check if we need to break the loop
        if user_input == "q":
            print("Exiting ...")
            break
        conversation = autocomplete(input_string=user_input,choose_from=list_conversations())
        # Start second infinite loop
        while True:
            os.system('clear')
            # Fetch the messages for the given conversation
            get_messages(conversation)
            # Ask for user input
            msg = input("Send message (type 'q' to go back, 'l' to reload the messages) : ")
            # If user typed q, we get back to the conversatins list
            if msg == "q":
                break
            # If user typed l, we refetch the messages
            elif msg == "l":
                # Remove cache file to force refetching of messages
                os.remove(f"{jsondir}/{conversation}.json")
                continue
            # Else we send the message and refetch them, to show the send message
            else:
                send_msg(conversation, msg)
                os.remove(f"{jsondir}/{conversation}.json")
                continue
