maxSec=$1
SECONDS=0

bash run.sh -constrained_branching '1' -dom_opt '0' -f_clique_lb '15' -f_clique_lb_c '3' -f_deg2 '8' -f_deg2_heur '7' -f_deg3 '8' -f_dom '9' -f_lp '4' -f_lp_lb '11' -f_lp_lb_c '2' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '377' 
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '9' -f_clique_lb_c '1' -f_deg2 '5' -f_deg2_heur '3' -f_deg3 '2' -f_dom '5' -f_lp '4' -f_lp_lb '11' -f_lp_lb_c '7' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '329' -limit_kern_start '10' 
bash run.sh -constrained_branching '1' -dom_opt '0' -f_clique_lb '9' -f_clique_lb_c '6' -f_deg2 '10' -f_deg2_heur '6' -f_deg3 '2' -f_dom '9' -f_lp '10' -f_lp_lb '7' -f_lp_lb_c '5' -lb_opt '1' -lb_opt_c '0' -limit_kern_branch '127' -limit_kern_start '440' 
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '21' -f_clique_lb_c '11' -f_deg2 '29' -f_deg2_heur '6' -f_deg3 '57' -f_dom '32' -f_lp '8' -f_lp_lb '95' -f_lp_lb_c '11' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '311' 

while [ $SECONDS -lt $maxSec ]; do
    python3 random_config.py > params.txt
    parameters=$(<params.txt)
    rm -f params.txt
    bash run.sh $parameters
done