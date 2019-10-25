import sys
import numpy as np

def read_data():
    input_data = sys.stdin
    for line in input_data:
        print(line)
        edge = line.split()
        # print(edge)

read_data()