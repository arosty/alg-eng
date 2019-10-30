import sys

current_path = sys.path[0] + "/"
current_history_file = "201910302031_run_history.txt"

history_file = open(current_path + current_history_file, "r")

print(history_file.read())