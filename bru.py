#!/usr/bin/env python3

import json
import itertools
import urllib.request
import urllib.parse # python 2 urlparse
import re
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

def load_bru_file(bru_file_name):
    with open(bru_file_name) as bru_file:
        json_without_hash_comments = drop_hash_comments(bru_file)
        try:
            bru_dict = json.loads(json_without_hash_comments)
        except Exception as err:
            print("error parsing json in {}: {}".format(bru_file_name, err))
            print(json_without_hash_comments)
            raise
    return bru_dict 

def load_formula(module_name, module_version):
    """ E.g. to load recipe for module_name='zlib' module_version='1.2.8' """
    # Recipes will be downloaded from some server some day (e..g  from github
    # directly).
    bru_file_name = os.path.join('./library', module_name, module_version + ".bru")
    return load_bru_file(bru_file_name)

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
    elif path.endswith('.tar.xz') or path.endswith('.txz'):
        opener, mode = tarfile.open, 'r:xz'
    else: 
        raise ValueError("Could not extract {} as no appropriate extractor is found".format(path))
    
    with opener(path, mode) as file:
        file.extractall(to_directory)
        file.close()

class TwoComponentPath:
    """ Used to represent artifacts in tar files, like #include files which
        in the extracted tar are under some root_dir like .../include and
        are named with multiple path comonents underneath, e.g. boost/regex/foo.h
    """

    def __init__(self, root_dir, path):
        self.root_dir = root_dir
        self.path = path
    def get_full_path(self):
        return os.path.join(self.root_dir, self.path)

# See http://stackoverflow.com/questions/161755/how-would-you-implement-ant-style-patternsets-in-python-to-select-groups-of-file
# The drawback of glob.glob("**/*.http") is that it will find hpp files 
# exactly one level deep, unlike an Ant-style fileset include glob which
# searches recursively. A recursive Ant-style glob is more convenient
# to specify filesets of boost #includes for example, so this here
# supports ant-style glob syntax also if you specify a ant:**/*.hpp
# glob_expr.
# Initially I wanted to reuse https://pypi.python.org/pypi/formic but
# this doesn't support python3 yet.
def ant_glob(local_root_dir, glob_expr):
    # we only support a small subset of ant's glob expr syntax: 
    # only **/*.{extension}
    if glob_expr == "**/*":
        is_matching = lambda filename: True
    else:
        match = re.match('^\\*\\*\\/\\*(\\.[a-z0-9_]+)$', glob_expr)
        if match != None:
            raise Exception("expected format **/*.{ext} or **/* for ant: glob expressions")
        extension = match.group(1)  # e.g. '.hpp'
        is_matching = lambda filename: filename.endswith(extension)
    
    # now simply recursively collect files with the given extension under
    # the local_root_dir
    for root, dirs, files in os.walk(local_root_dir):
        for file in files:
            if is_matching(file):
                yield os.path.join(root, file)
    
# Can handle either python-style or ant style glob exprs:
def do_glob(local_root_dir, glob_expr):
    ant_glob_prefix = 'ant:'
    if glob_expr.startswith(ant_glob_prefix):
        expr = glob_expr[len(ant_glob_prefix):]
        return ant_glob(local_root_dir, expr)
    else:
        return glob.glob(os.path.join(local_root_dir, glob_expr))

def get_files_from_glob_exprs(tar_root, glob_exprs):
    """ param glob_exprs is the glob expression pointing to e.g. include
        files in the module's tar file, the glob expr is relative to the
        tar_root dir, which is the dir into which the tar was unpacked.

        Returns pairs of files names: root_dir plus include path, where
        the include path is the file name as it's expected to be used 
        in #include statements, so for example for boost #includes it
        should return pairs ('boost-regex/..../1.57.0', 'boost/regex/foo.hpp')
    """
    files = []
    for glob_expr in glob_exprs:
        local_root_dir = os.path.join(tar_root, glob_expr['local_root_dir'])
        exprs = glob_expr['glob_expr'].split(';') # semi-colon separated
        for expr in exprs:
            matches = do_glob(local_root_dir, expr)
            for match in matches:
                files += [TwoComponentPath(local_root_dir, 
                           os.path.relpath(match, start=local_root_dir))]
    return files

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

