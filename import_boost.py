#!/usr/bin/env python3

# Helper file for pulling all modules of modularized Boost from
# github separately, which is a few dozen modules.
#
# To import all of boost and then build boost_regex run these cmds:
#   >./import_boost.py all 1.57.0
#   >./scan_deps.py boost* -r
#   >./detect_cycles.py   # should not detect dependency cycles
# Sadly this doesn't work as of today without generating plenty of module 
# dependency cycles, see details below at fix_annoying_dependency_cycle().
#
# Currenty for boost 1.57 these cycles here are detected by detect_cycles.py:
#   {mpl type_traits typeof utility} # resolved by merging all these modules into library/boost-mpl
#   {'boost-random', 'boost-range', 'boost-tr1', 'boost-lexical_cast', 'boost-math', 'boost-algorithm'}           
#   {'boost-graph_parallel', 'boost-property_map', 'boost-bimap', 'boost-disjoint_sets', 'boost-graph', 'boost-mpi'}
#   {'boost-date_time', 'boost-spirit', 'boost-serialization', 'boost-pool', 'boost-thread'}

import argparse
import json
import re
import urllib.request
import os
import os.path
import shutil
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
    ])

    # some boost libs have a src dir (e.g. boost-regex), but most don't. The 
    # gyp target will need to know if the lib is #include-only or not:
    include_dir = os.path.join(tar_content_dir, "include")
    src_dir = os.path.join(tar_content_dir, "src")
    assert os.path.exists(include_dir)
    has_src_dir = os.path.exists(src_dir)

    def get_dir_relative_to_gyp(path):
        return os.path.relpath(path, start=os.path.dirname(tar_root_dir))

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
        gyp_target['sources'] = [ 
            os.path.join(get_dir_relative_to_gyp(src_dir), "*.cpp") ]

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
    
    if not os.path.exists(os.path.join(library_root, bru_module_name)):
        print('saving', bru_module_name, 'to library')
        bru.save_formula(formula)
        bru.save_gyp(formula, gyp)
    else:
        print('skipping existing module', bru_module_name)

# WARNING: after I started generating a *.gyp file for each 
# modularized boost lib it turned out that gyp complained about
# dependency cycles between boost libs, and gyp refuses to generate
# makefiles between modules with circular deps (even with
# gyp --no-circular-check). Any modularization effort that ends up
# with dep cycles seems like a fail to me, I wonder what criterions
# where used for boost modularization :( In any case: we could
# auto-merge each cluster of circular dependent libs (choosing the
# conceptually highest-level cluster member's module name as the name
# for the cluster) if the number of dep cycles is small. See also 
#    http://lists.boost.org/Archives/boost/2014/06/214634.php
# for more details.
# Also see dep graphs at 
#    http://www.steveire.com/boost/after-edge-removal-june-14/range.png
#    http://www.steveire.com/boost/deps-june-14/thread.png
#    http://www.steveire.com/boost/deps-june-14/date_time.png
#    http://www.steveire.com/boost/deps-june-14/regex.png
# This indicates a serious problem with dependency cycles in modular boost!
# E.g. you cant use boost-thread without also requiring the #includes
# for boost-spirit. Which is not an intuitive or desirable dependency.
# After I merged the partial mpl cycle the detect_cycles.py emitted another
# set of cycles it hadn't mentioned the first time:
#    ['boost-date_time', 'boost-serialization', 'boost-spirit', 'boost-pool', 'boost-thread']
#    ['boost-graph', 'boost-bimap', 'boost-property_map', 'boost-mpi']
#    ['boost-disjoint_sets', 'boost-graph', 'boost-graph_parallel']
# So I guess atm the graph cycle detection script does not reliably emit
# ALL cycles after all (since these weren't listed the 1st time I ran
# the script).
# After getting this set of cycles I'm thinking boost modularization
# is a bit of a failure (or work in progress?) atm, and boost is a pretty 
# monolithic lib as of 1.57.0 :(
def fix_annoying_dependency_cycle(module_names, version):
    """ merge all bru & gyp files together, making module_names[0] the
        merge target """

    print('merging dependency cycle:', module_names)
    formulas = list(map(
        lambda module_name: bru.load_formula(module_name, version), 
        module_names))
    gyps = list(map(
        lambda formula: bru.load_gyp(formula),
        formulas))

    # first merge the *.bru files:
    all_urls = []
    for merge_source in formulas[0:]:
        all_urls.append(merge_source['url']) # list of tgzs
    target_formula = formulas[0]
    target_formula['url'] = all_urls
    bru.save_formula(target_formula)

    # now merge the *.gyp files:
    all_include_dirs = []
    for gyp in gyps:
        targets = gyp['targets']
        assert len(targets) == 1
        target = targets[0]
        assert target['type'] == 'none' # it's an #include-only lib
        all_include_dirs += target['include_dirs']
    target_gyp = gyps[0]
    merged_target = target_gyp['targets'][0]
    merged_target['include_dirs'] = all_include_dirs
    for dependent_settings in ['all_dependent_settings', 
                               'direct_dependent_settings']:
        if not dependent_settings in merged_target:
            continue
        settings_dict = merged_target[dependent_settings]
        if not 'include_dirs' in settings_dict:
            continue
        settings_dict['include_dirs'] = all_include_dirs
    bru.save_gyp(target_formula, target_gyp)

    # now delete the merge source dir's *.gyp and *.bru files, or
    # alternatively nuke the whole dir
    for deleted_module in module_names[1:]:
        def rmrf(deleted_dir):
            print('deleting merged', deleted_dir)
            shutil.rmtree(deleted_dir)
        rmrf(os.path.join('library', deleted_module))
        rmrf(os.path.join('bru_modules', deleted_module))


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

        # this cycle was detected by detect_cycles.py for 1.57. Maybe future
        # boost versions won't suffer from that anymore, we'll see.
        if True:
            fix_annoying_dependency_cycle([
                    'boost-mpl', 
                    'boost-type_traits', 
                    'boost-typeof',
                    'boost-utility'],
                version)
    else:
        assert boost_lib in all_boost_lib_names
        import_boost(boost_lib, version)


if __name__ == "__main__":
    main()
