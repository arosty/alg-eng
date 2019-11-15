import sys
import numpy as np

def add_vertex(g, vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    g[vertex] = [False, 0, []]
    return g


def add_edge(g, edge):
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
    return g


def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the given graph
    OUTPUT: np.array of shape (nb_edges,2)
    """
    # Get standard input:
    input_data = sys.stdin
    g = {}
    for counter, line in enumerate(input_data):
        if counter > 0:
            # Get current edge and add it to the graph:
            current_edge = line.split()
            g = add_edge(g, current_edge)
    # Return graph:
    return g


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


def get_neighbor(vertex):
    """
    INPUT: vertex is str
    get_neighbor returns the first neighbor
    OUTPUT: str
    """
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            return neighbor


def get_degree_one_neighbors():
    """
    INPUT: None
    get_degree_one_neighbors return the neighbors of all vertices of degree one
    (if two vertices of degree one are adjacent to each other, it choses one of them)
    OUTPUT: list
    """
    neighbors = []
    for vertex in g:
        if (not g[vertex][0]) and g[vertex][1] == 1 and (vertex not in neighbors):
            neighbor = get_neighbor(vertex)
            if neighbor not in neighbors:
                neighbors.append(neighbor)
    return neighbors


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
    # Get neighbors of vertices with degree one (if two are adjacent to each other, only one of them):
    degree_one_neighbors = get_degree_one_neighbors()
    # 'Delete' neighbors of degree one vertices:
    del_vert(degree_one_neighbors)
    # Reduce k according to new vertices:
    k -= len(degree_one_neighbors)
    # Return one degree neighbors list if no edges left:
    if is_edgeless():
        # 'Undelete' neighbors of degree one vertices:
        un_del_vert(degree_one_neighbors)
        if k < 0:
            return None
        return degree_one_neighbors
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
        un_del_vert(degree_one_neighbors)
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
        un_del_vert(degree_one_neighbors)
        Sv.append(v)
        return Sv
    return None


def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    vc_branch.counter = 0
    # Try the recursive function for every k until it gives a result or k>kmax
    for k in range(len(g)):
        S = vc_branch(k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


g = get_data()
vc()
