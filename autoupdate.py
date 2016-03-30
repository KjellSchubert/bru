#!/usr/bin/env python3

import os
import argparse
import time
import subprocess
import pdb

# http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory
def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_timestamp_filename():
    return os.path.join(get_script_path(), 'autoupdate.last')

def get_last_autoupdate_time():
    """ return time.time() param when git pull was run last, None if never """
    if not os.path.exists(get_timestamp_filename()):
        return None
    try:
        with open(get_timestamp_filename(), 'r') as file:
            line = file.readline()
            return float(line)
    except Exception as ex:
        # someone corrupted the file?
        print("WARNING: {} was corrupted? {}".format(get_timestamp_filename(), ex))

def save_autoupdate_time():
    """ param as in time.time() """
    with open(get_timestamp_filename(), 'w') as file:
        file.write(str(time.time()))
        file.write('\n# this file contains the time stamp of the last successful\n'
            'git pull executed by ./autoupdate.py (as time.time())')

def update_now():
    """ assuming this script here lives in a git repo we call git update """
    print("bru/autoupdate.py calling git pull")
    proc = subprocess.Popen(['git', 'pull'], cwd = get_script_path())
    proc.wait()
    returncode = proc.returncode
    if returncode != 0:
        print('ignoring git pull returncode={}, retrying later'.format(returncode))
        return
    save_autoupdate_time()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hours', default=0, type=int,
        help = 'e.g. --hours 12 would run a git pull unless one was already run '
        'within the last 12 hours')
    args = parser.parse_args()

    now = time.time()
    last_autoupdate_time = get_last_autoupdate_time()
    if args.hours > 0 and last_autoupdate_time != None:
        secs_per_hour = 60 * 60
        delta_time_in_hours = (now - last_autoupdate_time) / secs_per_hour
        if delta_time_in_hours < args.hours:
            print("not updating bru yet, last update was {} hours ago"\
                  .format(int(delta_time_in_hours)))
            return

    update_now()

if __name__ == "__main__":
    main()
