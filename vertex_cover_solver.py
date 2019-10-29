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
            current_edge = list(map(np.uint32, line.split()))     # TODO: maybe convert later to int (in np)
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