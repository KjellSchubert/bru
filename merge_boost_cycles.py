#!/usr/bin/env python3
# See import_boost.py for usage.

import argparse
import json
import re
import urllib.request
import os
import os.path
import shutil
import bru
import copy
from collections import OrderedDict
import pdb # only if you want to add pdb.set_trace()

def merge_key(source, target, key):
    """ in-place merge """
    assert isinstance(source, dict)
    assert isinstance(target, dict)
    if not key in source:
        return # nothing to merge
    value = source[key]
    if key in target:
        merge_elem(value, target[key])
    else:
        # no need to merge, just copy
        target[key] = value

def merge_dict(source, target):
    """ in-place merge """
    assert isinstance(source, dict)
    assert isinstance(target, dict)
    for key in source.keys():
        merge_key(source, target, key)

def merge_list(source, target):
    """ in-place merge """
    # don't create duplicates
    assert isinstance(source, list)
    assert isinstance(target, list)
    merged = set(source).union(set(target))
    target.clear()
    target += merged

def merge_elem(source, target):
    """ in-place merge """
    if isinstance(target, list) and isinstance(source, list):
        merge_list(source, target)
    elif isinstance(target, dict) and isinstance(source, dict):
        merge_dict(source, target)
    elif isinstance(target, str) and isinstance(source, str) and target == source:
        pass # nothing to do
    else:
        raise Exception('merge_elem cannot merge {} into {}'.format(
            source, target))

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
# See also cycle status at
#    https://svn.boost.org/trac/boost/wiki/ModuleDepednecies
def fix_annoying_dependency_cycle(module_names, target_module, version):
    """ merge all bru & gyp files together, making module_names[0] the
        merge target """

    print('merging dependency cycle:', module_names, 'into', target_module)
    formulas = list(map(
        lambda module_name: bru.load_formula(module_name, version), 
        module_names))
    gyps = list(map(
        lambda formula: bru.load_gyp(formula),
        formulas))

    # Merge the *.bru files.
    # Replace each source formula with a formula that has only a single
    # dependency to the merged formula, and with no tar.gz urls:
    target_formula = copy.deepcopy(formulas[0])
    target_formula['module'] = target_module
    target_formula['url'] = []
    for merge_source in formulas:
        if not isinstance(merge_source['url'], list):
            merge_source['url'] = [ merge_source['url'] ]
        merge_key(merge_source, target_formula, 'url')
        merge_key(merge_source, target_formula, 'dependencies')
        merge_source['url'] = []
        merge_source['dependencies'] = { target_module: version }
        bru.save_formula(merge_source)
    #xxx TODO: remove deps to merge_sources from target_formula
    bru.save_formula(target_formula)
    
    # Merge the *.gyp files.
    # Replace the original gyp files with one that depends on the merged
    # dependency only, and forwards all its settings via 
    # gyp's export_dependent_settings.
    target_gyp = copy.deepcopy(gyps[0])
    merged_target = target_gyp['targets'][0]
    merged_target['target_name'] = target_module
    merged_target['include_dirs'] = []
    merged_target['sources'] = []
    merge_dep = '../{}/{}.gyp:{}'.format(
        target_module, target_module, merged_target['target_name'])
    for i in range(len(gyps)):
        formula = formulas[i]
        gyp = gyps[i]
        targets = gyp['targets']
        assert len(targets) == 1
        source = targets[0]
        for key in ['all_dependent_settings', 'direct_dependent_settings', 
                    'include_dirs', 'sources']:
            if key in source:
                merge_key(source, merged_target, key)
                del source[key]
        source['dependencies'] = [ merge_dep ]
        source['export_dependent_settings'] = [ merge_dep ]
        bru.save_gyp(formula, gyp)
    #xxx TODO: remove deps to merge_sources from target_gyp
    bru.save_gyp(target_formula, target_gyp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help = "version of boost libs to merge, e.g. 1.57.0")
    args = parser.parse_args()
    version = args.version
    fix_annoying_dependency_cycle([
            'boost-mpl', 
            'boost-type_traits', 
            'boost-typeof',
            'boost-utility'],
        'boost-mpl-type_traits-typeof-utility',
        version)
    fix_annoying_dependency_cycle([
            'boost-math', 
            'boost-lexical_cast'],
        'boost-lexical_cast-math',
        version)

if __name__ == "__main__":
    main()
