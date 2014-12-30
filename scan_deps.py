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
import subprocess
import bru
import pdb # only if you want to add pdb.set_trace()

def get_library():
    return bru.get_library()

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

def get_include_files(include_dir):
    """ returns relative paths for all #include files underneath this dir.
        Since we can't be sure which extensions are include files and which
        ones aren't we simply return all files underneath this dir 
    """
    for root, dirs, files in os.walk(include_dir):
        for file in files:
            filename = os.path.join(root, file)
            include_file = os.path.relpath(filename, start=include_dir)
            yield include_file

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
         Returns a list of TwoComponentPath objects.
    """
    gyp = get_library().load_gyp(formula)
    module = formula['module']
    version = formula['version']
    gyp_root_dir = os.path.join('./bru_modules', module)
    # here we assume the gyp file is located in gyp_root_dir

    include_files = []
    for target in gyp['targets']:
        if not 'include_dirs' in target:
           continue # e.g. target zlib:zlib_test doesn't need include_dirs 
        include_dirs = target['include_dirs']
        for include_dir in include_dirs:
            abs_include_dir = os.path.join(gyp_root_dir, include_dir)
            include_files += [bru.TwoComponentPath(abs_include_dir, include_file)
                              for include_file 
                              in get_include_files(abs_include_dir)]
    #assert len(include_files) > 0, "missing includes for " + module
    if len(include_files) == 0:
        # didn't create an ICU gyp file yet, looks painful to me
        print("WARNING: no includes for module ", module)
    return include_files

class IncludeFileIndex:
    """ created from a list of modules, each of which has a set of #include
        files. Quickly can find which module offers which #include file """

    def __init__(self, library_path, bru_modules_path):
        # different module_versions may end up with different sets if
        # #include files, so which modules should we search here? All?
        # Only the latest known version of each module? All modules
        # whose tar.gz was downloaded already anyway?
        self.include2modules = {} 
        library = get_library()
        for module in get_all_modules(library_path):
            print('scanning #includes for', module)
            for version in library.get_all_versions(module):
                formula = library.load_formula(module, version)
                bru.unpack_module(formula)
                includes = [two_component_path.path 
                    for two_component_path in collect_includes(formula)]
                includes.sort()
                #print("includes for ", module, ": ", includes)
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

def find_includes(include_root_dir):
    includes = []
    for root, dirs, files in os.walk(include_root_dir):
        for file in files:
            include_file = os.path.join(root, file)
            # could also make it a TwoComponentPath here
            includes.append(include_file)
    return includes

def scan_deps(formula, include_file_index):
    """ param module like "boost-asio", version like "1.57.0" """
    
    module = formula['module']
    version = formula['version']
    bru_modules = "./bru_modules"
    gyp_root = os.path.join(bru_modules, module) # paths in gyp are rel to that
    tar_root = os.path.join(gyp_root, version)

    # We need to know where are the hpp and cpp files for this module.
    # If the module comes with a gyp file then we could extract the 
    # 'include_dirs' and 'sources' file libs (or glob expr lists) from
    # it, though (e.g. for zlib) this requires taking 'copies' actions
    # into account (or executing the 'copies' action). 
    # We could also heuristically search for cpp and hpp files, but
    # this won't work too well (e.g. it'll add dependencies only needed
    # for tests)
    gyp = get_library().load_gyp(formula)
    include_files = []
    src_files = []
    for target in gyp['targets']:
        if 'include_dirs' in target:
            for include_dir in target['include_dirs']:
                # any file could be included, not just *.hpp and *.h
                include_files += find_includes(
                                  os.path.join(gyp_root, include_dir))
        if 'sources' in target:
            for src_filename in target['sources']:
                # src_filename could be glob expr or file, but is always
                # relative to gyp_root
                src_files += glob.glob(os.path.join(gyp_root, src_filename))

    def abbreviate_list(elems):
        prefix = elems[:min(5, len(elems))]
        return prefix
    print('include_files:',abbreviate_list(include_files))
    print('src files:', abbreviate_list(src_files))

    def get_included_files(cpp_files):
        return set(itertools.chain.from_iterable(
                      get_includes_from_cpp(file) 
                      for file in include_files))

    included_files_from_hpp = get_included_files(include_files)
    included_files_from_cpp = get_included_files(src_files)

    #for included_file in included_files_from_hpp:
    #    print(included_file, include_file_index.get_modules_containing(included_file))

    # now we know what #include files are needed by the module let's 
    # automatically find out which (other) modules are providing these
    # includes:
    included_files = included_files_from_hpp.union(included_files_from_cpp)
    included_modules, unknown_includes = get_modules_for_includes(
        included_files, 
        include_file_index)

    # remove the obvious dep to the same module:
    def remove_if_exists(set, elem):
        if elem in set:
             set.remove(elem)
    remove_if_exists(included_modules, module)

    return (included_modules, unknown_includes)

