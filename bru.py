#!/usr/bin/env python3

import json
import itertools
import functools
import collections
import urllib.request
import urllib.parse # python 2 urlparse
import re
import os
import os.path
import platform
import tarfile
import zipfile
import shutil
import subprocess
import glob
import time
import argparse
from enum import Enum
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
            print("error parsing json in {}: {}".format(filename, err))
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
        #print("saved " + filename)


def load_from_library(module_name, module_version, ext):
    """ ext e.g. '.bru' or '.gyp' """
    json_file_name = os.path.join(get_library_dir(), module_name, module_version + ext)
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

# http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory
def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_user_home_dir():
    """ work both on Linux & Windows, this dir will be the parent dir of
        the .bru/ dir for storing downloaded tar.gzs on a per-user basis"""
    return os.path.expanduser("~")

def get_library_dir():
    """ assuming we execute bru.py from within its git clone the library
        directory will be located in bru.py's base dir. This func here
        returns the path to this library dir. """
    return os.path.join(get_script_path(), 'library')

def get_module_dir(formula):
    module_name = formula['module']
    module_version = formula['version']
    module_dir = os.path.join(get_library_dir(), module_name)
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

def split_all(path):
    (head, tail) = os.path.split(path)
    if len(head) > 0 and len(tail):
        return split_all(head) + [tail]
    else:
        return [path]

def url2filename(url):
    """ e.g. maps http://zlib.net/zlib-1.2.8.tar.gz to zlib-1.2.8.tar.gz,
        and http://boost.../foo/1.57.0.tgz to foo_1.57.0.tgz"""
    parse = urllib.parse.urlparse(url)
    if parse.scheme == 'file':
        path = parse.netloc
        assert len(path) > 0
        basename = os.path.basename(path)
        assert len(path) > 0
        return basename

    assert parse.scheme in ['http', 'https', 'ftp'] # todo: allow more?
    path =  parse.path
    if path.startswith('/'):
        path = path[1:]
    components = split_all(path)

    # only because of boost's nameing scheme and because modularized boost
    # requires downloading several targzs into the same module dir I set
    # this to 3. Otherwise 1 would be fine. Infinity would be OK also.
    combined_component_count = 5

    return "_".join(components[-combined_component_count:])

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
    # only **/*.{extension} with optional subdirs foo/bar/ before that
    match = re.match('^([^\*]*/)?\*\*/\*(\.[a-z0-9_]+)?$', glob_expr)
    if match == None:
        raise Exception("expected format **/*.{ext} or **/* for ant: glob expressions, got "
                        + glob_expr)
    subdir = match.group(1)
    extension = match.group(2) or '' # e.g. '.hpp'
    is_matching = lambda filename: filename.endswith(extension)
    if subdir != None:
        local_root_dir = os.path.join(local_root_dir, subdir)

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

def unpack_tarfile_once(zip_file, module_dir):
    """ unpacks tar or zip file unless we unpacked it in the past alrdy """
    zip_file_basename = os.path.basename(zip_file)
    assert len(zip_file_basename) > 0
    extract_done_file = os.path.join(module_dir, zip_file_basename + ".unpack_done")
    if not os.path.exists(extract_done_file):
        print("unpacking {}".format(zip_file))
        extract_file(zip_file, module_dir)
        touch(extract_done_file)

def remove_url_prefix(url, prefix):
    """ param prefix e.g. 'git+' """
    assert url.startswith(prefix)
    return url[len(prefix):]

def atomic_clone_repo(repo_url, module_dir, exec_clone):
    """ This executes an svn checkout or a git clone, taking care of the atomic
        rename of the clone to deal with interrupted clones (without implementing
        the svn or git-specific clone itself).
        param module_dir e.g. bru_modules/boost-range, that's where to clone to
        param repo_url is an svn or git url that will be passed to exec_clone()
        param exec_clone is a function which will be passed the intended parent
              dir of the repo clone as well as the checkout url
    """
    svn_root = os.path.join(module_dir, "clone")
    if not os.path.exists(svn_root):
        # atomic rename in case an earlier process run left a half-checkout
        svn_root_temp = svn_root + ".tmp"
        if os.path.exists(svn_root_temp):
            shutil.rmtree(svn_root_temp)
        exec_clone(repo_url, svn_root_temp)
        os.rename(svn_root_temp, svn_root)

def svn_checkout(repo_url, clone_root_dir):
    exit_code = subprocess.call(["svn","checkout", repo_url, clone_root_dir])
    assert exit_code == 0, "do you have subversion 'svn' installed and in your path?"

