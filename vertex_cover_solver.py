import sys
import numpy as np

def get_data():
    # Get standard input:
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            # Get number of vertices in the graph:
            nb_vertices = np.uint32(line.split()[0][1:])
            print(nb_vertices)
            break

get_data()