import sys
import csv

current_path = sys.path[0] + "/"
current_history_file = current_path + "201910302257_run_history."

def get_file_name():
    """
    INPUT: None
    get_data reads standard input and returns the given edges
    OUTPUT: np.array of shape (nb_edges,2)
    """
    return input()

print(get_file_name)

def transfer_data(current_history_file):
    """
    INPUT: current_history_file is string
    transfer_data converts data of txt file and writes it into csv file
    (txt and csv file must have same names)
    OUTPUT: None
    """
    # Read txt file:
    history_file = open(current_history_file + 'txt', 'r')
    # Iterate through every line of txt file:
    for line in history_file:
        for starter in ["random/", "dimacs/", "snap/"]:
            # If row contains statistics:
            if line.startswith(starter):
                # Write data in csv file:
                with open(current_history_file + 'csv', 'a') as sheet:
                    writer = csv.writer(sheet)
                    writer.writerow(line.split())
                break

# transfer_data(current_history_file)

# standard input
# being called automatically