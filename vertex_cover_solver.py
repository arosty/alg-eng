import sys
import numpy as np

def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the given edges
    OUTPUT: np.array of shape (nb_edges,2)
    """
    # Get standard input:
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            # Extract number of edges from first line:
            num_of_edges = np.uint32(line.split()[1])
            # Initialize array of edges:
            edges = np.empty(num_of_edges, dtype=np.ndarray)
        else:
            # Get current edge and convert it to int:
            current_edge = list(map(np.uint32, line.split()))
            # Convert edge to numpy array:
            current_edge = np.asarray(current_edge)
            # Add edge to array of all edges:
            edges[counter-1] = current_edge
    # Return array of edges:
    return edges


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
