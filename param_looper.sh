maxSec=$1

overallTime=$(date +%s);
now=$(date +%s);
elapsed=`expr $now - $overallTime`;

while [$elapsed -le $maxSec]; do
    echo hello
done