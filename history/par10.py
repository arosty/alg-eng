import sys
import pandas as pd
from datetime import datetime

def calc_par10(path_file_name):
    stats = pd.read_csv(path_file_name + '.csv')
    stats = pd.to_numeric(stats.time_in_seconds.str.rstrip('s'))
    stats.fillna(3000, inplace=True) 
    return sum(stats)


def get_params(path_file_name):
    f = open(path_file_name + '.txt', 'r')
    file_name = f.readline().replace('\n','')
    params = {}
    values = f.readline().split()
    for i in range(len(values)//2):
        params[values[2*i][1:]] = values[2*i+1]
    params = pd.DataFrame(data=params, index=[file_name])
    return params
    

current_path = sys.path[0] + "/"

arguments = sys.argv[1:]
# If csv in function call: save results in csv file
save_csv = 'csv' in sys.argv
if save_csv: arguments.remove('csv')

if sys.stdin.isatty(): file_names = arguments
else: file_names = list(sys.stdin)

list_of_runs = None
for file_name in file_names:
    file_name = file_name.replace('\r\n','')
    print(file_name + ':\n')
    par10_val = calc_par10(current_path + file_name)
    params = get_params(current_path + file_name)
    params['par10'] = [par10_val]
    for param in params.columns:
        if param == 'par10': print('...')
        print(param + ': ' + params[param].to_string(index=False))
    if list_of_runs is None: list_of_runs = params.copy()
    else: list_of_runs = pd.concat([list_of_runs, params], axis=0, join='outer')
    print('-------------------------\n')

if save_csv:
    new_file_name = 'params_par10_' + datetime.now().strftime("%Y%m%d%H%M")
    list_of_runs.to_csv(current_path + new_file_name + '.csv')
