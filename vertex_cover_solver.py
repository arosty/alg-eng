from __future__ import print_function

import sys
import cplex
from cplex.exceptions import CplexError

g = {}
max_degree = 0
degree_list = []
nb_vertices = 0
nb_edges = 0

#max number of kernelization loops allowed for preproccesing kern
limit_kern_start = float('inf')
#max number of kernelization loops allowed while branching
limit_kern_branch = float('inf')
#reduction rules' frequencies
f_deg2 = 1
f_dom = 1
f_deg3 = 1
f_lp = 1
f_bound = 1
#if True, second method of branching is used
constrained_branching = False
#if True, domination rule works with flags
dom_opt = True

def add_vertex(vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    global dom_opt
    if dom_opt: g[vertex] = [False, 0, [], True]
    else: g[vertex] = [False, 0, []]


def add_edge(edge):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), edge is list of length 2
    add_vertex adds a new edge to the graph and returns this graph
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    global max_degree
    global nb_edges
    if edge[0] in g and edge[1] in g[edge[0]][2]: return
    #Increment edge counter
    nb_edges += 1
    #add edge in dictionary
    for vertex in edge:
        if not vertex in g.keys():
            add_vertex(vertex)
        g[vertex][1] += 1
        # If current degree is greater than maximum degree, update:
        if g[vertex][1] > max_degree:
            max_degree += 1
    g[edge[0]][2].append(edge[1])
    g[edge[1]][2].append(edge[0])


def get_data():
    """
    INPUT: None
    get_data reads standard input and creates the given graph
    OUTPUT: None
    """
    global degree_list
    global nb_vertices
    # Get standard input:
    input_data = sys.stdin
    for line in input_data:
        if not line[0] == '#':
            # Get current edge and add it to the graph:
            current_edge = line.split()
            add_edge(current_edge)
    nb_vertices = len(g)
    # Initializing degree_list:
    nb_vertices = len(g)
    degree_list = [[] for i in range(nb_vertices)]
    for vertex in g:
        degree = g[vertex][1]
        # Append vertex to the list located at its degree in degree_list:
        degree_list[degree].append(vertex)


