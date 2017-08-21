max_dist_in_a_DAG.py is Python library that provides interfaces to build a Graph and can compute the maximum path length from the root node to the most distant remote node under the no-loops assumption (directed acyclic graph).

Graph object provides following interfaces:
* addEdge -> to build a graph
* topologicalSort -> sort DAG in topological order from given source. That method also detects loops in a graph and throws an exception.
* calculateDistances -> calculate distances for all nodes in topological order.
* maxPath -> find node with the longest distance and reconstruct path from it up to a given source


Time complexity is linear: 
* topologicalSort -> O(V+E) 
* calculateDistance -> O(E) runs a loop for all adjacent vertices  
* maxPath -> O(V+V) runs a loop for all vertices to find most distant node plus another loop to reconstruct a path. 
Therefore, overall time complexity of this algorithm is O(V+E).


TestGraph.jpg is a visual representation of the DAG used in the test driver.

to run tests:<br />
$ max_dist_in_a_DAG.py --test 
