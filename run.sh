time_stamp=$(date +%Y%m%d%H%M)
file_name="run_history/${time_stamp}_run_history.txt"
echo "benchmark.sh is running..."
bash benchmark > $file_name
cat $file_name