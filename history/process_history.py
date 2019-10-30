import sys
import csv

current_path = sys.path[0] + "/"
current_history_file = "201910302031_run_history."

history_file = open(current_path + current_history_file + 'txt', 'r')

for line in history_file:
    if line[:4] in ["rand", "dima", "snap"]:
        with open(current_path + current_history_file + 'csv', 'a') as sheet:
            writer = csv.writer(sheet)
            writer.writerow(line.split())