def split_off_changeset(repo_url):
    """ splits http://foo.com/bar@xyz into tuple (http://foo.com/bar, xyz),
        with the 2nd tuple elem being None if there's no '@' in the URL """
    parse = urllib.parse.urlparse(repo_url)
    at_index = parse.path.rfind('@')
    if at_index != -1:
        changeset_len = len(parse.path) - at_index # includes '@'
        assert repo_url[-changeset_len] == '@'
        url_prefix = repo_url[:-changeset_len]
        changeset = repo_url[-changeset_len+1:]
        assert repo_url == url_prefix + '@' + changeset
    else:
        url_prefix = repo_url
        changeset = None
    return (url_prefix, changeset)

def git_clone(repo_url, clone_root_dir):
    # if repo_url ends with @... then consider the portion of the @
    # the branch or changeset that should be checked out.
    (repo_url, changeset) = split_off_changeset(repo_url)
    print("git clone", repo_url)
    cmdline = ["git","clone", repo_url, clone_root_dir]
    exit_code = subprocess.call(cmdline)
    assert exit_code == 0, "do you have subversion 'svn' installed and in your path?"
    if changeset != None:
        print("git checkout", changeset)
        proc = subprocess.Popen(['git', 'checkout', changeset], 
                                  cwd = clone_root_dir)
        proc.wait()
        exit_code = proc.returncode
        assert exit_code == 0, "git checkout returned error {}".format(exit_code)

def unpack_dependency(bru_modules_root, module_name, module_version, zip_url):
    """ downloads tar.gz or zip file as given by zip_url, then unpacks it
        under bru_modules_root """
    src_module_dir = os.path.join(get_library_dir(), module_name)
    module_dir = os.path.join(bru_modules_root, module_name, module_version)
    os.makedirs(module_dir, exist_ok=True)

    parse = urllib.parse.urlparse(zip_url)
    if parse.scheme in ['svn+http', 'svn+https']:
        repo_url = remove_url_prefix(zip_url, 'svn+')
        atomic_clone_repo(repo_url, module_dir, svn_checkout)
        return

    if parse.scheme in ['git+http', 'git+https']:
        repo_url = remove_url_prefix(zip_url, 'git+')
        atomic_clone_repo(repo_url, module_dir, git_clone)
        return

    if parse.scheme == 'file':
        # this is typically used to apply a patch in the form of a targ.gz
        # on top of a larger downloaded file. E.g. for ogg & speex this
        # patch does approximately what ./configure would have done.
        # copying the tar file itself from ./library to ./modules would be
        # pointless, so we extract this file right from the library dir:
        path = parse.netloc
        assert len(path) > 0
        basename = os.path.basename(path)
        assert len(path) > 0
        src_tar_filename = os.path.join(src_module_dir, path)
        unpack_tarfile_once(src_tar_filename, module_dir)
        return

    # Store all downloaded tar.gz files in ~/.bru, e.g as boost-regex/1.57/foo.tar.gz
    # This ensures that multiple 'bru install foo' cmds in differet directories
    # on this machine won't download the same foo.tar.gz multiple times.
    # MOdules for which we must clone an svn or git repo are not sharable that
    # easily btw, they actually are cloned multiple times atm (could clone them
    # once into ~/.bru and copy, but I'm not doing this atm).
    if parse.scheme in ['http', 'https', 'ftp']:
        tar_dir = os.path.join(get_user_home_dir(), ".bru", "downloads",
                               module_name, module_version)
        zip_file = os.path.join(tar_dir, url2filename(zip_url))
        if not os.path.exists(zip_file):
            os.makedirs(tar_dir, exist_ok=True)
            zip_file_temp = zip_file + ".tmp"
            wget(zip_url, zip_file_temp)
            os.rename(zip_file_temp, zip_file)

        unpack_tarfile_once(zip_file, module_dir)
        return

    raise Exception('unsupported scheme in', zip_url)

def unpack_module(formula):
    if not 'module' in formula or not 'version' in formula:
        print(json.dumps(formula, indent=4))
        raise Exception('missing module & version')
    module = formula['module']
    version = formula['version']
    zip_urls = formula['url']

    # 'url' can be a single string or a list
    if isinstance(zip_urls, str):
        zip_urls = [zip_urls]

    bru_modules_root = './bru_modules'
    for zip_url in zip_urls:
        unpack_dependency(bru_modules_root, module, version, zip_url)
    module_dir = os.path.join(bru_modules_root, module, module)
    return module_dir

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
    unpack_module(formula)

    # make_command should only be used if we're too lazy to provide a
    # gyp file for a module.
    # A drawback of using ./configure make is that build are less reproducible
    # across machines, e.g. ./configure may enable some code paths on one
    # machine but not another depending on which libs are installed on both
    # machines.
    if 'make_command' in formula:
        module_dir = os.path.join(bru_modules_root, module_name, module_version)
        make_done_file = os.path.join(module_dir, "make_command.done")
        if not os.path.exists(make_done_file):
            make_commands = formula['make_command']
            system = platform.system()
            if not system in make_commands:
                raise Exception("no key {} in make_command".format(system))
            make_command = make_commands[system]
            with Chdir(module_dir):
                # todo: pick a make command depending on host OS
                print("building via '{}' ...".format(make_command))
                error_code = os.system(make_command)
                if error_code != 0:
                    raise ValueError("build failed with error code {}".format(error_code))
            touch(make_done_file)

