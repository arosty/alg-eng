import sys
import numpy as np

def add_vertex(g, vertex):
    g[vertex] = [False, 0, []]
    return g

def add_edge(g, edge):
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
    get_data reads standard input and returns the given edges
    OUTPUT: np.array of shape (nb_edges,2)
    """
    # Get standard input:
    input_data = sys.stdin
    g = {}
    for counter, line in enumerate(input_data):
        if counter > 0:
            # Get current edge and convert it to int:
            # current_edge = list(map(np.uint32, line.split()))
            current_edge = line.split()
            g = add_edge(g, current_edge)
    # Return array of edges:
    return g


def print_result(vertices):
    """
    INPUT: vertices is np.array of shape (nb_vertices,)
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)

        
def del_vert(vertex):
    """
    INPUT: vertex is int : vertex to 'delete'
    del_vert 'deletes' the given vertex and updates the number of edges of all adjacent vertices
    """
    # 'Delete' vertex:
    g[vertex][0] = True
    # Update number of edges on adjacent vertices:
    for adj_vert in g[vertex][2]:
        g[adj_vert][1] -= 1

def un_del_vert(vertex):
    """
    INPUT: vertex is int : vertex to 'undelete'
    un_del_vert 'undeletes' the given vertex and updates the number of edges of all adjacent vertices
    """
    # 'Delete' vertex:
    g[vertex][0] = False
    # Update number of edges on adjacent vertices:
    for adj_vert in g[vertex][2]:
        g[adj_vert][1] += 1

# def is_edgeless(edges):
#     """
#     INPUT: edges is np.array of shape (nb_edges,2)
#     is_edgeless returns True if the graph doesn't have any edges and False otherwise
#     OUTPUT: True or False
#     """
#     return edges.shape[0] == 0

def is_edgeless():
    """
    INPUT: None
    is_edgeless returns True if the graph doesn't have any edges and False otherwise
    OUTPUT: True or False
    """
    for vertex in g:
        if (not g[vertex][0]) and g[vertex][1] > 0:
            return False
    return True


# def get_edge():
#     """
#     INPUT: None
#     get_edge returns the first edge
#     OUTPUT: list of length 2
#     """
#     # Iterate through graph:
#     for vertex in g:
#         # If vertex not deleted and has edges, then take first adjacent vertex and return it:
#         if (not g[vertex][0]) and g[vertex][1] > 0:
#             for adj_vert in g[vertex][2]:
#                 if not g[adj_vert][0]:
#                     return [vertex, adj_vert]

def  highest_degree_vertex():
    """
    INPUT: None
    highest_degree_vertex returns the key to the highest degree vertex, and the list of all it's neigbours which aren't deleted
    OUTPUT: key to index the dictionary, list of neighbours' key 
    """
    key = None
    neighbours = []
    degree_max = -1
    #For every vertex in the dic, we remember its key and neighbours if it has the best degree yet
    for k in g.keys():
        if not g[k][0]:
            if g[k][1]>degree_max:
                degree_max = g[k][1]
                key = k
                neighbours = g[k][2]
    #We have to get rid of the neighbours who have been deleted
    neigh_vert = None
    for i in range (len(neighbours)):
        #pop the first neigbour vertex in the list
        neigh_vert = neighbours.pop(0)
        #if it hasn't been deleted we reinsert it at the end
        if not g[neigh_vert][0]:
            neighbours.append(neigh_vert)
    return(key,neighbours)


def vc_branch(k):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: np.array of shape at most (k,) or None
    """
    vc_branch.counter += 1
    if k < 0:
        return None
    # Return empty array if no edges are given:
    if is_edgeless():
        return np.array([], dtype = np.uint32)
    # Get vertices of first edge:
    [u,v] = get_edge()
    # 'Delete' first vertex from graph:
    del_vert(u)
    # Call function recursively:
    Su = vc_branch(k-1)
    # 'Undelete' first vertex from graph:
    un_del_vert(u)
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        return np.append(Su, u)
    # 'Delete' second vertex from graph:
    del_vert(v)
    # Call function recursively:
    Sv = vc_branch(k-1)
    # 'Undelete' second vertex from graph:
    un_del_vert(v)
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        return np.append(Sv, v)
    return None


def vc():
    """
    INPUT: edges is np.array of shape (nb_edges,2)
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
