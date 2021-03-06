# CLI-Talk
[![Build Status](https://travis-ci.org/mrchainman/CLI-Talk.svg?branch=master)](https://travis-ci.org/mrchainman/CLI-Talk)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

This program allows you to use Next cloud Talk form the Terminal.

At the moment it only has a text interface, Curses is comming :D

I will continue working on it, every help is appreciated.

## TODO
- [ ] Smaller Todos found as comments in the code
- [x] Fetch messages
- [x] Send messages
- [x] Save the participant-token dictionary to a file to speed up program start times
- [x] Create directories for different files to keep things organised
- [ ] Automatically fetch new conversations and messages periodically
- [ ] We do alot of deleting and recreating cache files, there needs to be a more efficient way
- [ ] Currently credentials are stored in plain text, we need to find a solution for this

## Nice to have
- [ ] Wrap everything into a curses menu
- [ ] Write more tests
- [ ] Bugfixing and testing
- [ ] Make code more "pythonic"

## Usage
If you want to just use the program and not work on it, please download the v1.0-Beta Tag, as the master branch could have bugs while I implement new features.

Run 'pip install -r requirements.txt' to install the needed packages (at the moment there is only 1)

Just run './main.py' from the bin folder.
The first time you will need to configure it through the wizard, then everything will be fetched automatically the next time you run it.

To force recreating cache files, you can just delete the corresponding json file in the cache folder.

Have fun :D
