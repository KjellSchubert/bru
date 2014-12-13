#!/usr/bin/env python3

import json
import itertools
import collections
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

# json (or pythen dicts) with hash comments is what gyp uses alrdy, so I
# made *.bru the same format.
def load_json_with_hash_comments(filename):
    with open(filename) as json_file:
        json_without_hash_comments = drop_hash_comments(json_file)
        try:
            jso = json.loads(json_without_hash_comments,
                                  object_pairs_hook=collections.OrderedDict)
            return jso
        except Exception as err:
            print("error parsing json in {}: {}".format(json_file_name, err))
            print(json_without_hash_comments)
            raise

def save_json(filename, jso):
    """ note this will lose hash comments atm. We could preserve them, is not 
        urgent though imo. Does implicit mkdir -p. 
        Param jso ('java script object') is a dict or OrderedDict """
    dirname = os.path.dirname(filename)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(jso, indent = 4))
        print("saved " + filename)


def load_from_library(module_name, module_version, ext):
    """ ext e.g. '.bru' or '.gyp' """
    json_file_name = os.path.join('./library', module_name, module_version + ext)
    jso = load_json_with_hash_comments(json_file_name)
    return jso

def load_formula(module_name, module_version):
    """ E.g. to load recipe for module_name='zlib' module_version='1.2.8' """
    # Recipes will be downloaded from some server some day (e..g  from github
    # directly).
    formula = load_from_library(module_name, module_version, '.bru')
    assert formula['module'] == module_name and formula['version'] == module_version
    return formula

def load_gyp(formula):
    """ to load the gyp file associated with a formula """
    gyp = load_from_library(formula['module'], formula['version'], '.gyp')
    assert 'targets' in gyp # otherwise it's not a (or is an empty) gyp file
    return gyp

def get_module_dir(formula):
    module_name = formula['module']
    module_version = formula['version']
    module_dir = os.path.join('./library', module_name)
    return module_dir

def save_to_library(formula, jso, ext):
    """ param jso is the dict or OrderedDict to save, which can by the
        forumula itself, or a gyp file, or ... """
    module_version = formula['version']
    module_dir = get_module_dir(formula)
    file_name = os.path.join(module_dir, module_version + ext)
    save_json(file_name, jso)
    #print("not modifying existing " + bru_file_name)


def save_formula(formula):
    """ param formula is the same dict as returned by load_formula,
        so should be an OrderedDict.
    """
    save_to_library(formula, formula, '.bru')

def save_gyp(formula, gyp):
    """ param is a dict representing gyp file content """
    save_to_library(formula, gyp, '.gyp')
    

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
        if match == None:
            raise Exception("expected format **/*.{ext} or **/* for ant: glob expressions, got "
                            + glob_expr)
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

def unpack_module(formula):
    if not 'module' in formula or not 'version' in formula:
        print(json.dumps(formula, indent=4))
        raise Exception('missing module & version')
    module = formula['module']
    version = formula['version']
    zip_url = formula['url']
    return unpack_dependency("./bru_modules", module, version, zip_url)

def get_gyp_dependencies(gyp, formula, resolved_dependencies):
    """ Param gyp is a *.gyp file content, so a dict. 
        Param formula is the formula belonging to the gyp, so a list
        of module deps with desired versions.
        Param resolved_dependencies is a superset of the deps in formula
        with recursively resolved module versions (after resolving conflicts).
    """


def get_dependency(module_name, module_version):
    bru_modules_root = "./bru_modules"
    formula = load_formula(module_name, module_version)
    module_dir = unpack_module(formula)

    # make_command should only be used if we're too lazy to provide a 
    # gyp file for a module.
    if 'make_command' in formula:
        make_command = formula['make_command']
        make_done_file = zip_file + ".make_done"
        if not os.path.exists(make_done_file):
            with Chdir(module_dir):
                # todo: pick a make command depending on host OS
                print("building via '{}' ...".format(make_command))
                error_code = os.system(make_command)
                if error_code != 0:
                    raise ValueError("build failed with error code {}".format(error_code))
            touch(make_done_file)

