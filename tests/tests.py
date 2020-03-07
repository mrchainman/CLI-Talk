#!/usr/bin/python3
#TODO Write some tests
# The Problem is that without a running Nextcloud instance writing tests is difficult
# and I don't want to put the credentials for my instance into the code...
# If somebody has some ideas, just make a PR
import sys
sys.path.append('../bin')
from main import *
from pathlib import Path


# Currently breaks other tests, as direct import is not possible
# def test_create_config():
#     try:
#         import config
#     except:
#         with open ("../bin/config.py",'a') as f:
#             f.write(f"#!/usr/bin/python3\nurl = \"https://cloud.example.com/ocs/v2.php/apps/spreed/api/v1\"\nuser = \"johndoe\"\npassword = \"s3cr3t\"")

configfile = Path("../bin/config.py")

def test_import_config():
    # Only run test if there is a config file, needed as otherwise travis-ci fails
    if configfile.is_file():
        import config
        assert len(url) != 0
        assert len(user) != 0
        assert len(password) != 0

def test_conversations_not_empty():
    # Only run test if there is a config file, needed as otherwise travis-ci fails
    if configfile.is_file():
        import config
        assert get_conversations(debug="True") != 0

def test_dictionary_not_empty():
    # Only run test if there is a config file, needed as otherwise travis-ci fails
    if configfile.is_file():
        import config
        assert list_conversations(debug="True") != 0