class GlobGroup:
    """ represents the mapping of local build files to normalized tar file names
        for a group of one or more files matching a glob expression 
    """
    def __init__(self, local_root_dir, glob_exprs, tar_root_dir):
        assert isinstance(glob_exprs, list) # multiple glob exprs
        self.local_root_dir = local_root_dir
        self.tar_root_dir = tar_root_dir
        self.glob_exprs = glob_exprs


def new_glob_group(glob_group_jso):
    """ argument glob_group_jso has a 'glob' expr as well as other props that
        specify how to tar local files and map them into the tar file.
        This file name mapping is desirable to end up with consistent tar
        files for includes (e.g. containing ./include/boost/regex/foo.h)
        for all the diverse builds we have to run. 
    """
    glob_exprs = glob_group_jso['glob_expr'].split(';')
    local_root_dir = glob_group_jso['local_root_dir'] 
    tar_root_dir = glob_group_jso['tar_root_dir']
    return GlobGroup(local_root_dir, glob_exprs, tar_root_dir)

def tar_glob_group(tar, module_dir, glob_group):
    joined_build_root = os.path.join(module_dir, glob_group.local_root_dir);
    build_file_lists = [
        glob.glob(os.path.join(joined_build_root, glob_expr))
        for glob_expr in glob_group.glob_exprs]
    build_files = list(itertools.chain(*build_file_lists))
    if len(build_files) == 0:
        raise ValueError("no matches for {} in dir {}".format(
          glob_group.glob_exprs,
          joined_build_root))
    for build_file in build_files:
        common_prefix = os.path.commonprefix([build_file, joined_build_root])
        relative_path = os.path.relpath(build_file, common_prefix)
        tar_file = os.path.join(glob_group.tar_root_dir, relative_path)
        print("  adding {}".format(tar_file))
        tar.add(build_file, arcname = tar_file)

def unpack_dependency(bru_modules_root, module_name, module_version, zip_url):
    """ downloads tar.gz or zip file as given by zip_url, then unpacks it
        under bru_modules_root """
    module_dir = os.path.join(bru_modules_root, module_name, module_version)
    os.makedirs(module_dir, exist_ok=True)

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

    return module_dir

def get_dependency(module_name, module_version):

    bru_modules_root = "./bru_modules"
    formula = load_formula(module_name, module_version)

    zip_url = formula['url']
    module_dir = unpack_dependency(bru_modules_root, 
                                   module_name, module_version, zip_url)

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

    # now archive groups of build artifacts: includes, libraries, ...
    artifacts = formula['artifacts']
    for artifact_type, glob_groups in artifacts.items(): # e.g. type='include'
        artifact_tar_file_name = os.path.join(module_dir, artifact_type + ".tar.gz")
        print("writing " + artifact_tar_file_name)
        with tarfile.open(artifact_tar_file_name, "w:gz") as tar:
            for glob_group in glob_groups:
                # each glob group covers a *.h or some such glob expression, with
                # local fs root and tar root in case you want to name the artifact
                # files differently then they end up in the local build.
                tar_glob_group(tar, module_dir, new_glob_group(glob_group))

        # upload tar files to the Artifactory server with enough information to 
        # not violate ODR when linking in the future.
        # todo

def main():
    with open('bru.json', 'r') as package_file:
        package_jso = json.loads(drop_hash_comments(package_file))
    for module_name, version_matcher in package_jso['dependencies'].items():
        module_version = version_matcher # todo: allow for npm-style version specs (e.g. '4.*')
        print('processing dependency {} version {}'.format(module_name, version_matcher))
        get_dependency(module_name, module_version)

if __name__ == "__main__":
    main()