def print_result(vertices):
    """
    INPUT: vertices is list : vertices
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)

        
def del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'delete'
    del_vert 'deletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    global dom_opt
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in vertices:
        # 'Delete' vertex:
        ###Deleting in g
        g[vertex][0] = True
        if dom_opt: g[vertex][3] = True
        nb_vertices -= 1
        ###Deleting in degree_list and updating nb_edges
        degree_vertex = g[vertex][1]
        nb_edges -= degree_vertex
        degree_list[degree_vertex].remove(vertex)
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            ###Updating g
            g[adj_vert][1] -= 1
            if not g[adj_vert][0]:
                if dom_opt: g[adj_vert][3] = True
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert+1].remove(adj_vert)
                degree_list[degree_adj_vert].append(adj_vert)
    #If max_degree is obsolete, go through all degrees decreasing from max_degree to find the new value
    while (max_degree > 0) & (degree_list[max_degree] == []):
        max_degree -= 1

def un_del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'undelete'
    un_del_vert 'undeletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    global dom_opt
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in vertices:
        # 'Undelete' vertex:
        ###Undeleting in g
        g[vertex][0] = False
        nb_vertices += 1
        ###Undeleting in degree_list and updating nb_edges
        degree_vertex = g[vertex][1]
        nb_edges += degree_vertex
        degree_list[degree_vertex].append(vertex)
        # If the vertex has a higher degree than max_degree, we update max_degree
        if g[vertex][1] > max_degree:
            max_degree = g[vertex][1]
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            ###Updating g
            g[adj_vert][1] += 1
            if not g[adj_vert][0]:
                if dom_opt: g[adj_vert][3] = True
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert-1].remove(adj_vert)
                degree_list[degree_adj_vert].append(adj_vert)
                #If the neighbor has after undeletion a higher degree than max degree we update it
                if g[adj_vert][1] > max_degree:
                    max_degree = g[adj_vert][1]


def is_edgeless():
    """
    INPUT: None
    is_edgeless returns True if the graph doesn't have any undeleted edges and False otherwise
    OUTPUT: True or False
    """
    return max_degree == 0


def get_highest_degree_vertex():
    """
    INPUT: None
    highest_degree_vertex returns the the highest degree vertex, and the list of all it's neigbors which aren't deleted
    OUTPUT: index of the dictionary : highest degree vertex, list : neighbors of highest degree vertex
    """
    # Get highest degree vertex:
    high_deg_vertex = degree_list[max_degree][0]
    # Initialize list of its neighbors:
    neighbors = []
    # Iterate through potential neighbors and add each on that is not deleted to the neighbor list:
    for neighbor in g[high_deg_vertex][2]:
        if not g[neighbor][0]:
            neighbors.append(neighbor)
    return [high_deg_vertex], neighbors


def get_neighbor(vertex):
    """
    INPUT: vertex is str
    get_neighbor returns the first neighbor
    OUTPUT: str
    """
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            return neighbor


def test_clique(vertex,clique):
    """
    INPUT: vertex, clique: list[vertices]
    For a vertex and a clique, returns True if the vertex and the existing clique form a clique
    OUTPUT, Bool
    """
    # For every vertex v in the clique:
    for v in clique:
        # If vertex is not a neighbor of v, vertex is not in the vertex cover:
        if vertex not in g[v][2]:
            return False
    # If vertex is a neighbor of all the vertices in the clique, return True:
    return True


def inspect_vertex(vertex):
    """
    INPUT: vertex to assign to a clique
    Appends vertex to the best existing clique possible in clique_list
    OUTPUT: None
    """
    global clique_list
    nb_cliques = len(clique_list)
    best_clique_index = -1
    best_clique_size = 0
    # For every clique already created in clique_list:
    for i in range (nb_cliques):
        clique_size = len(clique_list[i])
        # If vertex can be added to this clique and this clique is bigger than the best one we found yet:
        if (test_clique(vertex, clique_list[i])) & (clique_size > best_clique_size):
            # Remember this clique's index and size:
            best_clique_index = i
            best_clique_size = clique_size
    # If we didn't find any clique to add vertex in, we create one containing vertex:
    if best_clique_index == -1:
        clique_list.append([vertex])
    # Else we add vertex to the best clique possible:
    else: 
        clique_list[best_clique_index].append(vertex)


def bound():
    """
    INPUT: None
    bound returns a lower bound using clique cover, starting by smallest degree
    OUTPUT: int
    """
    global clique_list
    clique_list = []
    for list_degree_i in degree_list:
        for vertex in list_degree_i:
            inspect_vertex(vertex)
    return nb_vertices - len(clique_list)


def append_to_S(S, vertices):
    for vertex in vertices:
        if type(vertex) is str:
            S.append(vertex)
        else:
            v, u, w = vertex
            S = del_from_S(S,[v])
            for x in [u, w]:
                S = append_to_S(S, [x])
    return S


def del_from_S(S, vertices):
    for vertex in vertices:
        if type(vertex) is str:
            S.remove(vertex)
        else:
            v, u, w = vertex
            S = append_to_S(S, [v])
            for x in [u, w]:
                S = del_from_S(S, [x])
    return S


def high_degree_rule(k):
    """
    INPUT: k
    high_degree_rule executes the high-degree reduction rule (if a vertex has a higher degree than k, it gets added to the vertex cover)
    OUTPUT: list : additional vertices for the vertex cover, list : vertices that need to be undeleted later again, int : new k
    """
    S_kern = []
    while k >= 0 and max_degree > k:
        high_degree_vertex = degree_list[max_degree][0]
        del_vert([high_degree_vertex])
        S_kern.append(high_degree_vertex)
        k -= 1
    if S_kern != []:
        high_degree_rule.counter += 1
    undelete = S_kern[:]
    return S_kern, undelete, k


def degree_zero_rule():
    """
    INPUT: None
    degree_zero_rule deletes all degree zero vertices and returns them
    OUTPUT: list
    """
    if degree_list[0] != []:
        degree_zero_rule.counter += 1
        undelete = degree_list[0][:]
        del_vert(undelete)
    else: undelete = []
    return undelete


def extreme_reduction_rule(k):
    """
    INPUT: k
    extreme_reduction_rule executes the high-degree and zero-degree reduction rules and checks if the k is still high enough (rule)
    OUTPUT: OUTPUT: list : additional vertices for the vertex cover, list : vertices that need to be undeleted later again, int : new k
    """
    # Execute high-degree reduction rule:
    S_kern, undelete, k = high_degree_rule(k)
    # Execute degree-zero reduction rule:
    undelete += degree_zero_rule()
    # Check if k high enough, if not, set k to -1
    if nb_vertices > k ** 2 + k or nb_edges > k ** 2:
        extreme_reduction_rule.counter += 1
        k = -1
    return S_kern, undelete, k


def starter_reduction_rule():
    """
    INPUT: None
    starter_reduction_rule gives a lower bound for k according to the reduction rule
    OUTPUT: int
    """
    return int(.5 * max(-1 + (1 + 4 * nb_vertices) ** .5, 2 * nb_edges ** .5) + 0.999)


def get_all_neighbors(vertex):
    """
    INPUT: vertex
    get_neighbor returns the first neighbor
    OUTPUT: list of vertices
    """
    neighbors = []
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]: neighbors.append(neighbor)
    return neighbors


def merge_vert(vertex, u, w):
    """
    INPUT: vertex of degree 2, and its two neighbors u and w
    to use only if vertex has degree 2 and there is no edge between u and w
    merges vertex and its 2 neighbors, but doesn't change k 
    OUTPUT: the name of the resulting merged_point
    """
    global nb_vertices
    global degree_list
    global max_degree
    merged_point = (vertex, u, w)
    del_vert([vertex, u, w])
    if merged_point in g:
        un_del_vert([merged_point])
        return merged_point
    #add merged vertex and delete vertex and its neighbors
    add_vertex(merged_point)
    nb_vertices += 1
    #add edges towards every neighbor only once 
    for z in [u, w]:
        for n in g[z][2]:
            if n not in g[merged_point][2]:
                if not g[n][0]:
                    add_edge([merged_point, n])
                    n_degree = g[n][1]
                    degree_list[n_degree-1].remove(n)
                    degree_list[n_degree].append(n)
                else:
                    #add edge in dictionary
                    g[merged_point][2].append(n)
                    g[n][2].append(merged_point)
                    g[n][1] += 1
    degree_list[g[merged_point][1]].append(merged_point)
    return merged_point


def un_merge_vert(merged_points):
    """
    INPUT: list of result vertices of a merge that must be 'v u w'
    cancels the merge that resulted in the vertices of merged_points, but doesn't change k 
    OUTPUT: None
    """        
    for merged_point in reversed(merged_points):
        (vertex, u, w) = merged_point
        del_vert([merged_point])
        un_del_vert([vertex, u, w])


def degree_one_rule(k):
    """
    INPUT: k is int 
    degree_one_rule deletes all degree one vertices and returns them, deletes all 
    of their neighbors and return them to add them to S. also returns the depth budget k changed by deletion
    OUTPUT: S_kern is list of vertices, undeleteis list of vertices, k is int
    """
    S_kern, undelete = [],[]
    while degree_list[1] != [] and k >= 0:
        degree_one_rule.counter += 1
        # Get vertex with degree one:
        vertex = degree_list[1][0]
        # Get its neighbor
        neighbor = get_neighbor(vertex)
        k -= 1
        if k < 0: return S_kern, undelete, k
        S_kern.append(neighbor)
        del_vert([neighbor])
        undelete.append(neighbor)
        S_kern_new, undelete_new, k = extreme_reduction_rule(k)
        S_kern += S_kern_new
        undelete += undelete_new
    return S_kern, undelete, k


def basic_rules(k):
    S_kern, undelete = [], []
    while k >= 0:
        S_kern_ex, undelete_ex, k = extreme_reduction_rule(k)
        S_kern += S_kern_ex
        undelete += undelete_ex
        if k < 0: break
        S_kern_one, undelete_one, k = degree_one_rule(k)
        S_kern += S_kern_one
        undelete += undelete_one
        if S_kern_ex == [] and S_kern_one == []: break
    return S_kern, undelete, k


def degree_two_rule(k):
    S_kern, undelete, unmerge = [], [], []
    if max_degree < 2: return S_kern, undelete, unmerge, k
    while degree_list[2] != []:
        degree_two_rule.counter += 1
        vertex = degree_list[2][0]
        [u, w] = get_all_neighbors(vertex)
        if w in g[u][2]:
            if k - 2 < 0: return S_kern, undelete, unmerge, k - 2
            del_vert([vertex, u, w])
            undelete += [vertex, u, w]
            S_kern += [u, w]
            k -= 2
        else:
            if k - 1 < 0: return S_kern, undelete, unmerge, k - 1
            merged_point = merge_vert(vertex, u, w)
            S_kern.append(vertex)
            unmerge.append(merged_point)
            k -= 1
        if k < 0: break
        S_kern_new, undelete_new, k = basic_rules(k)
        S_kern += S_kern_new
        undelete += undelete_new
        if k < 0: break
    return S_kern, undelete, unmerge, k


def domination_rule(k):
    S_kern, undelete = [], []
    for degree in range(3, max_degree+1):
        for vertex in degree_list[degree]:
            if dom_opt:
                if not g[vertex][3]: continue
                else: g[vertex][3] = False
            neighborhood = [vertex]
            lowest_degree = max_degree + 1
            for adj_vert in g[vertex][2]:
                if not g[adj_vert][0]:
                    neighborhood.append(adj_vert)
                    if g[adj_vert][1] < lowest_degree:
                        lowest_degree = g[adj_vert][1]
                        low_degree_neighbor = adj_vert
            for adj_vert in g[low_degree_neighbor][2] + [low_degree_neighbor]:
                if adj_vert != vertex and adj_vert in neighborhood and all(u in ([adj_vert] + g[adj_vert][2]) for u in neighborhood):
                    domination_rule.counter += 1
                    del_vert([adj_vert])
                    undelete.append(adj_vert)
                    S_kern.append(adj_vert)
                    k -= 1
                    S_kern_new, undelete_new, k = basic_rules(k)
                    S_kern += S_kern_new
                    undelete += undelete_new
                    if k < 0: return S_kern, undelete, k
                    break
    return S_kern, undelete, k


def mipParam():
    """
    INPUT: NONE
    Under the assumption that all lists of neighbors are correctly updated, returns all the necessary objects to run CPLEX
    OUTPUT: my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows
    """
    global nb_vertices
    global nb_edges
    #Objective function is sum with all factors set to 1
    my_obj = [1]*nb_vertices
    #all variables bounded by 0 (default) and 1
    my_ub = [1]*nb_vertices
    #All variables are integers
    my_ctype = 'I'*nb_vertices
    #each edge is a greater-than 1 constraint 
    my_rhs = [1]*nb_edges
    my_sense = 'G'*nb_edges
    #name of the vertices and of the columns are left to fill
    my_colnames = []
    my_rownames = []
    #Actual rows are going to be filled during the for loop
    rows = []
    for degree in range(max_degree+1):
        for vertex in degree_list[degree]:
            my_colnames.append(str(vertex))
            for neigh in g[vertex][2]:
                if g[neigh][0] or g[neigh][1] < g[vertex][1]: continue
                new_row = [[str(neigh),str(vertex)],[1,1]]
                if g[neigh][1] == g[vertex][1] and new_row in rows: continue
                my_rownames.append("e %s %s" % (vertex,neigh))
                rows.append(new_row)
    return my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows


def lp_rule(k):
    """
    INPUT: None
    prints the vertex cover corresponding to global g using cplex solver
    OUTPUT: None
    """
    #get parameters of the CPLEX problem
    my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows = mipParam()
    #initialize the CPLEX problem
    prob = cplex.Cplex()
    #To avoid printing the summary of the cplex resolution, to limit memory usage to 1.5GB and get more precise results on big graphs
    prob.set_results_stream(None)
    prob.parameters.workmem = 1536
    # prob.parameters.mip.tolerances.mipgap = 1e-15
    # prob.parameters.mip.tolerances.absmipgap = 1e-15
    #fill the CPLEX problem with all correct parameters
    prob.objective.set_sense(prob.objective.sense.minimize)
    prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype, names=my_colnames)
    prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs, names=my_rownames)
    #Solve the CPLEX problem
    prob.solve()
    #print the solution 
    numcols = prob.variables.get_num()
    x = prob.solution.get_values()
    S_lp, undelete = [], []
    for j in range(numcols):
        if x[j] in [0,1]:
            vertex = my_colnames[j]
            # If vertex is merged point convert it from string to triple:
            if vertex[0] == '(': vertex = eval(vertex)
            del_vert([vertex])
            if x[j] == 1:
                S_lp.append(vertex)
                k -= 1
                if k < 0: return S_lp, undelete, k
            undelete.append(vertex)
    return S_lp, undelete, k


def kernelization(k):
    """
    INPUT: k is int
    kernelization applies all the kernelization rules, depending on the frequencies for branch counting , and returns the depth budget k changed by the kernelization, 
    the vertices to add to the vertex cover, and all the deleted vertices that have to be undeleted afterwards 
    OUTPUT: S_kern is list of vertices, undelete is list of vertices, k is int
    """
    global f_deg2
    global f_dom
    global f_lp
    global limit_kern_start
    global limit_kern_branch
    # Execute reduction rules:
    S_kern, undelete, k = basic_rules(k)
    unmerge = []
    counter = 0
    if vc_branch.counter == 0: limit = limit_kern_start
    else: limit = limit_kern_branch
    while k >= 0 and counter < limit:
        counter += 1
        if vc_branch.counter%f_deg2 == 0:
            S_kern_two, undelete_two, unmerge_two, k = degree_two_rule(k)
            S_kern += S_kern_two
            undelete += undelete_two
            unmerge += unmerge_two
            if k < 0 or is_edgeless(): break
        if vc_branch.counter%f_dom == 0:
            S_kern_dom, undelete_dom, k = domination_rule(k)
            S_kern += S_kern_dom
            undelete += undelete_dom
            if k < 0 or is_edgeless(): break
        if vc_branch.counter%f_lp == 0:
            S_lp, undelete_lp, k = lp_rule(k)
            S_kern += S_lp
            undelete += undelete_lp
            print("# " + str(S_lp))
        # if is_edgeless() or (S_kern_two == [] and S_kern_dom == []): break     # TODO: Try one last time! if haven't tried one of the above before (counter)
        if is_edgeless(): break
    return S_kern, undelete, unmerge, k


def vc_branch(k):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: list of length at most k or None
    """
    global f_bound
    vc_branch.counter += 1
    if k < 0: return None
    # Return empty list if no edges are given:
    if is_edgeless(): return []
    S_kern, undelete, unmerge, k = kernelization(k)
    if k < 0:
        un_del_vert(undelete)
        un_merge_vert(unmerge)
        return None
    # Return one degree neighbors list if no edges left:
    if is_edgeless(): S = S_kern
    # If k is smaller than lower bound, no need to branch:
    elif k == 0 or (vc_branch.counter % f_bound == 0 and k < bound()):
        bound.counter += 1
        S = None
    else:
        # Get vertices of first edge:
        u, neighbors = get_highest_degree_vertex()
        for vertices in u, neighbors:
            # 'Delete' first vertex from graph:    
            del_vert(vertices)
            # Call function recursively:
            S = vc_branch(k - len(vertices))
            # 'Undelete' first vertex from graph:
            un_del_vert(vertices)
            # If vertex cover found return it plus the first vertex:
            if S is not None:
                S = S_kern + vertices + S
                break
    un_del_vert(undelete)
    un_merge_vert(unmerge)
    return S