def verify_resolved_dependencies(formula, target, resolved_dependencies):
    """ param formula is the formula with a bunch of desired(!) dependencies
        which after conflict resolution across the whole set of diverse deps
        may be required to pull a different version for that module for not
        violate the ODR. But which of course risks not compiling the module
        (but which hopefully will compile & pass tests anyway).
        Param resolved_dependencies is this global modulename-to-version map
        computed across the whole bru.json dependency list.
        Returns the subset of deps for the formula, using the resolved_dependencies
    """

    # this here's the module we want to resolve deps for now:
    module = formula['module']
    version = formula['version']

    # iterate over all target and their deps, fill in resolved versions
    target_name = target['target_name']
    resolved_target_deps = []

    def map_dependency(dep):
        """ param dep is a gyp file dependency, so either a local dep to a local
            target like 'zlib' or a cross-module dep like '../boost-regex/...'.
            There should be no other kinds of gyp deps in use """

        # detect the regexes as written by scan_deps.py: references into
        # a sibling module within ./bru_modules.
        bru_regex = "^../([^/]+)/([^/]+)\\.gyp:(.+)"
        match = re.match(bru_regex, dep)
        if match == None:
            return dep
        upstream_module = match.group(1)
        upstream_targets = match.group(2)
        if not upstream_module in resolved_dependencies:
            raise Exception("module {} listed in {}/{}.gyp's target '{}'"
                " not found. Add it to {}/{}.bru:dependencies"
                .format(
                    upstream_module, module, version, target_name,
                    module, version
                ))
        return resolved_dependencies[upstream_module]
    return list(map(map_dependency, target['dependencies']))

def compute_sources(formula, target):
    """ gyp does not support glob expression or wildcards in 'sources', this
        here turns these glob expressions into a list of source files
    """
    def is_glob_expr(source):
        return '*' in source or source.startswith('ant:')
    sources = []
    gyp_target_dir = os.path.join('bru_modules', formula['module']) # that is
        # the dir the gyp file for this module is being stored in, so paths
        # in the gyp file are interpreted relative to that
    for source in target['sources']:
        if is_glob_expr(source):
            matching_sources = [os.path.relpath(filename, start=gyp_target_dir)
                                for filename in
                                do_glob(gyp_target_dir, source)]
            assert len(matching_sources) > 0, "no matches for glob " + source
            sources += matching_sources
        else:
            # source os a flat file name (relative to gyp parent dir)
            sources.append(source)
    return list(sorted(sources))

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
    gyp = load_json_with_hash_comments(os.path.join(get_library_dir(), rel_gyp_file_path))
    for target in gyp['targets']:

        if 'dependencies' in target:
            # Initially I thought there should be no such prop in the
            # library/.../*.gyp file because these deps will be filled in with
            # resolved deps from the *.bru file. But then I ran into two
            # problems:
            #   a) I wanted for example zlib tests to build via gyp also
            #      (espcially since zlib is being built via gyp target alrdy
            #      anyway), so the gyp test target should depend on the lib
            #      target.
            #   b) often test targets need to pull in additional module deps
            #      that the module (without its tests) does not depend on, for
            #      example tests often depend on googletest or googlemock,
            #      whereas the main module does not.
            # So now a *.bru file lists the union of dependencies for all
            # targets in a gyp file, while each target depends explicitly
            # lists dependencies as "bru:googletest". Could also support a
            # format like "bru:googletest:1.7.0" but then the *.gyp file
            # and *.bru file dependency lists would be redundant. Todo: move
            # dependency lists from *.bru to *.gyp file altogether? Maybe...
            verify_resolved_dependencies(formula, target, resolved_dependencies)

        # Sanity check: verify the 'sources' prop doesn't contain glob exprs
        # or wildcards: initially I though gyp was ok with
        #    "sources" : ".../src/*.cc"
        # in *.gyp files because at first glance this 'compiled', but it
        # turned out gyp just silently compiled zero source files in that case.
        #
        # Alternatively we could expand these wildcards now, drawback of that
        # is that the files in ./library are not really *.gyp files anymore,
        # and should probably be called *.gyp.in or *.gyp-bru or something
        # like that.
        if 'sources' in target:
            target['sources'] = compute_sources(formula, target)

    # note that library/boost-regex/1.57.0.gyp is being copied to
    # bru_modules/boost-regex/boost-regex.gyp here (with some minor
    # transformations that were applied, e.g. expanding wildcards)
    gyp_target_file = os.path.join('bru_modules', module_name, module_name + ".gyp")

    # We also need a certain set of MSVC options imported into gyp files
    # and don't want to repeat the same boring MSVC settings in every single
    # module's individual gyp file. So add common.gypi include unless
    # the module's gyp file explicitly specifies includes already.
    if not 'includes' in gyp:
        # we want the 'includes' at the begin, to achieve this order see
        # http://stackoverflow.com/questions/16664874/how-can-i-add-the-element-at-the-top-of-ordereddict-in-python
        new_gyp = collections.OrderedDict()
        new_gyp['includes'] = ['../../bru_common.gypi']
        for key, value in gyp.items():
            new_gyp[key] = value
        gyp = new_gyp

    save_json(gyp_target_file, gyp)

    # this file is only saved for human reader's sake atm:
    save_json(os.path.join('bru_modules', module_name, 'bru-version.json'),
        {'version': resolved_version})

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

