import sys
import pandas as pd

def calc_par10(path_file_name):
    stats = pd.read_csv(path_file_name + '.csv')
    stats = pd.to_numeric(stats.time_in_seconds.str.rstrip('s'))
    stats.fillna(3000, inplace=True) 
    return sum(stats)


def get_params(path_file_name):
    f = open(path_file_name + '.txt', 'r')
    print(f.read())
    

current_path = sys.path[0] + "/"

if len(sys.argv) >= 2:
    for file_name in sys.argv[1:]:
        print(file_name + ':')
        par10_val = calc_par10(current_path + file_name)
        print(par10_val)
        print('-------')
    
else:
    for file_name in sys.stdin:
        file_name = file_name.replace("\r\n",'')
        print(file_name + ':')
        par10_val = calc_par10(current_path + file_name)
        print(par10_val)
        get_params(current_path + file_name)
        print('-------')
    # txt file with file names and go through them
