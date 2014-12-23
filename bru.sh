#!/bin/bash

# This autoupdate here is kinda crappy: I want to automatically do a
# 'git pull' of the bru repo everytime bru is being run, mostly to get
# updates of the ./library directory, but I don't want to do a 
# 'git pull' more often than once a day.
# This auto-update would become unnecessary if the ./library content
# was ever migrated to a separate server (corresponding to npmjs.org
# or pypi.python.org), which I don't plan to do anytime soon.
./autoupdate.py --hours 24

# after the autoupdate run bru.py, forwarding all cmd line params
./bru.py $@
