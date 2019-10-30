# TIMESTAMP = $(date +"%Y%m%d%H%M")
# TIMESTAMP="test"
timestamp = $(date +"%Y%m%d%H%M")
bash benchmark.sh > $(timestamp)_run_history.txt
