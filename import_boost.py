#!/usr/bin/env python3

# Helper file for pulling all modules of modularized Boost from
# github separately, which is a few dozen modules.
#
# WARNING: after I started generating a *.gyp file for each 
# modularized boost lib it turned out that gyp complained about
# dependency cycles between boost libs, and gyp refuses to generate
# makefiles between modules with circular deps (even with
# gyp --no-circular-check). Any modularization effort that ends up
# with dep cycles seems like a fail to me, I wonder what criterions
# where used for boost modularization :( In any case: we could
# auto-merge each cluster of circular dependent libs (choosing the
# conceptually highest-level cluster member's module name as the name
# for the cluster), e.g. 
#    http://lists.boost.org/Archives/boost/2014/06/214634.php
# suggests that the number of circular modules in boost is small.
# Also see dep graps at 
#    http://www.steveire.com/boost/after-edge-removal-june-14/range.png

import argparse
import json
import re
import urllib.request
import os
import os.path
import bru
from collections import OrderedDict
import pdb # only if you want to add pdb.set_trace()

def get_boost_lib_names():
    
    # where's a good & uptodate list of (modularized) Boost libs?
    # I only see https://github.com/boostorg/boost/tree/master/libs, which is
    # in HTML format only.
    response = urllib.request.urlopen("https://github.com/boostorg/boost/tree/master/libs")
    assert response.status == 200
    html     =  response.read().decode(response.headers.get_content_charset())
    
    # Parsing the github HTML is kinda tedious, and the HTML can change anytime.
    # I wasn't keen on a git clone just to get one directory though.
    # Just scan the HTML for 'title="../accumulators.git @ 69dcfd15', which is
    # pretty crappy:
    matches = re.findall('\\.\\.\\/(.*)\\.git @', html)
    assert len(matches) > 10 and 'asio' in matches, "regex is outdated, update it"
    return matches

def import_boost(boost_lib, version):
    """ param boost_lib like "asio", version like "1.57.0" """

    assert re.match("[a-z0-9_]+", boost_lib)
    bru_module_name = "boost-" + boost_lib
    tar_url = "https://github.com/boostorg/" + boost_lib + "/archive/boost-" + version + ".tar.gz"
    bru_modules = "./bru_modules"
    bru.unpack_dependency(bru_modules, bru_module_name, 
                          version, tar_url)

    # now that the modularized boost dep was unpacked in ./bru_modules,
    # so lets inspect it:
    
    # this here is the dir the tar was extracted into:
    tar_root_dir = os.path.join(bru_modules, bru_module_name, version)

    # this is one level below the tar_root_dir, it's the dir which should
    # have an ./include dir.
    tar_content_dir = os.path.join(tar_root_dir, boost_lib + "-boost-" + version)

    assert os.path.exists(tar_content_dir)
    assert os.path.exists(os.path.join(tar_content_dir, "include"))
    print("downloaded " + boost_lib + " to " + tar_content_dir)

    formula = OrderedDict([
        ("homepage", "http://www.boost.org/"),
        ("url", "https://github.com/boostorg/{}/archive/boost-{}.tar.gz"\
            .format(boost_lib, version)),
        ("module", bru_module_name),
        ("version", version),

        # todo: rem?
        ("artifacts", {
            "include" : [
                OrderedDict([
                    ("local_root_dir", boost_lib + "-boost-" + version + "/include"),

                    # note that **/*.h searches more than one level, being an
                    # Ant-style glob, not a Python-glob-style glob.
                    # Initially I had a pattern 'ant:**/*.hpp' here, but
                    # boost-compatibility has #include names like 'ctime', without
                    # a *.h or *.hpp extension.
                    ("glob_expr", "ant:**/*"),

                    ("tar_root_dir", "")
                ])
            ],
            # dont need lib dir for header-only libs
        })
    ])

    # some boost libs have a src dir (e.g. boost-regex), but most don't. The 
    # gyp target will need to know if the lib is #include-only or not:
    include_dir = os.path.join(tar_content_dir, "include")
    src_dir = os.path.join(tar_content_dir, "src")
    assert os.path.exists(include_dir)
    has_src_dir = os.path.exists(src_dir)

    def get_dir_relative_to_gyp(path):
        return os.path.relpath(path, start=tar_root_dir)

    gyp_target =\
        OrderedDict([
            ('target_name', bru_module_name),
            ('type', 'static_library' if has_src_dir else 'none'),
            ('include_dirs', [ get_dir_relative_to_gyp(include_dir) ]),
            # I wish I could use direct_dependent_settings here, but I cannot:
            ('all_dependent_settings', {
                'include_dirs' : [ get_dir_relative_to_gyp(include_dir) ]
            })
        ])
    if has_src_dir:
        gyp_target['sources'] = os.path.join(get_dir_relative_to_gyp(src_dir), "*.cpp")

        def has_subdirs(dir):
            for file in os.listdir(dir):
                if os.path.isdir(os.path.join(dir, file)):
                    return True
            return False
        # src_dir should be flat, otherwise we'd have to use a different
        # 'sources' expression in the gyp file. One boost dir that violates 
        # this is boost.context, with an asm subdir
        libs_with_known_src_subdirs = [
            'context',   # asm subdir
            'coroutine', # posix and windows subdirs
            'date_time', # posix_time
            'locale',
            'math',
            'mpi',
            'python',
            'thread',
            'wave',
        ]
        assert not has_subdirs(src_dir) or boost_lib in libs_with_known_src_subdirs

    gyp = { "targets": [ gyp_target ] }

    # here we could in theory also determine deps between boost modules
    # automatically by finding #include statements in cpp and hpp files, and
    # by searching all local boost_modules for which boost module provides
    # each #include. But let's rather have a more general tool do that for
    # arbitrary libraries, not just for boost.
    # See scan_deps.py for that tool.

    library_root = "./library"
    if not os.path.isdir(library_root):
      raise Exception("expected to run script in repo root with " + libary_root + " dir")
    
    bru.save_formula(formula)
    bru.save_gyp(formula, gyp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help = "e.g. asio or 'all' to get all boost libs")
    parser.add_argument("version", help = "version of boost lib to imp, e.g. 1.57.0")
    args = parser.parse_args()
    all_boost_lib_names = get_boost_lib_names()
    boost_lib = args.module
    version = args.version

    def remove_prefix(text, prefix):
        return text[len(prefix):] if text.startswith(prefix) else text

    def remove_prefixes(text, prefixes):
        for prefix in prefixes:
            text = remove_prefix(text, prefix)
        return text

    boost_lib = remove_prefixes(boost_lib, ['boost-', 'boost_'])
    if boost_lib == 'all':
        for boost_lib in all_boost_lib_names:
            import_boost(boost_lib, version)
    else:
        assert boost_lib in all_boost_lib_names
        import_boost(boost_lib, version)


if __name__ == "__main__":
    main()