def heuristic_processing(vertex, counter, dom_freq):
    del_vert([vertex])
    S_one, undelete_one, _ = degree_one_rule(nb_vertices)
    S_two, undelete_two, unmerge_new, _ = degree_two_rule(nb_vertices)
    S_new = [vertex] + S_one + S_two
    undelete_new = [vertex] + undelete_one + undelete_two
    # if counter % dom_freq == 0:
    #     S_dom, undelete_dom = domination_rule(False)
    #     S_new += S_dom
    #     undelete_new += undelete_dom
    #     current_dom_freq = max(1, int((nb_edges / 15000) ** 5))
    #     if S_dom == []: dom_freq = current_dom_freq
    #     else: dom_freq = max(1, min(dom_freq, current_dom_freq) // (1 + len(S_dom)))
    return S_new, undelete_new, unmerge_new, dom_freq


def heuristic():
    S_heur, undelete, unmerge = [], [], []
    dom_freq = 1
    counter = 0
    while not is_edgeless() and max_degree > 0:
        counter += 1
        vertex = degree_list[max_degree][0]
        S_new, undelete_new, unmerge_new, dom_freq = heuristic_processing(vertex, counter, dom_freq)
        S_heur += S_new
        undelete += undelete_new
        unmerge += unmerge_new
    un_del_vert(undelete)
    un_merge_vert(unmerge)
    return len(S_heur)


