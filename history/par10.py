import sys
import pandas as pd

def give_par10(path_file_name):
    stats = pd.read_csv(path_file_name + '.csv')
    return stats
    

current_path = sys.path[0] + "/"

if len(sys.argv) >= 2:
    for file_name in sys.argv[1:]:
        stats = give_par10(current_path + file_name)
        print(stats)
        # print par10
    
else:
    pass
    # txt file with file names and go through them
