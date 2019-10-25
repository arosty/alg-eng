import sys
import numpy as np

def read_data():
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            print("special: " + line[-1])
        else:
            print(line)
        edge = line.split()
        # print(edge)

read_data()