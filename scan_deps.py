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
import pdb # only if you want to add pdb.set_trace()

OrderedDict = collections.OrderedDict

class TwoComponentPath:
    def __init__(self, root_dir, path):
        self.root_dir = root_dir
        self.path = path
    def get_full_path(self):
        return os.path.join(self.root_dir, self.path)

def get_files_from_glob_exprs(tar_root, glob_exprs):
    """ param glob_exprs is the glob expression pointing to e.g. include
        files in the module's tar file, the glob expr is relative to the
        tar_root dir.
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
            matches = glob.glob(os.path.join(local_root_dir, expr))
            for match in matches:
                files += [TwoComponentPath(local_root_dir, 
                           os.path.relpath(match, start=local_root_dir))]
    return files


def get_includes_from_cpp(cpp_file_name):
    """ open cpp or hpp file and scans it for #includes, returning the
        list of #includes """

    # the regex is suboptimal? Should match a large percentage of #includes
    print("reading " + cpp_file_name)
    pattern = re.compile('\\s*#\\s*include\\s*[\\<"](.*)[\\>"]')
    with open(cpp_file_name, 'r') as cpp_file:
        while True:
            line = cpp_file.readline()
            if len(line) == 0:
                break # eof
            match = pattern.search(line)
            if match != None:
                included_file = match.group(1)
                print("  includes " + included_file)
                yield included_file

def scan_deps(module, version):
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
    include_files = get_files_from_glob_exprs(tar_root, include_globs)
    src_files = get_files_from_glob_exprs(tar_root, src_globs)

    included_files = set(itertools.chain.from_iterable(
        get_includes_from_cpp(file.get_full_path()) for file in include_files))
    print(included_files)




    #with open(bru_file_name, 'w') as bru_file:
    #    bru_file.write(json.dumps(bru_content, indent = 4))
    #    print("created " + bru_file_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help = "e.g. boost-asio")
    parser.add_argument("version", help = "version of module, e.g. 1.57.0")
    args = parser.parse_args()
    scan_deps(args.module, args.version)

if __name__ == "__main__":
    main()