def get_all_versions(library_path, module):
    bru_file_names = os.listdir(os.path.join(library_path, module))
    regex = re.compile('^(.+)\\.bru$') # version can be 1.2.3 or 1.2rc7 or ...
    for bru_file_name in bru_file_names:
        match = regex.match(bru_file_name)
        if match != None:
            version = match.group(1)
            yield version

def alphnumeric_lt(a, b):
    # from http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    def to_alphanumeric_pairs(text):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return alphanum_key(text)
    pdb.set_trace()
    return to_alphanumeric_pairs(a) < to_alphanumeric_pairs(b)

@functools.total_ordering
class ModuleVersion:
    def __init__(self, version_text):
        self.version_text = version_text
    def __lt__(self, other):
        lhs = self .version_text
        rhs = other.version_text
        # module versions could be straightforward like 1.2.3, or they could be
        # openssl-style mixtures of numberrs & letters like 1.0.0f
        return alphnumeric_lt(lhs, rhs)

def get_latest_version_of(module):
    versions = get_all_versions(get_library_dir(), module)
    return max((ModuleVersion(version_text) for version_text in versions)).version_text

def get_single_bru_file(dir):
    """ return None of no *.bru file in this dir """
    matches = glob.glob("*.bru")
    if len(matches) == 0:
        return None
    if len(matches) > 1:
        raise Exception("there are multiple *.bru files in {}: {}".format(
              dir, matches))
    return os.path.join(dir, matches[0])

def get_or_create_single_bru_file(dir):
    """ returns single *.bru file from given dir or creates an empty
        package.bru file (corresponding to package.json for npm).
        So unlike get_single_bru_file() never returns None.
    """
    bru_file = get_single_bru_file(dir)
    if bru_file == None:
        bru_file = os.path.join(dir, 'package.bru')
        save_json(bru_file, {'dependencies':{}})
        print('created ', bru_file)
    assert bru_file != None
    return bru_file

def parse_module_at_version(installable):
    """ parses 'googlemock@1.7.0' into tuple (module, version),
        and returns (module, None) for input lacking the @version suffix.
    """
    elems = installable.split('@')
    if len(elems) == 1:
        return Installable(elems[0], None)
    if len(elems) == 2:
        return Installable(elems[0], elems[1])
    raise Exception("expected module@version but got {}".format(installable))

def parse_existing_module_at_version(installable):
    """ like parse_module_at_version but returns the latest version if version
        was unspecified. Also verifies module at version actually exist
        in ./library.
    """
    installable = parse_module_at_version(installable)
    module = installable.module
    version = installable.version
    if not os.path.exists(os.path.join(get_library_dir(), module)):
        raise Exception("no module {} in {}, may want to 'git pull'"\
              " if this module was added very recently".format(
              module, get_library_dir()))
    if version == None:
        version = get_latest_version_of(module)
    if not os.path.exists(os.path.join(get_library_dir(), module)):
        raise Exception("no version {} in {}/{}, may want to 'git pull'"\
              " if this version was added very recently".format(
              version, get_library_dir(), module))
    assert version != None
    return Installable(module, version)

