#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse # python 2 urlparse
import os
import os.path
import tarfile
import zipfile
import glob
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

def load_formula(module, version):
    """ E.g. to load recipe for module='zlib' version='1.2.8' """
    # Recipes will be downloaded from some server some day (e..g  from github
    # directly).
    with open('library/zlib/1.2.8.bru') as bru_file:
        json_without_hash_comments = drop_hash_comments(bru_file)
        #print(json_without_hash_comments)
        bru_dict = json.loads(json_without_hash_comments)
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
        file.close()

def touch(file_name, times=None):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    with open(file_name, 'a'):
        os.utime(file_name, times)

# from http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
class Chdir:         
    """Context manager for changing the current working directory"""
    def __init__( self, newPath ):  
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def main():

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
        wget(zip_url, zip_file_temp)
        os.rename(zip_file_temp, zip_file)

    extract_done_file = zip_file + ".extract_done"
    if not os.path.exists(extract_done_file):
        print("extracting {}".format(zip_file))
        extract_file(zip_file, module_dir)
        touch(extract_done_file)

    # todo: convert into platform-independant make, e.g. via gyp,
    #       or at least call makes on a platform-dependant fashion
    # todo: sanitize make_commands
    make_command = formula['make_command']
    make_done_file = zip_file + ".make_done"
    if not os.path.exists(make_done_file):
        with Chdir(module_dir):
            print("building via '{}' ...".format(make_command))
            error_code = os.system(make_command)
            if error_code != 0:
                raise ValueError("build failed with error code {}".format(error_code))
        touch(make_done_file)

    # now zip up build artifacts: includes, libraries, ...
    artifacts = formula['artifacts']
    for artifact_type, glob_exprs in artifacts.items():
      files = []
      for glob_expr in glob_exprs:
        expr_files = glob.glob(os.path.join(module_dir, glob_expr))
        files += expr_files
      print("artifacts for type={} are {}: ".format(artifact_type, str(files)))
       

if __name__ == "__main__":
    main()
