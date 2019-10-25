import sys
import numpy as np

def read_data():
    input_data = sys.stdin
    print(type(input_data))
    for line in input_data:
        edge = line.split()
        # print(line)

read_data()