def compute_resolved_dependencies(formula, resolved_dependencies):
    """ param formula is the formula with a bunch of desired(!) dependencies
        which after conflict resolution across the whole set of diverse deps
        may be required to pull a different version for that module for not
        violate the ODR. But which of course risks not compiling the module
        (but which hopefully will compile & pass tests anyway).
        Param resolved_dependencies is this global modulename-to-version map
        computed across the whole bru.json dependency list.
        Returns the subset of deps for the formula, using the resolved_dependencies
    """
    # so let's project resolved_deps to the subset of deps needed by this
    # formula here:
    if not 'dependencies' in formula:
        return {}  # no deps
    deps = {}
    for module_name in formula['dependencies'].keys():
        assert module_name in resolved_dependencies # otherwise the resolver failed
        resolved_version = resolved_dependencies[module_name]
        deps[module_name] = resolved_version

    # now convert this into the format that *.gyp:dependencies expects:
    # a list of relative paths to gyp files:
    gyp_deps = []
    for module_name, version in deps.items():
        # relative gyp file path should look like "../boost-regex/1.57.0.gyp"
        rel_gypfile_path = os.path.join('..', module_name, version + ".gyp")
        gyp_deps.append(rel_gypfile_path + ":*") # depend on all targets in gyp

    return gyp_deps

def copy_gyp(formula, resolved_dependencies):
    """
        Param resolved_dependencies is a superset of the deps in formula
        with recursively resolved module versions (after resolving conflicts).
    """

    # If the module has a gyp file then let's copy it into ./bru_modules/$module,
    # so next to the unpacked tar.gz, which is where the gyp file's relative 
    # paths expect include_dirs and source files and such.
    # Not all modules need a gyp file, but a gyp file allows specifying upstream
    # module dependencies, whereas a ./configure; make might have easily overlooked
    # dependencies that result in harder-to-reproduce builds (unless you build
    # on only one single machine in your organization).
    # Actually even for modules build via make_command we need a gyp file to 
    # specify include paths and module libs via all|direct_dependent_settings. 
    #
    # Note that the gyp file in the ./library does not contain 'dependencies'
    # property yet, we add this property now (to not have the same redundant deps
    # both in *.bru and *.gyp in the ./library dir)
    module_name = formula['module']
    assert module_name in resolved_dependencies
    resolved_version = resolved_dependencies[module_name]
    rel_gyp_file_path = os.path.join(module_name, resolved_version + ".gyp")
    gyp = load_json_with_hash_comments(os.path.join('library', rel_gyp_file_path))
    gyp_dependencies = compute_resolved_dependencies(
                            formula, resolved_dependencies)
    for target in gyp['targets']:

        if 'dependencies' in target:
            # There should be no such prop in the library/.../*.gyp file.
            print('WARNING: replacing "dependencies" in ', rel_gyp_file_path)

        # 
        target['dependencies'] = gyp_dependencies
        
    save_json(os.path.join('bru_modules', rel_gyp_file_path), gyp)

def resolve_conflicts(dependencies):
    """ takes a dict of modules and version matchers and recursively finds
        all indirect deps. Then resolves version conflicts by picking the newer
        of competing deps, or by picking the version that was requested by the module
        closest to the root of the dependency tree (unsure still).
    """
    root_requestor = 'bru.json'
    todo = [(module, version, root_requestor) for (module, version)
            in dependencies.items()]
    recursive_deps = collections.OrderedDict() 
    for module_name, version_matcher, requestor in todo:
        module_version = version_matcher # todo: allow for npm-style version specs (e.g. '4.*')
        #print('resolving dependency {} version {} requested by {}'
        #      .format(module_name, module_version, requestor))
        if module_name in recursive_deps:
            resolved = recursive_deps[module_name]
            resolved_version = resolved['version']
            if module_version != resolved_version:
                winning_requestor = resolved['requestor']
                print("WARNING: version conflict for {} requested by first {} and then {}"
                      .format(module_name, winning_requestor, requestor))
                # instead of just letting the 2nd and later requestors loose 
                # the competition we could probably do something more sensible.
                # todo?
        else:
            # this is the first time this module was requested, freeze that 
            # chosen version:
            formula = load_formula(module_name, module_version)
            recursive_deps[module_name] = {
                'version' : module_version, 
                'requestor' : requestor
            }

            # then descend deeper into the dependency tree:
            deps = formula['dependencies'] if  'dependencies' in formula else {}
            child_requestor = module_name
            todo += [(child_module, version, child_requestor) 
                     for (child_module, version)
                     in deps.items()]

    return [(module, resolved['version'], resolved['requestor'])
            for (module, resolved) in recursive_deps.items()]

def main():
    with open('bru.json', 'r') as package_file:
        package_jso = json.loads(drop_hash_comments(package_file))
    recursive_deps = resolve_conflicts(package_jso['dependencies'])
    resolved_dependencies = dict((module, version) 
        for (module, version, requestor) in recursive_deps)
    for module_name, module_version, requestor in recursive_deps:
        print('processing dependency {} version {} requested by {}'
              .format(module_name, module_version, requestor))
        formula = load_formula(module_name, module_version)
        get_dependency(module_name, module_version)
        copy_gyp(formula, resolved_dependencies)

    # todo: clean up unused module dependencies from /bru_modules?

if __name__ == "__main__":
    main()