def add_dependencies_to_bru(bru_filename, installables):
    bru = load_json_with_hash_comments(bru_filename)
    if not 'dependencies' in bru:
        bru['dependencies'] = {}
    deps = bru['dependencies']
    for installable in installables:
        deps[installable.module] = installable.version
    save_json(bru_filename, bru) # warning: this nukes comments atm

def add_dependencies_to_gyp(gyp_filename, installables):
    gyp = load_json_with_hash_comments(gyp_filename)
    # typically a gyp file has multiple targets, e.g. a static_library and
    # one or more test executables. Here we add the new dep to only the first
    # target in the gyp file, which is somewhat arbitrary. TODO: revise.
    # Until then end user can always shuffle around dependencies as needed
    # between targets.
    if not 'targets' in gyp:
        gyp['targets'] = []
    targets = gyp['targets']
    if len(targets) == 0:
        targets[0] = {}
    first_target = targets[0]
    if not 'dependencies' in first_target:
        first_target['dependencies'] = []
    deps = first_target['dependencies']
    for installable in installables:
        module = installable.module
        dep_gyp_path = "bru_modules/{}/{}.gyp".format(module, module)
        dep_expr = dep_gyp_path + ":*" # depend on all targets, incl tests
        if not dep_expr in deps:
            deps.append(dep_expr)
    save_json(gyp_filename, gyp) # warning: this nukes comments atm

def create_gyp_file(gyp_filename):
    """ creates enough of a gyp file so that we can record dependencies """
    if os.path.exists(gyp_filename):
        raise Exception('{} already exists'.format(gyp_filename))
    gyp = collections.OrderedDict([
        ("includes", ["bru_common.gypi"]),
        ("targets", [
            collections.OrderedDict([
                ("target_name", "foo"), # just a guess, user should rename
                ("type", "none"), # more likely 'static_library' or 'executable'

                # these two props are going to have to be filled in by enduser
                ("sources", []),
                ("includes_dirs", []),

                ("dependencies", [])
        ])])
    ])
    save_json(gyp_filename, gyp)

class Installable:
    def __init__(self, module, version):
        self.module = module
        self.version = version

def cmd_install(installables):
    """ param installables: e.g. [] or ['googlemock@1.7.0', 'boost-regex']
        This is supposed to mimic 'npm install' syntax, see
        https://docs.npmjs.com/cli/install. Examples:
          a) bru install googlemock@1.7.0
          b) bru install googlemock
          c) bru install
        Variant (a) is self-explanatory, installing the module of the given
        version. Variant (b) installs the latest known version of the module
        as specified by the versions listed in bru/library/googlemock.
        Variant (c) will install all dependencies listed in the local *.bru
        file (similar as how 'npm install' install all deps from ./package.json).
        Unlike for 'npm install' the option --save is implied, means whatever you
        install will end up in the local *.bru file's "dependencies" list, as
        well as in the companion *.gyp file.
    """
    if len(installables) == 0:
        # 'bru install'
        bru_filename = get_single_bru_file(os.getcwd())
        if bru_filename == None:
            raise Exception("no file *.bru in cwd")
        print('installing dependencies listed in', bru_filename)
        install_from_bru_file(bru_filename)
    else:
        # installables are ['googlemock', 'googlemock@1.7.0']
        installables = [parse_existing_module_at_version(installable)
                        for installable in installables]
        bru_filename = get_or_create_single_bru_file(os.getcwd())
        gyp_filename = bru_filename[:-3] + 'gyp'
        if not os.path.exists(gyp_filename):
            create_gyp_file(gyp_filename)
        add_dependencies_to_bru(bru_filename, installables)
        add_dependencies_to_gyp(gyp_filename, installables)
        for installable in installables:
            print("added dependency {}@{} to {} and {}".format(
                installable.module, installable.version,
                bru_filename, gyp_filename))
        # now download the new dependency just like 'bru install' would do
        # after we added the dep to the bru & gyp file:
        install_from_bru_file(bru_filename)

def install_from_bru_file(bru_filename):
    with open(bru_filename, 'r') as package_file:
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

    # copy common.gypi which is referenced by module.gyp files and usually
    # also by the parent *.gyp (e.g. bru-sample:foo.gyp).
    # Should end users be allowed to make changes to bru_common.gypi or
    # should they rather edit their own optional common.gpyi which shadows
    # bru_common.gypi? Unsure, let them edit for now, so dont overwrite gypi.
    common_gypi = 'bru_common.gypi'
    if not os.path.exists(common_gypi):
        print('copying', common_gypi)
        shutil.copyfile(
            os.path.join(get_script_path(), common_gypi),
            common_gypi)

    #for module, version, requestor in recursive_deps:
    #    for ext in ['bru', 'gyp']:
    #        print("git add -f library/{}/{}.{}".format(module, version, ext))


    # todo: clean up unused module dependencies from /bru_modules?

