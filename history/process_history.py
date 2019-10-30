import sys

current_path = sys.path[0] + "/"
current_history_file = "201910302031_run_history."

history_file = open(current_path + current_history_file + "txt", "r")

for line in history_file:
    # print("NEUE ZEILE")
    # print(line)
    # if line starts with random, snap or dimacs
    # line.split()
    with open(current_path + current_history_file + "csv", "a") as sheet:
        sheet.write(line.split())
