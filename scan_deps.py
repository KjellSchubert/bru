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
import functools # @total_ordering
import bru
import pdb # only if you want to add pdb.set_trace()

OrderedDict = collections.OrderedDict


def get_includes_from_cpp(cpp_file_name):
    """ open cpp or hpp file and scans it for #includes, returning the
        list of #includes """

    # the regex is suboptimal? Should match a large percentage of #includes
    #print("reading " + cpp_file_name)
    pattern = re.compile('\\s*#\\s*include\\s*[\\<"](.*)[\\>"]')
    try:
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
    except:
        # Some files we open experimentally assuming they are a utf8 cpp file
        # may not actually be one. Ignore these.
        print("WARNING: could not get includes from ", cpp_file_name)

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
    versions = get_all_versions('./library', module)
    return max((ModuleVersion(version_text) for version_text in versions)).version_text

def collect_includes(formula):
    """  one of the most basic things to know about a module is which
         include files it comes with: e.g. for boost you're supposed
         to #include "boost/regex/foo.h", not #include "regex/foo.h"
         or #include "foo.h". 
         For most modules this list of #includes can be generated from
         the module's unpacked archive directly (assuming the root
         include directories are listed in the module's artifact list),
         but for the kinds of modules that generate or modify #include 
         files during ./configure you should collect_includes only after
         ./configure or even after make. These kinds of libs are hopefully
         rare though.
         This func here will modify the $formula in-place, adding the 
         list of #include files as an 'includes' property.
    """
    if not 'module' in formula or not 'version' in formula:
        print(json.dumps(formula, indent=4))
        raise Exception('missing module & version')
    module = formula['module']
    version = formula['version']
    tar_root_dir = os.path.join('./bru_modules', module, version)
    include_files = bru.get_files_from_glob_exprs(
        tar_root_dir, formula['artifacts']['include'])
    assert len(include_files) > 0   # there's no boost lib without #includes
    includes = [two_component_path.path for two_component_path in include_files]
    includes.sort()
    formula['includes'] = includes

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

                    # if the *.bru file doesn't include a list of #includes
                    # yet then let's create that list now.
                    bru.unpack_module(formula)
                    collect_includes(formula)
                    bru.save_formula(formula)
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
    
    formula = bru.load_formula(module, version)
    artifacts = formula['artifacts']
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

    # remove the obvious dep to the same module:
    def remove_if_exists(set, elem):
        if elem in set:
             set.remove(elem)
    remove_if_exists(included_modules_from_cpp, module)
    remove_if_exists(included_modules_from_hpp, module)

    # now add the computed dependencies to the formula, unless
    # the formula alrdy epxlicitly lists deps:
    if not 'hpp_dependencies' in formula:
        def annotate_with_latest_version(modules):
            dependency2version = OrderedDict()
            for module in sorted(modules):
                dependency2version[module] = get_latest_version_of(module)
            return dependency2version
        formula['hpp_dependencies'] = annotate_with_latest_version(included_modules_from_hpp)
        formula['cpp_dependencies'] = annotate_with_latest_version(included_modules_from_cpp)
        bru.save_formula(formula)

    return (included_modules_from_hpp, included_modules_from_cpp, 
            unknown_includes_hpp.union(unknown_includes_cpp))

def get_arg_modules(module, version):
    """ returns list of (module,version) tuples given cmdline args.
        If version is None then we pick the latest available version
        of a module
        If module ends with '*' then we glob all matching modules """
    if module.endswith('*'):
        lib_dir = './library'
        matching_dirs = glob.glob(os.path.join(lib_dir, module))
        modules = [os.path.relpath(dir, start=lib_dir) for dir in matching_dirs]
        return [(module, version or get_latest_version_of(module)) 
                for module in modules]
    else:
        version = version or get_latest_version_of(module)
        return [(module, version)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help = "e.g. boost-asio, or 'boost*'")
    parser.add_argument("--version", '-v', required = False, default = None,
        help = "version of module, e.g. 1.57.0, defaults to latest if unspecified")
    parser.add_argument('--recursive', '-r', action='store_true', 
        help='recursively find dependencies')
    args = parser.parse_args()
    index = IncludeFileIndex('./library', './bru_modules')

    todo_module_version = get_arg_modules(args.module, args.version)
    done_modules = set()
    while len(todo_module_version) > 0:
        module, version = todo_module_version.pop()
        if module in done_modules:
            continue
        
        print("scanning module {} version {}".format(module, version))
        (hpp_deps, cpp_deps, missing_includes) = scan_deps(module, version, index)
        print("hpp dependencies: ", hpp_deps)
        print("(additional) cpp dependencies: ", cpp_deps)
        print("missing includes: ", missing_includes)
        done_modules.add(module)

        if args.recursive:
            direct_dependency_modules = list(item for item in hpp_deps.union(cpp_deps))
            todo_module_version += ((module, get_latest_version_of(module)) 
                                   for module in direct_dependency_modules)

    if args.recursive:
        print("recursive module dependencies: ", done_modules)

if __name__ == "__main__":
    main()