def get_test_targets(gyp):
    """ returns the subset of gyp targets that are tests """

    # Each module typically declares a static lib (usually one, sometimes
    # several), as well as one or more tests, and in rare cases additional
    # executables, e.g. as utilities.
    # How can we tell which of the targets are tests? Heuristically static libs
    # cannot be tests, executables usually but not always are. What many tests
    # still need though is a cwd at startup (e.g. to find test data), which
    # differs from module to module. Let's add this test/cwd property to the
    # gyp target, gyp will ignore such additional props silently. This test/cwd
    # is interpreted relative to the gyp file (like any other path in a gyp file).
    targets = gyp['targets']
    for target in targets:
        if 'test' in target:
            yield target

class TestResult(Enum):
    fail = 0
    success = 1
    notrun = 2 # e.g. not run because executable wasnt built or wasnt found

class CompletedTestRun:
    def __init__(self, target_name, test_result):
        """ param test is a gyp target name for given module, e.g. 'googlemock_test'
            param result is a test result
            param result is of type TestResult
        """
        self.target_name = target_name
        self.test_result = test_result
        self.module = None
        self.duration_in_ms = -1 # -1 means test wasnt run yet

def locate_executable(target_name):
    """ return None if it (likely) wasnt built yet (or if for some other reason
        we cannot determine where the executable was put by whatever toolchain
        gyp was triggering.
        Otherwise return relative path to executable.
    """
    for config in ['Release', 'Debug']:
        candidates = [
            os.path.join('out', config, target_name),
            os.path.join('out', config, target_name + '.exe'),
            os.path.join(config, target_name),
            os.path.join(config, target_name + '.exe')]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
    return None

def exec_test(gypdir, target):
    """ runs test (if executable was built) and returns an instance of
        CompletedTestRun.
        param gypdir is the location of the gyp file
        param target is a 'target' node from a gyp file, so a dict with
              keys like gyp's 'target_name' and the bru-specific 'test'
    """

    # Now knowing the target we have the following problems:
    # * where is the compiled target executable located? E.g. on Ubuntu
    #   with make I find it in out/Release/googlemock_test but on Windows
    #   with msvs it ends in Release/googlemock_test.exe
    # * run Debug or Release or some other config? Let's run Release only
    #   for now. TODO: make configurable, or use Release-Debug fallback?
    #   Or run whichever was built last?
    target_name = target['target_name']
    exe_path = locate_executable(target_name)
    if exe_path != None:
        print('running', target_name)
        t0 = time.time() # or clock()?
        test = target['test']
        rel_cwd = test['cwd'] if 'cwd' in test else './'
        test_argv = test['args'] if 'args' in test else []
        proc = subprocess.Popen([os.path.abspath(exe_path)] + test_argv,
                                cwd = os.path.join(gypdir, rel_cwd))
        proc.wait()
        returncode = proc.returncode
        duration_in_ms = int(1000 * (time.time() - t0))
        print(target_name, 'returned with exit code', returncode, 'after',
            duration_in_ms, 'ms')
        testrun = CompletedTestRun(target_name,
            TestResult.success if returncode == 0 else TestResult.fail)
        testrun.duration_in_ms = duration_in_ms
        return testrun
    else:
        print('cannot find executable', target_name)
        return CompletedTestRun(target_name, TestResult.notrun)

def collect_tests(module_names):
    """ yields tuples (module, gypdir, test_target), where gypdir is the
        directory the *gyp file is located in (since all file paths in the
        gyp - e.g. the test.cwd - are relative to that particular dir """
    modules_dir = 'bru_modules'
    for module in module_names:
        gypdir = os.path.join(modules_dir, module)
        gyp = load_json_with_hash_comments(os.path.join(
                gypdir, module + ".gyp"))
        test_targets = get_test_targets(gyp)
        for test_target in test_targets:
            yield (module, gypdir, test_target)

