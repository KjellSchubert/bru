# for cycle detection I initially wanted to use python-graph-core
# but
#   >pip install --allow-unverified python-graph-core python-graph-core
# was kinda annoying with its need for this creepy --allow-unverified.
# Same for https://pypi.python.org/pypi/graph/0.4
# What did install easily was pip install altgraph, but this doesn't
# have cycle detection?
# Anyway, just use the usual
#   >pip install -r requirements.txt
# Unfortunately there's no method to find all cycles in pygraph, so
# this code below yields only one cycle. A cycle detection algo is
# here though:
# https://code.google.com/p/python-graph/issues/attachmentText?id=98&aid=980000000&name=find_all_cycles.py
if False:
    from pygraph.algorithms.cycles import find_cycle
    from pygraph.classes.digraph import digraph
    def find_one_pointless_cycle(node2arc_targets):
        """ node2arc_targets is a simple digraph representation via dict() """
        graph = digraph()
        for node in node2arc_targets.keys():
            graph.add_node(node)
        for node, arc_targets in node2arc_targets.items():
            for arc_target in arc_targets:
                graph.add_edge((node, arc_target)) # insists on tuple
        print(find_cycle(graph))

"""
find_all_cycles contributed by Mathias Laurin <Mathias Laurin AT gmail com>
"""

def find_cycle_to_ancestor(spanning_tree, node, ancestor):
    """
    Find a cycle containing both node and ancestor.
    """
    path = []
    while (node != ancestor):
        if node is None:
            return []
        path.append(node)
        node = spanning_tree[node]
    path.append(node)
    path.reverse()
    return path

def find_all_cycles(graph):
    """
    Find all cycles in the given graph.

    This function will return a list of lists of nodes, which form cycles in the
    graph or an empty list if no cycle exists.
    """

    def dfs(node):
        """
        Depth-first search subfunction.
        """
        visited.add(node)
        # Explore recursively the connected component
        for each in graph[node]:
            if each not in visited:
                spanning_tree[each] = node
                dfs(each)
            else:
                if (spanning_tree[node] != each):
                    cycle = find_cycle_to_ancestor(spanning_tree, node, each)
                    if cycle:
                        cycles.append(cycle)

    visited = set()         # List for marking visited and non-visited nodes
    spanning_tree = {}      # Spanning tree
    cycles = []

    # Algorithm outer-loop
    for each in graph:
        # Select a non-visited node
        if each not in visited:
            spanning_tree[each] = None
            # Explore node's connected component
            dfs(each)

    return cycles
