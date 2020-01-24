PROGRAMM_NAME="python3 ../vertex_cover_solver.py"
INSTANCE="$1"
SPECIFICS=$2
runTimeCutOff=$3
runLength=$4
seed=$5

LOG=log.txt

rm -f time.txt

overallTime=$(date +%s);
now=$(date +%s);
elapsed=`expr $now - $overallTime`;

echo $INSTANCE >> $LOG

# start everything in a new process group such that we can kill everything if necessary
(setsid /usr/bin/time -f "%e" -a -o time.txt $PROGRAMM_NAME< $INSTANCE 1> prog_out.txt 2>&1) & PID=$!

# kill processes on exit
trap "{ kill -$PID 2>/dev/null; }" TERM
trap "{ kill -9 -$PID 2>/dev/null; }" EXIT

waited=0
alive=0
disown $PID;
kill -0 $PID 2>/dev/null && alive=1;
while [ $alive -eq 1 -a $waited -le $runTimeCutOff ]; do
    sleep 2;
    (( waited += 2 ));
    kill -0 $PID 2>/dev/null || alive=0
done
if [ $alive -eq 1 ]; then
    # process still exists, kill it softly, then brutally, if necessary
    kill -TERM -$PID 2>/dev/null; sleep 1; kill -9 -$PID 2>/dev/null;
    finished=0;
else
    finished=1;
fi

cat prog_out.txt >> $LOG

rm -f prog_out.txt

time=$(cat time.txt);

echo "Result for SMAC: SUCCESS, $time, 0, 0, $seed"
echo "" >> $LOG

rm -f time.txt