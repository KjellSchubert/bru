#!/usr/bin/env python3

# I added this script mostly because I wanted to use modularized boost
# libs (so I don't have to pull in & compile boost-serialization just because 
# I want to use boost-regex), and because modularized boost doesn't make
# it obvious which boost module depends on which other boost module.
#
# There are two kinds of deps to consider here:
# a) deps due to public #include files of a module: e.g. when I want to 
#    #include boost-regex I have to have boost-config in the Include search
#    path because boost/regex/something.h does #include boost/config/foo.h.
# b) private deps: if a boost-regex *.cpp file #includes boost/thingy/foo.h
#    (but public #includes dont) then downstream consumers of boost-regex
#    don't need boost/thingy in their #include path. They still need to
#    link against boost/thingy though (unless boost/thingy was a header-only
#    library, many boost libs are).
#
# Not sure what the best name for these 2 kinds of deps would be: e.g. 'public'
# vs 'private' module deps? These public deps should be avoided if possible,
# e.g. via pimpl idiom. Only the linker which needs to link the final executable
# will need to accumulate all private deps across the whole dependency tree
# (and can ignore header-only deps).
#
# Dont connfuse a&b with nodejs:npm-style dev-dependencies, which are deps for
# building an individual module or its resources.
#
# WARNING: finding the exact set of needed #includes is difficult due to
# c preprocessor: some #includes may be #ifdef'ed out in some configs. This
# tool here is supposed to find the worst-case, potentially overestimated
# set of deps.

import argparse
import json
import os
import re
import os.path
import glob
import collections
import itertools
import bru
import pdb # only if you want to add pdb.set_trace()

OrderedDict = collections.OrderedDict


def get_includes_from_cpp(cpp_file_name):
    """ open cpp or hpp file and scans it for #includes, returning the
        list of #includes """

    # the regex is suboptimal? Should match a large percentage of #includes
    #print("reading " + cpp_file_name)
    pattern = re.compile('\\s*#\\s*include\\s*[\\<"](.*)[\\>"]')
    with open(cpp_file_name, 'r') as cpp_file:
        while True:
            line = cpp_file.readline()
            if len(line) == 0:
                break # eof
            match = pattern.search(line)
            if match != None:
                included_file = match.group(1)
                #print("  includes " + included_file)
                yield included_file

def get_all_modules(library_path):
    return (dir for dir in os.listdir(library_path) 
            if os.path.isdir(os.path.join(library_path, dir)))

def get_all_versions(library_path, module):
    bru_file_names = os.listdir(os.path.join(library_path, module))
    regex = re.compile('^([0-9.]+)\\.bru$')
    for bru_file_name in bru_file_names:
        match = regex.match(bru_file_name)
        if match != None:
            version = match.group(1)
            yield version

class IncludeFileIndex:
    """ created from a list of modules, each of which has a set of #include
        files. Quickly can find which module offers which #include file """

    def __init__(self, library_path, bru_modules_path):
        # different module_versions may end up with different sets if
        # #include files, so which modules should we search here? All?
        # Only the latest known version of each module? All modules
        # whose tar.gz was downloaded already anyway?
        self.include2modules = {} 
        for module in get_all_modules(library_path):
            for version in get_all_versions(library_path, module):
                formula = bru.load_formula(module, version)
                if not 'includes' in formula:
                    print("WARNING: no includes listed for " + module + " " + version)
                    continue
                includes = formula['includes']
                self._remember_includes(module, includes)

    def _remember_includes(self, module, includes):
        for include in includes:
            if not include in self.include2modules:
                self.include2modules[include] = set()
            self.include2modules[include].add(module)

    def get_modules_containing(self, included_file):
        """ returns a set of modules that contain this include file,
            this set should usually consist of one single file, unless
            several modules contain the same file, which would be worryingly
            ambiguous """
        map = self.include2modules
        return map[included_file] if included_file in map else set() 
            

def get_modules_for_includes(included_files, include_file_index):
    """ given a set of included files return the set of modules that
        contain these files, as well as the set of include files which
        were not found in any module """
    included_modules = set()
    unknown_includes = set()
    for included_file in included_files:
        mods = include_file_index.get_modules_containing(included_file)
        if len(mods) > 1:
            print("WARNING: {} is present in multiple modules: ".format(
                  included_file, mods))
        if len(mods) == 0:
            unknown_includes.add(included_file)
        included_modules = included_modules.union(mods)
    return (included_modules, unknown_includes)

def scan_deps(module, version, include_file_index):
    """ param module like "boost-asio", version like "1.57.0" """
    
    library_root = "./library"
    bru_file_name = os.path.join(library_root, module, version + ".bru")
    with open(bru_file_name, 'r') as bru_file:
       bru_content = json.loads(bru_file.read(), object_pairs_hook=collections.OrderedDict)

    artifacts = bru_content['artifacts']
    include_globs = artifacts['include']
    src_globs = artifacts['src'] if 'src' in artifacts else [] 
                # empty if header-only lib

    bru_modules = "./bru_modules"
    tar_root = os.path.join(bru_modules, module, version)
    include_files = bru.get_files_from_glob_exprs(tar_root, include_globs)
    src_files = bru.get_files_from_glob_exprs(tar_root, src_globs)

    def get_included_files(cpp_files):
        return set(itertools.chain.from_iterable(
                      get_includes_from_cpp(file.get_full_path()) 
                      for file in include_files))

    included_files_from_hpp = get_included_files(include_files)
    included_files_from_cpp = get_included_files(src_files)

    #for included_file in included_files_from_hpp:
    #    print(included_file, include_file_index.get_modules_containing(included_file))

    # now we know what #include files are needed by the module let's 
    # automatically find out which (other) modules are providing these
    # includes:
    included_modules_from_hpp, unknown_includes_hpp = get_modules_for_includes(
        included_files_from_hpp, 
        include_file_index)

    # explicitly compute the list of modules needed by cpp files only: these
    # are only internal dependencies (which later the linker has to link 
    # against, but which the compiler in downstream modules doesnt care about)
    #
    # WARNING: remember these sets of module dependencies are often overestimated,
    # e.g. if you wrap an include in an #if defined(FOO) or #if 0 the #include
    # statement will still be considered a valid potential #include!
    included_modules_from_cpp, unknown_includes_cpp = get_modules_for_includes(
        included_files_from_cpp, 
        include_file_index)
    included_modules_from_cpp = included_modules_from_cpp.difference(included_modules_from_hpp)
    print(included_modules_from_hpp)
    print(included_modules_from_cpp)
    print(unknown_includes_hpp.union(unknown_includes_cpp))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help = "e.g. boost-asio")
    parser.add_argument("version", help = "version of module, e.g. 1.57.0")
    args = parser.parse_args()
    scan_deps(args.module, args.version, 
        IncludeFileIndex('./library', './bru_modules'))

if __name__ == "__main__":
    main()
