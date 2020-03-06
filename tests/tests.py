#!/usr/bin/python3
#TODO Write some tests
# The Problem is that without a running Nextcloud instance writing tests is difficult
# and I don't want to put the credentials for my instance into the code...
# If somebody has some ideas, just make a PR
import sys
sys.path.append('../bin')
from main import *

# Currently breaks other tests, as direct import is not possible
# def test_create_config():
#     try:
#         import config
#     except:
#         with open ("../bin/config.py",'a') as f:
#             f.write(f"#!/usr/bin/python3\nurl = \"https://cloud.example.com/ocs/v2.php/apps/spreed/api/v1\"\nuser = \"johndoe\"\npassword = \"s3cr3t\"")

def test_import_config():
    import config
    assert len(url) != 0
    assert len(user) != 0
    assert len(password) != 0

# def test_get_conversations():
#     get_conversations()
#     assert r_conversations != 0
