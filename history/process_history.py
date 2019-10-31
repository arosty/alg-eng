import sys
import csv

current_path = sys.path[0] + "/"
current_history_file = current_path + "201910302257_run_history."

def transfer_data(current_history_file):
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

transfer_data(current_history_file)

# standard input
# being called automatically