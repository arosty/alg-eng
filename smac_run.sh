#!/bin/bash

run_ce_solver()
{
	PROGRAMM_NAME="$1"
	maxSecPerInstance=$2
	testFile="$3"

	rm -f time.txt

	overallTime=$(date +%s);
	now=$(date +%s);
	elapsed=`expr $now - $overallTime`;

    # start everything in a new process group such that we can kill everything if necessary
    (setsid /usr/bin/time -f "%e" -a -o time.txt $PROGRAMM_NAME< $testFile 1> prog_out.txt 2>&1) & PID=$!

    # kill processes on exit
    trap "{ kill -$PID 2>/dev/null; }" TERM
    trap "{ kill -9 -$PID 2>/dev/null; }" EXIT

    waited=0
    alive=0
    disown $PID;
    kill -0 $PID 2>/dev/null && alive=1;
    while [ $alive -eq 1 -a $waited -le $maxSecPerInstance ]; do
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

    rm -f prog_out.txt

# 			time=$(cat time.txt | awk '/system/{print $3}' | sed -e 's/elapsed//');
    time=$(cat time.txt);
    verify="";

    if [ "$finished" -eq "1" ]; then
        solFile=${f/input/solution};
        solFile=${solFile/.dimacs/.solution};
        solNumber=$(cat $solFile);
        if [ -n "$solNumber" ] && [ "$solNumber" -eq "$solNumber" ] 2>/dev/null; then
            if [ "$solNumber" -eq "$k" ]; then
                verify="correct";
            else
                verify=">>INCORRECT<<";
            fi
        fi
    fi
    
    echo -e $testFile"\t"$time"s\t"$k"\t"$recursiveSteps"\t"$firstLowerBoundDifference"\t"$highDegreeRules"\t"$degreeZeroRules"\t"$extremeReductionRules"\t"$degreeOneRules"\t"$degreeTwoRules"\t"$dominationRules"\t"$degreeThreeRules"\t"$lowerBounds"\t"$finished"\t"$verify
    echo "" >> $LOG
    
    rm -f time.txt

    now=$(date +%s);
    elapsed=`expr $now - $overallTime`;
}


PROGRAMM_NAME="python3 vertex_cover_solver.py"  	# insert your program here
LOG=log.txt									# specify the name of the log file
maxSecPerInstance=300							# allowed time (in seconds) for one instance

run_ce_solver "$PROGRAMM_NAME" $maxSecPerInstance $testFile




