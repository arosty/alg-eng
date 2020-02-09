import random as rd

limit_kern_start = [3, 500] 
limit_kern_branch = [1, 2] #[1, 5, 500] 
f_deg2 = [1, 2] #[1, 3, 50, 500, 40000] 
f_deg2_heur = [1, 80000] 
f_dom = [1, 3, 5] #[1, 3, 50, 500, 40000]
f_deg3 = [1, 5, 10] #[1, 5, 40000]
f_lp = [1, 2] #[1, 5, 40000]
f_clique_lb = [1, 10, 40000]
f_lp_lb = [1, 10, 40000]
lb_opt = 1
f_clique_lb_c = [1, 3, 5, 10] #[1, 5] 
f_lp_lb_c = [1, 3, 5] #[1, 5]
lb_opt_c = [0, 1] #[1]
constrained_branching = [1] #[0, 1]
dom_opt = 1

output = "-constrained_branching {0} -dom_opt {1} -f_clique_lb {2} -f_clique_lb_c {3} -f_deg2 {4} -f_deg2_heur {5} -f_deg3 {6} -f_dom {7} -f_lp {8} -f_lp_lb {9} -f_lp_lb_c {10} -lb_opt {11} -lb_opt_c {12} -limit_kern_branch {13} -limit_kern_start {14}"
x = [rd.choice(constrained_branching), dom_opt, rd.choice(f_clique_lb), rd.choice(f_clique_lb_c), rd.choice(f_deg2), rd.choice(f_deg2_heur), rd.choice(f_deg3), rd.choice(f_dom), rd.choice(f_lp), rd.choice(f_lp_lb), rd.choice(f_lp_lb_c), lb_opt, lb_opt_c, rd.choice(limit_kern_branch), rd.choice(limit_kern_start)]

print (output.format(*x))