def cmd_test(testables):
    """ param testables is list of module names, empty to test all modules
    """

    # You alrdy can run tests for upstream deps via these cmds, here
    # for example for running zlib tests:
    #   >bru install
    #   >cd bru_modules/zlib
    #   >gyp *.gyp --depth=.
    #   >make
    #   >out/Default/zlib_test
    # This command here is supposed to automate these steps: you can run these
    # commands here:
    #   >bru test  # runs tests for all modules in ./bru_modules
    #   >bru test boost-regex  # runs tests for given modules only

    modules_dir = 'bru_modules'
    if len(testables) == 0:
        for gyp_filename in glob.glob(os.path.join(modules_dir, '**', '*.gyp')):
            module_dir = os.path.dirname(gyp_filename)
            _, module = os.path.split(module_dir)
            testables.append(module)

    # first let's check if all tests were built already, if they weren't then
    # we'll do an implicit 'bru make' before running tests
    def did_all_builds_complete(testables):
        for module, gypdir, target in collect_tests(testables):
            target_name = target['target_name']
            if locate_executable(target_name) == None:
                print("executable for {}:{} not found".format(
                    module, target_name))
                return False
        return True
    if not did_all_builds_complete(testables):
        print("running 'bru make':")
        cmd_make()

    testruns = []
    module2test_count = dict((module, 0) for module in testables)
    for module, gypdir, target in collect_tests(testables):
        testrun = exec_test(gypdir, target)
        testrun.module = module
        testruns.append(testrun)
        module2test_count[module] += 1
        
    # for modules that don't have tests defined yet strive for adding
    # some tests, warn/inform the user about these modules here:
    modules_without_tests = [module 
                for (module, test_count) in module2test_count.items()
                if test_count == 0]

    # also partition/group testruns by test result:                
    testgroups = {} # testresult to list of testruns, so partitioned testruns
    for test_result, runs in itertools.groupby(testruns,
                             lambda testrun: testrun.test_result):
        testgroups[test_result] = list(runs)

    def get_test_group(test_result):
        return testgroups[test_result] if test_result in testgroups else []

    def print_test_group(msg, test_result):
        testgroup = list(get_test_group(test_result))
        if len(testgroup) > 0:
            print(msg.format(len(testgroup)))
            for testrun in testgroup:
                line = '  {}:{}'.format(testrun.module, testrun.target_name)
                if testrun.duration_in_ms >= 0:
                    line += ' after {} ms'.format(testrun.duration_in_ms)
                print(line)
        return len(testgroup)

    print("test summary:")
    if len(modules_without_tests) > 0:
        print('warning: the following modules have no tests configured:')
        for module in sorted(modules_without_tests):
            print('  ', module)
    successful_test_count = print_test_group(
        'The following {} tests succeeded:', 
        TestResult.success)
    missing_test_count = print_test_group(
        'The following {} tests are missing (build failed?):', 
        TestResult.notrun)
    failed_test_count = print_test_group(
        'The following {} tests failed:', 
        TestResult.fail)
    if missing_test_count > 0 or failed_test_count > 0:
        raise Exception('ERROR: {} tests failed and {} tests failed building'\
                        .format(failed_test_count, missing_test_count))
    print('All {} tests successful.'.format(successful_test_count))

def cmd_make():
    """ this command makes some educated guesses about which toolchain
        the user probably wants to run, then invokes gyp to create the
        makefiles for this toolchain and invokes the build. On Linux
        'bru make' is likely equivalent to:
           >gyp *gyp --depth=.
           >make
        On Windows it's likely equivalent to:
           >gyp --depth=. package.gyp -G msvs_version=2012
           >C:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild.exe package.sln
        The main purpose of 'bru make' is really to spit out these two
        command lines as a quick reminder for how to build via cmd line.
    """

    # first locate the single gyp in the cwd
    bru_file = get_single_bru_file('.')
    if bru_file == None:
        raise Exception("there's no *.bru file in current work dir, "
            'e.g. run "bru install googlemock" first to create one')
    gyp_file = bru_file[:-3] + 'gyp'
    if not os.path.exists(gyp_file):
        raise Exception(bru_file,'has no companion *.gyp file, '
            'e.g. recreate one via "bru install googlemock"')

    system = platform.system()
    if system == 'Windows':
        cmd_make_win(gyp_file)
    elif system == 'Linux':
        cmd_make_linux(gyp_file)
    else:
        raise Exception('no idea how to invoke gyp & toolchain on platform {}'\
            .format(system))

def get_latest_msbuild_exe():
    """ return path to latest msbuild on Windows machine """
    env = os.environ
    windir = env['SystemRoot'] if 'SystemRoot' in env else env['windir']
    glob_expr = os.path.join(windir, 'Microsoft.NET', 'Framework',
        '**', 'msbuild.exe')
    msbuilds = glob.glob(glob_expr)
    return max(msbuilds)  # not alphanumeric, should be good enough tho

