import sys
import numpy as np

def read_data():
    input_data = sys.stdin
    print(input_data[0])
    for line in input_data:
        edge = line.split()
        # print(line)

read_data()