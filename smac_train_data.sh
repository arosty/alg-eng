mv random random_test
mv dimacs dimacs_test
mv snap snap_test
mv random_train random
mv dimacs_train dimacs
mv snap_train snap

echo "100 train"
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '21' -f_clique_lb_c '11' -f_deg2 '29' -f_deg2_heur '6' -f_deg3 '57' -f_dom '32' -f_lp '8' -f_lp_lb '95' -f_lp_lb_c '11' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '311' 
echo "101 train"
bash run.sh -constrained_branching '1' -dom_opt '0' -f_clique_lb '9' -f_clique_lb_c '6' -f_deg2 '10' -f_deg2_heur '6' -f_deg3 '2' -f_dom '9' -f_lp '10' -f_lp_lb '7' -f_lp_lb_c '5' -lb_opt '1' -lb_opt_c '0' -limit_kern_branch '127' -limit_kern_start '440' 
echo "102 train"
bash run.sh --constrained_branching '0' -dom_opt '0' -f_clique_lb '9' -f_clique_lb_c '1' -f_deg2 '5' -f_deg2_heur '3' -f_deg3 '2' -f_dom '5' -f_lp '4' -f_lp_lb '11' -f_lp_lb_c '7' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '329' -limit_kern_start '10' 
echo "103 train"
bash run.sh -constrained_branching '1' -dom_opt '0' -f_clique_lb '15' -f_clique_lb_c '3' -f_deg2 '8' -f_deg2_heur '7' -f_deg3 '8' -f_dom '9' -f_lp '4' -f_lp_lb '11' -f_lp_lb_c '2' -lb_opt '0' -lb_opt_c '0' -limit_kern_branch '8' -limit_kern_start '377'
echo "big train"
bash run.sh -constrained_branching '1' -dom_opt '1' -f_clique_lb '31' -f_clique_lb_c '4' -f_deg2 '32' -f_deg2_heur '65' -f_deg3 '56' -f_dom '58' -f_lp '8' -f_lp_lb '17' -f_lp_lb_c '2' -lb_opt '0' -lb_opt_c '1' -limit_kern_branch '457' -limit_kern_start '356'
echo "1 train"
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '43' -f_clique_lb_c '5' -f_deg2 '92' -f_deg2_heur '85' -f_deg3 '67' -f_dom '75' -f_lp '66' -f_lp_lb '41' -f_lp_lb_c '19' -lb_opt '1' -lb_opt_c '1' -limit_kern_branch '94' -limit_kern_start '148'
echo "2 train"
bash run.sh -constrained_branching '0' -dom_opt '0' -f_clique_lb '13' -f_clique_lb_c '8' -f_deg2 '63' -f_deg2_heur '38' -f_deg3 '28' -f_dom '96' -f_lp '49' -f_lp_lb '41' -f_lp_lb_c '10' -lb_opt '1' -lb_opt_c '1' -limit_kern_branch '150' -limit_kern_start '215'

mv random random_train
mv dimacs dimacs_train
mv snap snap_train