def is_in_scm(path):
    """ return true if the file is (git) versioned """
    # http://stackoverflow.com/questions/2405305/git-how-to-tell-if-a-file-is-git-tracked-by-shell-exit-code
    with open(os.devnull, 'w') as devnull:
        proc = subprocess.Popen(['git', 'ls-files', '--error-unmatch', path], 
                 stdout = devnull, stderr = devnull)
        proc.wait()
        returncode = proc.returncode
    return returncode == 0

def get_arg_modules(module, version):
    """ returns list of (module,version) tuples given cmdline args.
        If version is None then we pick the latest available version
        of a module
        If module ends with '*' then we glob all matching modules """
    library = get_library()
    if module.endswith('*'):
        lib_dir = './library'
        matching_dirs = glob.glob(os.path.join(lib_dir, module))
        modules = [os.path.relpath(dir, start=lib_dir) for dir in matching_dirs]
        return [(module, version or library.get_latest_version_of(module)) 
                for module in modules]
    else:
        version = version or library.get_latest_version_of(module)
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
    library = get_library()

    todo_module_version = get_arg_modules(args.module, args.version)
    done_modules = set()
    while len(todo_module_version) > 0:
        module, version = todo_module_version.pop()
        if module in done_modules:
            continue
        
        print("scanning module {} version {}".format(module, version))
        formula = library.load_formula(module, version)
        (deps, missing_includes) = scan_deps(formula, index)
        print("dependencies: ")
        for dep in deps:
            # show for each dep if it was git added alrdy
            print(dep, '' if is_in_scm(os.path.join('library', dep)) else '*')
        if len(missing_includes) > 0:
            print("missing includes: ", missing_includes)

        # now add the computed dependencies to the formula, unless
        # the formula alrdy epxlicitly lists deps:
        if not 'dependencies' in formula:
            def annotate_with_latest_version(modules):
                dependency2version = collections.OrderedDict()
                for module in sorted(modules):
                    dependency2version[module] = library.get_latest_version_of(module)
                return dependency2version

            # remove deps we consider builtin, like C++ stdlib and C lib. 
            # This here is kinda fuzzy and differs between OSs.
            builtin_deps = set([
                'llvm-libcxx'
            ])
            deps = deps.difference(builtin_deps)

            formula['dependencies'] = annotate_with_latest_version(deps)
            print(formula)
            bru.save_formula(formula)

        # also add the deps to the gyp in a sloppy & ad-hoc way for now:
        # this works sort of ok for modules with a single target only (e.g.
        # the boost modules after boost_import.py): add the all found
        # deps to the first gyp target's dependencies.
        if len(deps) > 0:
            gyp = library.load_gyp(formula)
            first_target = gyp['targets'][0]
            if not 'dependencies' in first_target:
                # Todo: reconsider the ':*' dependency on all targets in 
                # upstream modules. May wanna exclude test targets from this,
                # which we cannot do here easily though. Maybe bru.py can
                # exclude test targets later on? Test targets give extra
                # confidence that things are wired up fine, but will increase
                # initial compile times after 'bru install'.
                first_target['dependencies'] = [
                    "../{}/{}.gyp:*".format(dep, dep) for dep in deps]
                bru.save_gyp(formula, gyp)

        done_modules.add(module)

        if args.recursive:
            direct_dependency_modules = list(item for item in deps)
            todo_module_version += ((module, library.get_latest_version_of(module)) 
                                   for module in direct_dependency_modules)

    if args.recursive:
        print("recursive module dependencies: ", done_modules)

if __name__ == "__main__":
    main()
