import sys
import numpy as np

def get_data():
    """
    INPUT: None
    Function reads standard input
    OUTPUT: array of all edges
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
            current_edge = list(map(np.uint32, line.split()))     # TODO: maybe convert later to int (in np)
            # Convert edge to numpy array:
            current_edge = np.asarray(current_edge)
            # Add edge to array of all edges:
            edges[counter-1] = current_edge
    # Return array of edges:
    return edges

edges = get_data()

def del_vert(tab,v):
    """
    INPUT: tab is np.array of shape (nb_edges,2), v is int : vertex to 'delete'
    del_vert returns a new tab without the edges containing v
    OUTPUT: a new graph like tab but without the edges containing v
       /!\ np.delete returns a copy of the tab without the specified indexes, it doesn't delete on the tab
    """
    size = tab.shape[0]
    idx_2_del = []
    for i in range(size):
        if v in tab[i]:
            idx_2_del.append(i)
    return(np.delete(tab,idx_2_del,0))


def is_edgeless (tab):
    """
    INPUT: tab is np.array of shape (nb_edges,2)
    for a Graph in tab form returns True if the graph doesn't have any edge
    OUTPUT: True if edgeless
    """
    return(tab.shape[0] == 0) #not sure it's the best way, what do you think?



def vc_branch (tab, k):
    """
    INPUT: tab is a Graph as np.array of shape (nb_edges,2) , k is an integer
    gives a vertex cover of size k if it exists in this graph
    OUTPUT: A vertex cover (np.array) of size at most k, 
            or none if there is no vertex cover of size k.
    """
    if k<0:
        return(None)
    if is_edgeless(tab):
        return(np.array([],dtype = np.uint32))
    [u,v] = tab[0]
    Su = vc_branch(del_vert(tab,u),k-1)
    if Su is not None:
        return (np.append(Su,u))
    Sv = vc_branch(del_vert(tab,v),k-1)
    if Sv is not None:
        return (np.append(Sv,v))
    return(None)