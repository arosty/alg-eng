mv random random_test
mv dimacs dimacs_test
mv snap snap_test

mv random_train random
mv dimacs_train dimacs
mv snap_train snap

bash run.sh -constrained_branching '1' -dom_opt '1' -f_clique_lb '1' -f_clique_lb_c '1' -f_deg2 '1' -f_deg2_heur '1' -f_deg3 '1' -f_dom '1' -f_lp '1' -f_lp_lb '1' -f_lp_lb_c '1' -lb_opt '1' -lb_opt_c '1' -limit_kern_branch '500' -limit_kern_start '500'

git add .
git commit -m "training run"
git push origin smac-testing

mv random random_train
mv dimacs dimacs_train
mv snap snap_train

mv random_test random
mv dimacs_test dimacs
mv snap_test snap

bash run.sh -constrained_branching '1' -dom_opt '1' -f_clique_lb '1' -f_clique_lb_c '1' -f_deg2 '1' -f_deg2_heur '1' -f_deg3 '1' -f_dom '1' -f_lp '1' -f_lp_lb '1' -f_lp_lb_c '1' -lb_opt '1' -lb_opt_c '1' -limit_kern_branch '500' -limit_kern_start '500'

git add .
git commit -m "testing run"
git push origin smac-testing