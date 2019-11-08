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
            edges = np.empty(num_of_edges, dtype=list)
        else:
            # Get current edge and convert it to int:
            current_edge = list(map(np.uint32, line.split()))
            # Add edge to array of all edges:
            edges[counter-1] = [current_edge, False]
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
    INPUT: edges is np.array of shape (nb_edges,2), vertex is int : vertex to 'delete'
    del_vert returns all edges except the ones containing vertex
    OUTPUT: np.array of shape (nb_edges_after_del,2)
       /!\ np.delete returns a copy of the edges without the specified indexes, it doesn't delete on the edges
    """
    # Get number of edges:
    size = edges.shape[0]
    for i in range(size):
        # If edge contains vertex append the index to list
        if vertex in edges[i]:
            edges[i][2] = True


def un_del_vert(vertex):
    """
    INPUT: edges is np.array of shape (nb_edges,2), vertex is int : vertex to 'delete'
    del_vert returns all edges except the ones containing vertex
    OUTPUT: np.array of shape (nb_edges_after_del,2)
       /!\ np.delete returns a copy of the edges without the specified indexes, it doesn't delete on the edges
    """
    # Get number of edges:
    size = edges.shape[0]
    for i in range(size):
        # If edge contains vertex append the index to list
        if vertex in edges[i]:
            edges[i][2] = False


def is_edgeless():
    """
    INPUT: edges is np.array of shape (nb_edges,2)
    is_edgeless returns True if the graph doesn't have any edges and False otherwise
    OUTPUT: True or False
    """
    for edge in edges:
        if not edge[2]:
            return False
    return True


def get_edge():
    for edge in edges:
        if not edge[2]:
            return edge[0:2]


def vc_branch(k):
    """
    INPUT: edges is np.array of shape (nb_edges,2), k is int
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
    # Call function without first vertex
    del_vert(u)
    Su = vc_branch(k-1)
    un_del_vert(u)
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        return np.append(Su, u)
    # Call function without second vertex:
    del_vert(v)
    Sv = vc_branch(k-1)
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
    #kmax is the upper bound for k
    kmax = int(edges.shape[0] / 2) + 1
    vc_branch.counter = 0
    #try the recursive function for every k until it gives a result or k>kmax
    for k in range (kmax + 1):
        S = vc_branch(k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


edges = get_data()
vc()
