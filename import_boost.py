#!/usr/bin/env python3

# Helper file for pulling all modules of modularized Boost from
# github separately, which is a few dozen modules.

import argparse
import json
import re
import urllib.request
import os
import os.path
import bru
from collections import OrderedDict
import pdb # only if you want to add pdb.set_trace()


def wget(url, filename):
    """ typically to download tar.gz or zip """
    # from http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
    print("wget {} -> {}".format(url, filename))
    urllib.request.urlretrieve(url, filename)

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
    tar_root_dir = os.path.join(bru_modules, bru_module_name, version,
        boost_lib + "-boost-" + version)
    assert os.path.exists(tar_root_dir)
    assert os.path.exists(os.path.join(tar_root_dir, "include"))
    print("downloaded " + boost_lib + " to " + tar_root_dir)

    bru_file_content = OrderedDict([
        ("homepage", "http://www.boost.org/"),
        ("url", "https://github.com/boostorg/" + boost_lib 
                + "/archive/boost-1.57.0.tar.gz"),
        ("artifacts", {
            "include" : [
                OrderedDict([
                    ("local_root_dir", boost_lib + "-boost-" + version + "/include"),
                    ("glob_expr", "**/*.hpp;**/**/*.hpp"),
                    ("tar_root_dir", "")
                ])
            ],
            # dont need lib dir for header-only libs
        })
    ])

    # most boost libs are #include only, some like regex do have a src dir
    # though and need to be compiled.
    if os.path.exists(os.path.join(tar_root_dir, "src")):
        print("boost module " + boost_lib + " has a src/ dir")
        bru_file_content['artifacts']['lib'] = [
            OrderedDict([
                ("local_root_dir", boost_lib + "-boost-" + version + "/lib"),
                ("glob_expr", "*.a;*.lib;*.so;*.dll"),
                ("tar_root_dir", "")
          ])
        ]

    # here we could in theory also determine deps between boost modules
    # automatically by finding #include statements in cpp and hpp files, and
    # by searching all local boost_modules for which boost module provides
    # each #include. But let's rather have a more general tool do that for
    # arbitrary libraries, not just for boost.
    # See scan_deps.py for that tool.

    library_root = "./library"
    if not os.path.isdir(library_root):
      raise Exception("expected to run script in repo root with " + libary_root + " dir")
    
    bru_module_dir = os.path.join(library_root, bru_module_name)
    bru_file_name = os.path.join(bru_module_dir, version + ".bru")
    if os.path.exists(bru_file_name):
        print("not moddifying existing " + bru_file_name)
        return

    os.makedirs(bru_module_dir, exist_ok=True)
    with open(bru_file_name, 'w') as bru_file:
        bru_file.write(json.dumps(bru_file_content, indent = 4))
        print("created " + bru_file_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module", help = "e.g. asio or 'all' to get all boost libs")
    parser.add_argument("version", help = "version of boost lib to imp, e.g. 1.57.0")
    args = parser.parse_args()
    all_boost_lib_names = get_boost_lib_names()
    boost_lib = args.module
    version = args.version
    if boost_lib == 'all':
        for boost_lib in all_boost_lib_names:
            import_boost(boost_lib, version)
    else:
        assert boost_lib in all_boost_lib_names
        import_boost(boost_lib, version)


if __name__ == "__main__":
    main()
