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
    ##### INPUT: tab is np.array of shape (nb_edges,2), v is int : vertex to 'delete'
    del_vert returns a new tab without the edges containing v
    ##### OUTPUT: a new graph like tab but without the edges containing v
    ###   /!\ np.delete returns a copy of the tab without the specified indexes, it doesn't delete on the tab
    """
    size = tab.shape[0]
    idx_2_del = []
    for i in range(size):
        if v in tab[i]:
            idx_2_del.append(i)
    return(np.delete(tab,idx_2_del,0))
