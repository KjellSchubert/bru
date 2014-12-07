#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse # python 2 urlparse
import os
import os.path
import tarfile
import zipfile
import pdb # only if you want to add pdb.set_trace()

class Formula:
    pass

def drop_hash_comment(line):
    """ Getting a line with '#' comment it drops the comment.
        Note that JSON does not support comments, but gyp
        with its JSON-like syntax (really just a Python dict)
        does support comments.
        Should this func be aware of hashes in double quotes?
        Atm it's not.
    """
    hash_index = line.find('#')
    return line if hash_index == -1 else line[hash_index]
    

def drop_hash_comments(file):
    """ reads file that can have '<whitespace>#' line comments, dropping
        all comments.
    """
    lines = file.readlines()
    lines_without_comments = (drop_hash_comment(line) for line in lines)
    return "".join(lines)

def load_formula(module, version):
    """ E.g. to load recipe for module='zlib' version='1.2.8' """
    # Recipes will be downloaded from some server some day (e..g  from github
    # directly).
    with open('library/zlib/1.2.8.bru') as bru_file:
        bru_dict = json.loads(drop_hash_comments(bru_file))
    return bru_dict 

def url2filename(url):
    """ e.g. maps http://zlib.net/zlib-1.2.8.tar.gz to zlib-1.2.8.tar.gz """
    path =  urllib.parse.urlparse(url).path
    return os.path.basename(path)

def wget(url, filename):
    """ typically to download tar.gz or zip """
    # from http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
    print("wget {} -> {}".format(url, filename))
    urllib.request.urlretrieve(url, filename)
    
def extract_file(path, to_directory):
    # from http://code.activestate.com/recipes/576714-extract-a-compressed-file/
    # with slight modifications (without the cwd mess)
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else: 
        raise ValueError("Could not extract {} as no appropriate extractor is found".format(path))
    
    with opener(path, mode) as file:
        file.extractall(to_directory)

def touch(file_name, times=None):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    with open(file_name, 'a'):
        os.utime(file_name, times)

bru_modules_root = "./bru_modules"
os.makedirs(bru_modules_root, exist_ok=True)
module_name = 'zlib'
module_version = '0.2.8'
module_dir = os.path.join(bru_modules_root, module_name, module_version)
os.makedirs(module_dir, exist_ok=True)
formula = load_formula(module_name, module_version)
zip_url = formula['url']
zip_file = os.path.join(module_dir, url2filename(zip_url))
if not os.path.exists(zip_file):
    zip_file_temp = zip_file + ".tmp"
    wget(zip_url, zip_file)
    os.rename(zip_file_temp, zip_file)
extract_done_file = zip_file + ".extract_done"
if not os.path.exists(extract_done_file):
    extract_file(zip_file, module_dir)
    touch(extract_done_file)

# untar