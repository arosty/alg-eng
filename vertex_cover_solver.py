import sys
import numpy as np

def add_vertex(vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    g[vertex] = [False, 0, []]


def add_edge(edge):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), edge is list of length 2
    add_vertex adds a new edge to the graph and returns this graph
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    for vertex in edge:
        if not vertex in g.keys():
            g = add_vertex(g, vertex)
        g[vertex][1] += 1
    g[edge[0]][2].append(edge[1])
    g[edge[1]][2].append(edge[0])


def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the given graph
    OUTPUT: np.array of shape (nb_edges,2)
    """
    # Get standard input:
    input_data = sys.stdin
    global g
    g = {}
    for counter, line in enumerate(input_data):
        if counter > 0:
            # Get current edge and add it to the graph:
            current_edge = line.split()
            g = add_edge(current_edge)


def print_result(vertices):
    """
    INPUT: vertices is np.array of shape (nb_vertices,)
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)

        
def del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'delete'
    del_vert 'deletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    for vertex in vertices:
        # 'Delete' vertex:
        g[vertex][0] = True
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            g[adj_vert][1] -= 1


def un_del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'undelete'
    un_del_vert 'undeletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    for vertex in vertices:
        # 'Delete' vertex:
        g[vertex][0] = False
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            g[adj_vert][1] += 1


def is_edgeless():
    """
    INPUT: None
    is_edgeless returns True if the graph doesn't have any undeleted edges and False otherwise
    OUTPUT: True or False
    """
    # For every vertex in the graph, check if it has adjacent vertices that are undeleted:
    for vertex in g:
        if (not g[vertex][0]) and g[vertex][1] > 0:
            return False
    return True


def get_edge():
    """
    INPUT: None
    get_edge returns the first edge
    OUTPUT: list of length 2
    """
    # Iterate through graph:
    for vertex in g:
        # If vertex not deleted and has edges, then take first adjacent vertex and return it:
        if (not g[vertex][0]) and g[vertex][1] > 0:
            for adj_vert in g[vertex][2]:
                if not g[adj_vert][0]:
                    return [vertex, adj_vert]


def vc_branch(k):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: list of length at most k or None
    """
    vc_branch.counter += 1
    if k < 0:
        return None
    # Return empty list if no edges are given:
    if is_edgeless():
        return []
    # Get vertices of first edge:
    [u,v] = get_edge()
    # 'Delete' first vertex from graph:
    del_vert([u])
    # Call function recursively:
    Su = vc_branch(k-1)
    # 'Undelete' first vertex from graph:
    un_del_vert([u])
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        Su.append(u)
        return Su
    # 'Delete' second vertex from graph:
    del_vert([v])
    # Call function recursively:
    Sv = vc_branch(k-1)
    # 'Undelete' second vertex from graph:
    un_del_vert([v])
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        Sv.append(v)
        return Sv
    return None


def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    # Set upper bound for k:
    kmax = len(g) // 2 + 1
    vc_branch.counter = 0
    # Try the recursive function for every k until it gives a result or k>kmax
    for k in range (kmax + 1):
        S = vc_branch(k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


g = get_data()
vc()
