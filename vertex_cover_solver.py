import sys
import numpy as np

def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the corresponding adjacency matrix
    OUTPUT: np.array of shape (num_of_vertices,num_of_vertices)
    """
    # Get standard input:
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            # Extract number of edges from first line:
            num_of_vertices = np.uint32(line.split()[0][1:])
            # Initialize adjacency matrix:
            adjmat = np.zeros((num_of_vertices, num_of_vertices), np.int8)
        else:
            # Get current edge and convert it to int:
            [u,v] = list(map(np.uint32, line.split()))
            # Add edge to adjacency mat:  ### the -1 is necessary to use the first line and first column of the matrix
            adjmat[u-1, v-1] = 1
            adjmat[v-1, u-1] = 1
    # Return adjacency matrix:
    return adjmat


def print_result(vertices):
    """
    INPUT: vertices is np.array of shape (nb_vertices,)
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)

        
def del_vert(adjmat, vertex):
    """
    INPUT: adjmat is np.array of shape (nb_vertices,nb_vertices), vertex is int : vertex to 'delete'
    del_vert returns adjmat with zeros in line and column of the vertex
    OUTPUT: np.array of shape (nb_vertices,nb_vertices)
       /!\ np.delete returns a copy of the adjmat without the specified indexes, it doesn't delete on the original adjmat
    """
    # create the copy of adjmat:
    newadjmat = np.copy(adjmat)
    (nb_vertices,nb_vertices2) = adjmat.shape
    #write zero in line and column of vertex:
    newadjmat[vertex-1] = np.zeros(nb_vertices)
    newadjmat[:,vertex-1] = np.zeros(nb_vertices)
    #return the newadjmat
    return newadjmat

def is_edgeless(adjmat):
    """
    INPUT: adjmat is np.array of shape (nb_vertices,nb_vertices)
    is_edgeless returns True if the graph doesn't have any edges and False otherwise
    OUTPUT: True or False
    """
    return not np.any(adjmat)


def choose_edge(adjmat):
    """
    INPUT: adjmat is np.array of shape (nb_vertices,nb_vertices)
    gives an existing edge to use in vc_branch
    OUTPUT: (u,v): the vertices number corresponding to the edge found
    """
    #find the number of vertices in the graph
    (nb_vertices,nb_vertices2) = adjmat.shape
    #going through the adjmat upper triangle
    for i in range(nb_vertices):
        for j in range (i):
            #the first edge found is returned
            if adjmat[i,j] == 1:
                return[i+1, j+1]

def vc_branch(adjmat, k):
    """
    adjmat is np.array of shape (nb_vertices,nb_vertices), k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: np.array of shape at most (k,) or None
    """
    vc_branch.counter += 1
    if k < 0:
        return None
    # Return empty array if no edges are given:
    if is_edgeless(adjmat):
        return np.array([], dtype = np.uint32)
    # Get vertices of first edge:
    [u,v] = choose_edge(adjmat)
    # Call function without first vertex
    Su = vc_branch(del_vert(adjmat, u), k-1)
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        return np.append(Su, u)
    # Call function without second vertex:
    Sv = vc_branch(del_vert(adjmat, v), k-1)
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        return np.append(Sv, v)
    return None


def vc(adjmat):
    """
    adjmat is np.array of shape (nb_vertices,nb_vertices)
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    #kmax is the upper bound for k
    kmax = int(adjmat.shape[0] / 2) + 1
    vc_branch.counter = 0
    #try the recursive function for every k until it gives a result or k>kmax
    for k in range (kmax + 1):
        S = vc_branch(adjmat, k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


vc(get_data())