def get_latest_msvs_version():
    """ e.g. return 2012 (aka VC11) if msvs 2012 is installed. If multiple
        vs versions are installed then pick latest.
        Return None if no installs are found?
    """
    # whats a good way to detect the msvs version?
    # a) scan for install dirs like
    #    c:\Program Files (x86)\Microsoft Visual Studio 10.0
    # b) scan for env vars like VS110COMNTOOLS
    # Let's do (b) for now.
    # See also https://code.google.com/p/gyp/source/browse/trunk/pylib/gyp/MSVSVersion.py
    msvs_versions = []
    regex = re.compile('^VS([0-10]+)COMNTOOLS$')
    for key in os.environ:
        match = regex.match(key)
        if match != None:
            msvs_versions.append(int(match.group(1)))
    if len(msvs_versions) == 0:
        return None
    latest = max(msvs_versions) # e.g. 110
    if len(msvs_versions) > 1:
        print('detected installs of msvs {}, choosing latest {}'.format(
            msvs_versions, latest))
    msvs_version2year = {
        80: 2005,
        90: 2008,
        100: 2010,
        110: 2012,
    }
    if not latest in msvs_version2year:
        print('not sure how to map VC{} to a VS year, defaulting to VS 2012'
            .format(latest))
        return 2012
    return msvs_version2year[latest]

def run_gyp(gyp_cmdline):
    print('running >', gyp_cmdline)
    returncode = os.system(gyp_cmdline)
    if returncode != 0:
        raise Exception('error running gyp, did you install it?'
            ' Instructions at https://github.com/KjellSchubert/bru')

def cmd_make_win(gyp_filename):
    # TODO: locate msvs version via glob
    msvs_version = get_latest_msvs_version()
    if msvs_version == None:
        print('WARNING: no msvs installation detected, did you install it? '
            'Defaulting to msvs 2012.')
    gyp_cmdline = 'gyp --depth=. {} -G msvs_version={}'.format(
        gyp_filename, msvs_version)
    run_gyp(gyp_cmdline)
    # gyp should have created a *.sln file, verify that.
    # if it didnt that pass a msvc generator option to gyp in a more explicit
    # fashion (is -G msvs_version enough? need GYP_GENERATORS=msvs?).
    sln_filename = gyp_filename[:-3] + 'sln'
    if not os.path.exists(sln_filename):
        raise Exception('gyp unexpectedly did not generate a *.sln file, '
            'you may wanna invoke gyp manually to generate the expected '
            'make/sln/ninja files, e.g. set GYP_GENERATORS=msvs')

    # there are many ways to build the *.sln now, e.g. pass it to devenv
    # or alternatively to msbuild. Lets do msbuild here:
    # TODO locate msbuild via glob
    msbuild_exe = get_latest_msbuild_exe()
    if msbuild_exe == None:
        raise Exception('did not detect any installs of msbuild, these should'
            ' be part of .NET installations, please install msbuild or .NET')
    config = 'Release'
    msbuild_cmdline = '{} {} /p:Configuration={}'.format(
        msbuild_exe, sln_filename, config)
    print('running msvs via msbuild >', msbuild_cmdline)
    returncode = os.system(msbuild_cmdline)
    if returncode != 0:
        raise Exception('msbuild failed with errors, returncode =', returncode)
    print('Build complete.')

def cmd_make_linux(gyp_filename):
    # Here we could check if ninja or some such is installed to generate ninja
    # project files. But for simplicity's sake let's just use whatever gyp
    # defaults to.

    # For some odd reason passing './package.gyp' as a param to gyp will 
    # generate garbage, instead you gotta pass 'package.gyp'. Se let's 
    # explicitly remove a leading ./
    dirname = os.path.dirname(gyp_filename)
    assert dirname == '.' or len(dirname) == 0
    gyp_filename = os.path.basename(gyp_filename)
    
    gyp_cmdline = 'gyp --depth=. {}'.format(gyp_filename)
    run_gyp(gyp_cmdline)
    if not os.path.exists('Makefile'):
        raise Exception('gyp did not generate ./Makefile, no idea how to '
            'build with your toolchain, please build manually')
    returncode = os.system('make')
    if returncode != 0:
        raise Exception('Build failed: make returned', returncode)
    print('Build complete.')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument("installables", default = [], nargs = '*',
                                help = 'e.g. googlemock@1.7.0')

    parser_test = subparsers.add_parser('test')
    parser_test.add_argument("testables", default = [], nargs = '*',
                                help = 'e.g. googlemock')

    parser_test = subparsers.add_parser('make')

    args = parser.parse_args()
    if args.command == 'install':
        cmd_install(args.installables)
    elif args.command == 'make':
        cmd_make()
    elif args.command == 'test':
        cmd_test(args.testables)
    else:
        raise Exception("unknown command {}, chose install | test".format(args.command))

if __name__ == "__main__":
    main()
