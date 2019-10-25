import sys
import numpy as np

def get_data():
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            num_of_edges = int(line.split()[1])
            edges = np.empty(num_of_edges, dtype=np.ndarray)
        else:
            current_edge = list(map(int, line.split()))     # TODO: maybe convert later to int (in np)
            current_edge = np.asarray(current_edge)
            edges[counter-1] = current_edge
    return edges

read_data()