import sys
import numpy as np

def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the incidence list
    OUTPUT: dictionary like {vertex : neighbour vertices}
    """
    # Get standard input:
    input_data = sys.stdin
    # Initialize incidence list:
    G = {}
    for counter, line in enumerate(input_data):
        if counter == 0:
            # Extract number of edges from first line:
            num_of_edges = np.uint32(line.split()[1])
        else:
            # Get current edge and convert it to int list:
            [u,v] = list(map(np.uint32, line.split()))
            #insert vertices where needed
            try:
                G[u][1] +=1
                G[u][2].append(v)
            except :
                G[u] = [False,1,[v]]

            try:
                G[v][1] +=1
                G[v][2].append(u)
            except :
                G[v] = [False,1,[u]]
            
    # Return incidence list:
    return (G,num_of_edges) 

print(get_data()) 

def print_result(vertices):
    """
    INPUT: vertices is np.array of shape (nb_vertices,)
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)

        
def del_vert(edges, vertex):
    """
    INPUT: edges is np.array of shape (nb_edges,2), vertex is int : vertex to 'delete'
    del_vert returns all edges except the ones containing vertex
    OUTPUT: np.array of shape (nb_edges_after_del,2)
       /!\ np.delete returns a copy of the edges without the specified indexes, it doesn't delete on the edges
    """
    # Get number of edges:
    size = edges.shape[0]
    # Initialize list of indices which will be deleted
    idx_del = []
    for i in range(size):
        # If edge contains vertex append the index to list
        if vertex in edges[i]:
            idx_del.append(i)
    # Return array of edges without the ones deleted:
    return np.delete(edges, idx_del, 0)


def is_edgeless(edges):
    """
    INPUT: edges is np.array of shape (nb_edges,2)
    is_edgeless returns True if the graph doesn't have any edges and False otherwise
    OUTPUT: True or False
    """
    return edges.shape[0] == 0


def vc_branch(edges, k):
    """
    INPUT: edges is np.array of shape (nb_edges,2), k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: np.array of shape at most (k,) or None
    """
    vc_branch.counter += 1
    if k < 0:
        return None
    # Return empty array if no edges are given:
    if is_edgeless(edges):
        return np.array([], dtype = np.uint32)
    # Get vertices of first edge:
    [u,v] = edges[0]
    # Call function without first vertex
    Su = vc_branch(del_vert(edges, u), k-1)
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        return np.append(Su, u)
    # Call function without second vertex:
    Sv = vc_branch(del_vert(edges, v), k-1)
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        return np.append(Sv, v)
    return None


def vc(edges):
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
        S = vc_branch(edges, k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


#vc(get_data())
