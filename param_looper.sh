maxSec=$1
SECONDS=0

while [ $SECONDS -lt $maxSec ]; do
    python3 random_config.py > params.txt
    parameters=$(<params.txt)
    rm -f params.txt
    bash run.sh $parameters
done