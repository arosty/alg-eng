time_stamp=$(date +%Y%m%d%H%M)
file_name="${time_stamp}_run_history"
file_name_path="history/$file_name.txt"
echo $file_name > $file_name_path
echo "benchmark.sh is running..."
bash benchmark.sh >> $file_name_path
cat $file_name_path
file_name_path="history/${time_stamp}_run_history.csv"
echo >> $file_name_path