def vc_branch_constrained(sol_size, upper):
    vc_branch_constrained.counter += 1
    S = None
    if is_edgeless():
        if sol_size > upper: return S, upper
        else: return [], sol_size
    if vc_branch_constrained.counter > 1 and sol_size + bound() > upper: return S, upper
    S_kern, undelete, unmerge, _ = kernelization(upper)
    sol_size += len(S_kern)
    if is_edgeless():
        if sol_size <= upper:
            S = S_kern
            upper = sol_size
    elif sol_size + bound() > upper: bound.counter += 1
    else:
        heur_upper = heuristic()
        upper = min(sol_size + heur_upper, upper)
        u, neighbors = get_highest_degree_vertex()
        for vertices in u, neighbors:
            # 'Delete' first vertex from graph:    
            del_vert(vertices)
            # Call function recursively:
            S_new, upper = vc_branch_constrained(sol_size + len(vertices), upper)
            # 'Undelete' first vertex from graph:
            un_del_vert(vertices)
            # If vertex cover found return it plus the first vertex:
            if S_new is not None: S = S_kern + vertices + S_new
    un_del_vert(undelete)
    un_merge_vert(unmerge)
    return S, upper


def correct_output(S):
    S_new = []
    for vertex in S:
        S_new = append_to_S(S_new, [vertex])
    return S_new


