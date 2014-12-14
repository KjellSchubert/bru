# for cycle detection I initially wanted to use python-graph-core
# but
#   >pip install --allow-unverified python-graph-core python-graph-core
# was kinda annoying with its need for this creepy --allow-unverified.
# Same for https://pypi.python.org/pypi/graph/0.4
# What did install easily was pip install altgraph, but this doesn't
# have cycle detection? P.S.: it does in
#   pygraph.algorithms.accessibility.mutual_accessibility
# which finds strongly connected components in a digraph.
# Anyway, just use the usual
#   >pip install -r requirements.txt
#
# See also
# https://code.google.com/p/python-graph/issues/attachmentText?id=98&aid=980000000&name=find_all_cycles.py
#
# General problem is described here:
#    http://en.wikipedia.org/wiki/Strongly_connected_component

import pdb

from pygraph.algorithms.cycles import find_cycle
from pygraph.classes.digraph import digraph
from pygraph.algorithms.accessibility import mutual_accessibility

def _graph2py_digraph(node2arc_targets):
    """ node2arc_targets is a simple digraph representation via dict() """
    graph = digraph()
    for node in node2arc_targets.keys():
        graph.add_node(node)
    for node, arc_targets in node2arc_targets.items():
        for arc_target in arc_targets:
            graph.add_edge((node, arc_target)) # insists on tuple
    return graph

def find_all_cycles(node2arc_targets):
    """ cycle aka strongly connected component of a digraph.
        Return list of stronly connected components.
    """
    result = mutual_accessibility(_graph2py_digraph(node2arc_targets))
    cycles = []
    nodes_in_cycles = set()
    for node, cycle in result.items():
        if len(cycle) <= 1:
            continue
        if node in nodes_in_cycles:
            #assert cycles.count(cycle) == 1
            continue
        cycles.append(set(cycle))
        for node in cycle:
            assert not node in nodes_in_cycles
            nodes_in_cycles.add(node)
    for cycle in cycles:
        print(node, cycle)
    return cycles

