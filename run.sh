time_stamp=$(date +%Y%m%d%H%M)
file_name="history/${time_stamp}_run_history.txt"
echo "benchmark.sh is running..."
bash benchmark.sh > $file_name
cat $file_name
file_name="history/${time_stamp}_run_history.csv"
echo >> $file_name