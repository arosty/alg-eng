import matplotlib.pyplot as plt
import pandas as pd
import sys

# 0: Paul, 1: Alfons

def seconds_per_instance_plot:
    plt.plot([-5, 3, 4])
    plt.ylabel('some numbers')
    plt.show()
current_user = 1
if current_user == 0:
    print('')
elif current_user == 1:
    current_path = 'C:/Users/ARF/Code/arosty/tu_berlin/'
    
current_path += 'alg-eng/history/'
    
current_timestamp = '201910311127'

current_file = current_path + current_timestamp + '_run_history.csv'

data = pd.read_csv(current_file)
