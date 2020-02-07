maxSec=$1
SECONDS=0

while [ $SECONDS -lt $maxSec ]; do
    python3 random_config.py > params.txt
    # rm -f params.txt
done