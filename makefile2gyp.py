#!/usr/bin/env python3
""" run this after
      >cd wherever_your_Makefile_is
      >make -n > make.log
    via
      >./makefile2gyp.py make.log
    which will emit a partial gyp file with sources compiled by this
    Makefile. Afterwards typically ./gyp_sources_intersect.py to merge
    sources for several platforms into one.
    Luckily few modules (e.g. xerces and openssl) require these steps.
"""

import argparse
import os
import re
import json
import pdb

def find_single_match(regex, text):
    """ throw exception if multiple matches """
    match = regex.search(text)
    if match == None:
        return match
    match2 = regex.search(text, match.end())
    if match2 != None:
        raise Exception('multiple matches in {}:\n  match1={}\n  match2={}'
              .format(text, match1.group(), match2.group()))
    return match

def read_make_log(make_logfilename):
    """ reads output of make -n (make sure you generate this output 
        without having a full or partial make before)
    """
    makefile_dir = os.path.dirname(make_logfilename)
    with open(make_logfilename, 'r') as logfile:
        loglines = logfile.readlines()
    files = []
    for line in loglines:

        # this grepping here is brittle, also assumes CXX=clang++
        # to find cpp files
        # This only needs to be good enough for dealing with xerces and
        # openssl make -n output.
        if not (line.find('clang++') != -1 and line.find(' -I') != -1):
            continue
        regex = re.compile(' ([a-zA-Z0-9_\\/]+\\.(cpp|c|cc|cxx))[ ;]')
        match = find_single_match(regex, line)
        if match == None:
            continue
        relpath = match.group(1) # rel to makefile (which is assumed next to make log)
        path = os.path.normpath(os.path.join(makefile_dir, relpath))
        files += [path]

    print(json.dumps({
        'targets': [
            {
                'sources': files
            }
        ]}, sort_keys=True, indent=4))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("make_logfilename", help = "e.g. foo/bar.vcproj")
    args = parser.parse_args()
    read_make_log(args.make_logfilename)