def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    global constrained_branching
    global nb_vertices
    vc_branch.counter = 0
    vc_branch_constrained.counter = 0
    first_lower_bound_difference = 0
    high_degree_rule.counter = 0
    degree_zero_rule.counter = 0
    extreme_reduction_rule.counter = 0
    degree_one_rule.counter = 0
    degree_two_rule.counter = 0
    domination_rule.counter = 0
    bound.counter = 0
    if is_edgeless(): S = []
    else:
        S_kern, _, _, _ = kernelization(nb_vertices - 1)
        if is_edgeless(): S = S_kern
        else:
            x = bound()
            bound.counter += 1
            y = starter_reduction_rule()
            kmin = max(x, y)
            first_lower_bound_difference = x - y
            if constrained_branching:
                upper = nb_vertices - 1
                S, _ = vc_branch_constrained(0, upper)
            else:
                for k in range(kmin, nb_vertices):
                    S = vc_branch(k)
                    if S is not None: break
            S = S_kern + S
    print("#convert...")
    S = correct_output(S)
    print_result(S)
    print("#solution size: %s" % len(S))
    print("#recursive steps: %s" % vc_branch.counter)
    print("#recursive steps (constrained): %s" % vc_branch_constrained.counter)
    print("#first lower bound difference: %s" % first_lower_bound_difference)
    print("#high degree rules: %s" % high_degree_rule.counter)
    print("#degree zero rules: %s" % degree_zero_rule.counter)
    print("#extreme reduction rules: %s" % extreme_reduction_rule.counter)
    print("#degree one rules: %s" % degree_one_rule.counter)
    print("#degree two rules: %s" % degree_two_rule.counter)
    print("#domination rules: %s" % domination_rule.counter)
    print("#lower bounds: %s" % bound.counter)


get_data()
vc()
