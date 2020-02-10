mv random_test random
mv dimacs_test dimacs
mv snap_test snap

echo "103 train"
bash run.sh -constrained_branching '1' -dom_opt '0' -f_clique_lb '15' -f_clique_lb_c '3' -f_deg2 '8' -f_deg2_heur '7' -f_deg3 '8' -f_dom '9' -f_lp '4' -f_lp_lb '11' -f_lp_lb_c '2' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '377'
echo "big train"
bash run.sh -constrained_branching '1' -dom_opt '1' -f_clique_lb '31' -f_clique_lb_c '4' -f_deg2 '32' -f_deg2_heur '65' -f_deg3 '56' -f_dom '58' -f_lp '8' -f_lp_lb '17' -f_lp_lb_c '2' -lb_opt '0' -lb_opt_c '1' -limit_kern_branch '457' -limit_kern_start '356'
echo "100 train"
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '21' -f_clique_lb_c '11' -f_deg2 '29' -f_deg2_heur '6' -f_deg3 '57' -f_dom '32' -f_lp '8' -f_lp_lb '95' -f_lp_lb_c '11' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '311' 
echo "1 train"
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '43' -f_clique_lb_c '5' -f_deg2 '92' -f_deg2_heur '85' -f_deg3 '67' -f_dom '75' -f_lp '66' -f_lp_lb '41' -f_lp_lb_c '19' -lb_opt '1' -lb_opt_c '1' -limit_kern_branch '94' -limit_kern_start '148'