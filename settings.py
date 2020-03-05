# Headers
headers = {'OCS-APIRequest': 'true',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
          }
# Set some parameters for requesting chat messages, limit to 3 to make it fast for testing
data_chat = {'lookIntoFuture':0, 'setReadMarker':0, 'limit':3}
dict_token_participant = {}
