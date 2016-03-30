#!/usr/bin/env python3

# you don't want dependency cycles between modules, this script here
# checks if you have such cycles in your library. E.g. the boost_import.py
# script blindly imports each boost module separately, but these modules
# happen to have ugly/crippling dependency cycles, soo import_boost.py
# for more details.

import argparse
import os
import re
import os.path
import glob
import itertools
import bru
import scan_deps
import graph_cycles
import pdb # only if you want to add pdb.set_trace()

def get_library():
    return bru.get_library()

def get_lib_with_most_includes(formulas):
    """ return formula with most include files """
    tuples = []
    for formula in formulas:
        include_file_count = len(scan_deps.collect_includes(formula))
        print(formula['module'], 'has', include_file_count, 'includes')
        tuples.append((include_file_count, formula))
    result = max(tuples)[1] 
    return result

def merge_formulas_into(target, sources):
    # we merge the targzs into a list, they'll be unpacked into the same
    # target dir. This means all include_dirs in the module's gyp files
    # must be merged also.
    # P.S.: let's just do the merge in import-boost.py, that's a bit simpler
    # then a generic merge function.
    raise Exception('todo')

def merge_module_cycle(formulas):
    # here's one example cycle you get after import-boost.py:
    #   ['boost-mpl', 'boost-type_traits', 'boost-typeof']
    # merging modules is relatively straightforward (assuming
    # their tar files can simply be extracted into the same dir
    # without overwriting each other's files, which is the case
    # for these boost libs), but what name should be chosen for
    # the merged lib? Let the user choose a name, or auto-chose
    # the name of the largest of these libs, e.g. measured in 
    # each lib's number (or file size) of include files:
    merged_formula = get_lib_with_most_includes(formulas)
    print('=> merging all libs into', merged_formula['module'])
    print('not doing automated merge atm, merge manually')
     

def main():
    # Import each module, each of which should list accurate module
    # dependencies. If a module has multiple version we only look
    # at the latest one for simplicity's sake.
    module2formula = {}
    library = get_library()
    for module in os.listdir('library'):
        version = library.get_latest_version_of(module)
        formula = library.load_formula(module, version)
        module2formula[module] = formula
    print("loaded ", len(module2formula), " formulas")

    # now detect dep cycles between formulas/modules:
    # turn the deps into this graph structure, ignoring module versions:
    # {
    #   'boost-regex': ['boost-config', 'boost-foo', ...]
    #   'boost-config': ...
    # }
    dep_graph = {}
    for formula in module2formula.values():
        module_name = formula['module']
        deps = formula['dependencies'].keys() \
               if 'dependencies' in formula else []
        dep_graph[module_name] = list(deps)

    # now use general graph cycle detection 
    cycles = graph_cycles.find_all_cycles(dep_graph)
    if len(cycles) == 0:
        print("no cycles detected, good")
        return

    cycle_member_count = sum(len(cycle) for cycle in cycles)
    print(len(cycles), 'cycles found with', cycle_member_count, 'members:\n  ', 
        "\n  ".join(
            map(
                lambda modulelist: str(modulelist),
            cycles)))

    # if cycles were found then merge them
    for cycle in cycles:
       merge_module_cycle(map(
        lambda module: module2formula[module],
        cycle))

if __name__ == "__main__":
    main()

