
import sys
import argparse
import traceback

#class Node:
#   def __init__(self, children):
#       self.children = children

# Graph is represented via adjacency list. 
class Graph:

    # Constants used to classify edges 
    TEMPORARY = 1
    PERMANENT = 2

    def __init__(self):
        # Dictionary containing adjacency List
        self.graph = {}

    # Function to add an edge to the graph
    def addEdge(self,u,v):
        if self.graph.has_key(u):
            self.graph[u].append(v)
        else:    
            self.graph[u] = [v]

        if not self.graph.has_key(v):
            self.graph[v] = []

    # A recursive function used by topologicalSort
    # depth-first search terminates when it hits any node 
    # that has already been visited since the beginning of the topological sort 
    # or the node has no outgoing edges (i.e. a leaf node):
    def dfs(self,v,visited,stack):
        if visited.has_key(v):
            if visited[v] == self.PERMANENT: return
            # make sure there are no loops 
            else: raise Exception('This graph is not a DAG. Unable to proceed :(')

        visited[v] = self.TEMPORARY
        # Visit all the vertices adjacent to the current one
        if v in self.graph.keys():
            for node in self.graph[v]:
                self.dfs(node,visited,stack)
        visited[v] = self.PERMANENT
        # Add current node to list that stores vertices in topological order
        stack.append(v)

    # DFS based topological sort
    def topologicalSort(self, source):
        if not self.graph.has_key(source): raise Exception('Source vertice does not exist')
        # All the vertices are not visited
        visited = {}
        stack = []
        # Call the recursive helper function to store Topological
        # Sort starting from source vertice
        for i in range(len(self.graph)):
            self.dfs(source,visited,stack)
        return stack

    # Calculate all distances from the source
    def calculateDistances(self, source):        
        # store elements as {distance,source_vertex} tuple
        # where,
        #   distance ::= is a longest calculated distance from given node
        #   source_vertex ::= back reference to a parent vertex that can be used to reconstruct the longest path
        dist = {}

        # Set distance to source as 0 and reference to parent vertex as None (aka root)
        dist[source] = (0,None)

        # Get DAG sorted in topological order 
        stack = self.topologicalSort(source)
 
        # Process vertices in topological order
        while stack:
            # Get the next vertex from topological order
            v = stack.pop()
            #print v, self.graph[v]
            # For all adjacent vertices:
            for node in self.graph[v]:
                # Initialize distances as -1 (infinite) when vertice has no distance preset
                if not dist.has_key(node):
                    dist[node] = (-1, None)
                if not dist.has_key(v):
                    dist[v] = (-1, None)
                # Modify distance when new distance is bigger 
                # Also update back reference to current parent
                if dist[node][0] < dist[v][0] + 1:
                    dist[node] = (dist[v][0] + 1, v)
        return dist

    # find node with longest distance and reconstruct path 
    def maxPath(self, source):
        distances = self.calculateDistances(source)
        far_node = None
        far_distance = -1

        # Find most distant node
        for node, (d, _p) in distances.iteritems():
            if d > far_distance:
                far_node = node
                far_distance = d

        # Reconstruct path back to source node
        path = []
        while not far_node == None:
            source = distances[far_node][1]
            target = far_node
            path.append((source,target))
            far_node = source
        path.reverse()
        return path

def test(g, node, expected):
    print '-'*60
    print 'Topological order from node "%s"' % node
    print g.topologicalSort(node)
    print 'Calculated distances from node "%s"' % node
    print g.calculateDistances(node)
    print 'Longest path from node "%s" to most distant node' % node
    mp = g.maxPath(node)
    print g.maxPath(node)
    assert(mp == expected)

def testDrive():
    g = Graph()
    g.addEdge('a', 1)
    g.addEdge('a', 2)
    g.addEdge(1, 3)
    g.addEdge(1, 2)
    g.addEdge(2, 4)
    g.addEdge(2, 5)
    g.addEdge(2, 3)
    g.addEdge(3, 4)
    g.addEdge(3, 6)
    g.addEdge(4, 5)
    g.addEdge(6, 7)
    g.addEdge(6, 4)
    g.addEdge(4, 7)
    g.addEdge(7, 8)
    g.addEdge(8, 'b')
    g.addEdge(5, 'b')

    test(g, 'a', [(None, 'a'), ('a', 1), (1, 2), (2, 3), (3, 6), (6, 4), (4, 7), (7, 8), (8, 'b')])
    test(g, 6, [(None, 6), (6, 4), (4, 7), (7, 8), (8, 'b')])
    test(g, 'b', [(None, 'b')])

    # negative test for dummy node, should raise 'not exist' exception
    try:
        test(g, 'c', [(None, 'b')])
    except:    
        traceback.print_exc(file=sys.stderr)
    
    # Adding loop and make sure prorgam bails out with exception 
    print '-'*60
    print 'Adding loop into DAG to make sure we can detect it and throw exception'
    g.addEdge(8, 6)
    try:
        print g.maxPath('a')
    except:    
        # Oops caught some Not a DAG! DAG literally means FISH in Hebrew :)
        traceback.print_exc(file=sys.stderr)


    print '-'*60
    print 'We still sohuld be able to get max path from last node since it is out of loop.'
    test(g, 'b', [(None, 'b')])
    print '='*60
    print 'All set. See you soon!'

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='run some regression tests')
    args, unknown = parser.parse_known_args()

    if args.test: testDrive()

except Exception, e:
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

sys.exit(0)


