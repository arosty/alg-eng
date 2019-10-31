import sys
import csv

current_path = sys.path[0] + "/"
current_history_file = current_path + "201910302257_run_history."

def get_file_name():
    """
    INPUT: None
    get_file_name returns first line of stdin
    OUTPUT: string
    """
    print(sys.stdin.readline())
    print(type(sys.stdin.readline()))
    return sys.stdin.readline()

print(get_file_name())

def transfer_data():
    """
    INPUT: None
    transfer_data converts data of txt file and writes it into csv file
    (txt and csv file must have same names)
    OUTPUT: None
    """
    current_history_file = sys.path[0] + '/' + get_file_name() + '.csv'
    print(current_history_file)
    # Iterate through every line of txt file:
    for line in sys.stdin:
        for starter in ["random/", "dimacs/", "snap/"]:
            # If row contains statistics:
            if line.startswith(starter):
                # Write data in csv file:
                with open(current_history_file, 'a') as sheet:
                    writer = csv.writer(sheet)
                    writer.writerow(line.split())
                break

transfer_data()

# standard input
# being called automatically