""" jsonc as in json with (hash) comments. I picked that format for *.bru
    files because gyp used a similar format: a JSON file with hash comments
    is a valid gyp file. Actually gyp files are a superset of this format, 
    since gyp is Python dictionaries (in fact most gyp files out there used
    ' instead of " for dictionary properties, and most gyp files have trailing
    commas that are illegal in JSON.
"""

import json
import collections
import os

def drop_hash_comment(line):
    """ Getting a line with '#' comment it drops the comment.
        Note that JSON does not support comments, but gyp
        with its JSON-like syntax (really just a Python dict)
        does support comments.
        Should this func be aware of hashes in double quotes?
        Atm it's not.
    """
    hash_index = line.find('#')

    # drops suffix while keeping trailing \n
    def drop_line_suffix(line, index):
      trailing_whitespace = line[len(line.rstrip()):]
      remaining_line = line[0:index]
      return remaining_line + trailing_whitespace

    return line if hash_index == -1 else drop_line_suffix(line,hash_index)


def drop_hash_comments(file):
    """ reads file that can have '<whitespace>#' line comments, dropping
        all comments.
    """
    lines = file.readlines()
    lines_without_comments = (drop_hash_comment(line) for line in lines)
    return "".join(lines_without_comments)

def loadfile(filename):
    """ reads file containing JSON with hash comments.
        Returns dictionaries as OrderedDict to not shuffle key/value pairs
        around during a loadfile/savefile sequence.
    """
    with open(filename) as json_file:
        json_without_hash_comments = drop_hash_comments(json_file)
        try:
            jso = json.loads(json_without_hash_comments,
                                  object_pairs_hook=collections.OrderedDict)
            return jso
        except Exception as err:
            print("error parsing json in {}: {}".format(filename, err))
            print(json_without_hash_comments)
            raise

def savefile(filename, jso):
    """ note this will lose hash comments atm. We could preserve them, is not
        urgent though imo. Does implicit mkdir -p.
        Param jso ('java script object') is a dict or OrderedDict.
        Note that atm this looses all hash comments that were in a previously
        loaded file. Not worth addressing any time soon imo. """
    json_text = json.dumps(jso, indent = 4)
    dirname = os.path.dirname(filename)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as json_file:
        json_file.write(json_text)
        #print("saved " + filename)
