# Set False if cplex not installed on current machine:
use_cplex = True

# Import cplex only if set to True:
if use_cplex:
    import cplex
    from cplex.exceptions import CplexError

import sys

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
f_deg2_heur = 1
f_dom = 1
f_deg3 = 1
f_lp = 1
f_clique_lb = 3
f_lp_lb = 2
#if True, second method of branching is used
constrained_branching = True
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
        if not vertex in g.keys(): add_vertex(vertex)
        g[vertex][1] += 1
        # If current degree is greater than maximum degree, update:
        if g[vertex][1] > max_degree: max_degree += 1
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
    degree_list = [[] for i in range(max(4,nb_vertices))]
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
    for vertex in vertices: print(vertex)

        
def del_vert(vertices, really=False):
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
            if really: g[adj_vert][2].remove(vertex)
        if really: del g[vertex]
    #If max_degree is obsolete, go through all degrees decreasing from max_degree to find the new value
    while max_degree > 0 and degree_list[max_degree] == []: max_degree -= 1

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
        if g[vertex][1] > max_degree: max_degree = g[vertex][1]
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
                if g[adj_vert][1] > max_degree: max_degree = g[adj_vert][1]


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
        if not g[neighbor][0]: neighbors.append(neighbor)
    return [high_deg_vertex], neighbors


def get_neighbor(vertex):
    """
    INPUT: vertex is str
    get_neighbor returns the first neighbor
    OUTPUT: str
    """
    for neighbor in g[vertex][2]:
        # Return neighbor if not deleted:
        if not g[neighbor][0]: return neighbor


def test_clique(vertex,clique):
    """
    INPUT: vertex, clique: list[vertices]
    For a vertex and a clique, returns True if the vertex and the existing clique form a clique
    OUTPUT, Bool
    """
    # For every vertex v in the clique:
    for v in clique:
        # If vertex is not a neighbor of v, vertex is not in the vertex cover:
        if vertex not in g[v][2]: return False
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
        if test_clique(vertex, clique_list[i]) and clique_size > best_clique_size:
            # Remember this clique's index and size:
            best_clique_index = i
            best_clique_size = clique_size
    # If we didn't find any clique to add vertex in, we create one containing vertex:
    if best_clique_index == -1: clique_list.append([vertex])
    # Else we add vertex to the best clique possible:
    else: clique_list[best_clique_index].append(vertex)


def clique_bound():
    """
    INPUT: None
    bound returns a lower bound using clique cover, starting by smallest degree
    OUTPUT: int
    """
    # Declare clique list:
    global clique_list
    clique_list = []
    for list_degree_i in degree_list:
        for vertex in list_degree_i:  inspect_vertex(vertex)
    return nb_vertices - len(clique_list)


def lpParam():
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
    my_ctype = 'C'*nb_vertices
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
                if g[neigh][1] == g[vertex][1] and [[str(neigh),str(vertex)],[1,1]] in rows: continue
                my_rownames.append("e %s %s" % (vertex,neigh))
                rows.append([[str(vertex),str(neigh)],[1,1]])
    return my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows


def lp():
    #get parameters of the CPLEX problem
    my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows = lpParam()
    #initialize the CPLEX problem
    prob = cplex.Cplex()
    #To avoid printing the summary of the cplex resolution, to limit memory usage to 1.5GB and get more precise results on big graphs
    prob.set_results_stream(None)
    prob.parameters.workmem = 1536
    #fill the CPLEX problem with all correct parameters
    prob.objective.set_sense(prob.objective.sense.minimize)
    prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype, names=my_colnames)
    prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs, names=my_rownames)
    #Solve the CPLEX problem
    prob.solve()
    #print the solution 
    numcols = prob.variables.get_num()
    x = prob.solution.get_values()
    return x, numcols, my_colnames


def lp_bound():
    x, _, _ = lp()
    return sum(x)


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
    if S_kern != []: high_degree_rule.counter += 1
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
    OUTPUT: list : additional vertices for the vertex cover, list : vertices that need to be undeleted later again, int : new k
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
        del_vert([merged_point], True)
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
        if k < 0: break
        S_kern.append(neighbor)
        del_vert([neighbor])
        undelete.append(neighbor)
        S_kern_new, undelete_new, k = extreme_reduction_rule(k)
        S_kern += S_kern_new
        undelete += undelete_new
    return S_kern, undelete, k


def basic_rules(k):
    """
    INPUT: k is int
    basic_rules calls the extreme reduction rule (degree zero and high degree) and the degree one rule until
    none of them can be applied anymore and returns the so gotten vertices for S, the ones to undelete again
    and the depth budget k changed by deletion
    OUTPUT: S_kern is list of vertices, undeleteis list of vertices, k is int
    """
    S_kern, undelete = [], []
    while k >= 0:
        S_kern_ex, undelete_ex, k = extreme_reduction_rule(k)
        S_kern += S_kern_ex
        undelete += undelete_ex
        if k < 0: break
        S_kern_one, undelete_one, k = degree_one_rule(k)
        S_kern += S_kern_one
        undelete += undelete_one
        # Finish if no rule could be applied:
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
    for degree in range(3, max_degree):
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


def lp_rule(k):
    """
    INPUT: None
    prints the vertex cover corresponding to global g using cplex solver
    OUTPUT: None
    """
    x, numcols, my_colnames = lp()
    if sum(x) > k: return [], [], -1
    S_lp, undelete = [], []
    for j in range(numcols):
        if x[j] in [0,1]:
            vertex = my_colnames[j]
            # If vertex is merged point convert it from string to triple:
            if vertex[0] == '(': vertex = eval(vertex)
            del_vert([vertex])
            undelete.append(vertex)
            if x[j] == 1:
                S_lp.append(vertex)
                k -= 1
                if k < 0: return S_lp, undelete, k
    return S_lp, undelete, k


def add_neighborhood(vertex, neighborhood):
    """
    INPUT: vertex is int, neighborhood is list of int
    try to add all vertices from neighborhood as neighbors of vertex. Those who aren't already are returned in new_neigh
    OUTPUT: new_neigh is list of int
    """
    global max_degree
    global nb_edges
    new_neigh = []
    for neigh in neighborhood:
        # if neigh is not already a neighbor and is not the vertex itself, it can be added as neighbor
        if neigh not in g[vertex][2] and vertex not in g[neigh][2] and neigh != vertex:
            new_neigh.append(neigh)
            #Increment edge counter
            nb_edges += 1
            #add edge for neigh
            g[neigh][1] += 1
            g[neigh][2].append(vertex)
            degree_list[g[neigh][1]-1].remove(neigh)
            degree_list[g[neigh][1]].append(neigh)
            # If new degree of neigh is greater than maximum degree, update:
            if g[neigh][1] > max_degree: max_degree = g[neigh][1]
    #add edges for vertex
    old_degree = g[vertex][1]
    g[vertex][1] += len(new_neigh)
    g[vertex][2] += new_neigh
    new_degree = g[vertex][1]
    degree_list[old_degree].remove(vertex)
    degree_list[new_degree].append(vertex)
    # If new degree of vertex is greater than maximum degree, update:
    if new_degree > max_degree: max_degree = new_degree
    return new_neigh



def degree_three_rule(k):
    """
    INPUT: vertex is int
    applies degree 3 independent set rule and returns the undo_list
    OUTPUT: undo_list 
    """
    S_kern, undo_list = [], []
    for vertex in degree_list[3]:
        [a,b,c] = get_all_neighbors(vertex)
        independent_test = (b not in g[a][2]) & (c not in g[a][2]) & (c not in g[b][2])
        if independent_test:
            degree_three_rule.counter += 1
            # Delete vertex:
            del_vert([vertex])
            # adding edges to a, b and c:
            all_neigh_a = get_all_neighbors(a)
            all_neigh_b = get_all_neighbors(b)
            all_neigh_c = get_all_neighbors(c)
            new_neigh_a = add_neighborhood(a, all_neigh_b)
            new_neigh_b = add_neighborhood(b, all_neigh_c)
            new_neigh_c = add_neighborhood(c, all_neigh_a)
            add_edge([a,b])
            add_edge([b,c])
            degree_list[g[a][1]-1].remove(a)
            degree_list[g[a][1]].append(a)
            degree_list[g[b][1]-2].remove(b)
            degree_list[g[b][1]].append(b)
            degree_list[g[c][1]-1].remove(c)
            degree_list[g[c][1]].append(c)
            undo_list.append( [3, [ (vertex,a,b,c), new_neigh_a, new_neigh_b, new_neigh_c ] ] )
            S_kern_new, undelete, k = basic_rules(k)
            S_kern += S_kern_new
            undo_list.append([1, undelete])
    return S_kern, undo_list, k



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
    kernelization.counter += 1
    undo_list = []
    # Execute reduction rules:
    S_kern, undelete, k = basic_rules(k)
    if undelete != []: undo_list.append([1, undelete])
    counter = 0
    if vc_branch.counter == 0: limit = limit_kern_start
    else: limit = limit_kern_branch
    while k >= 0 and not is_edgeless() and counter < limit:
        counter += 1
        successful = False
        if kernelization.counter%f_deg2 == 0:
            S_kern_two, undelete_two, unmerge_two, k = degree_two_rule(k)
            S_kern += S_kern_two
            if S_kern_two != []: successful = True
            if unmerge_two != []: undo_list.append([2, unmerge_two])
            if undelete_two != []: undo_list.append([1, undelete_two])
            if k < 0 or is_edgeless(): break
        if kernelization.counter%f_dom == 0:
            S_kern_dom, undelete_dom, k = domination_rule(k)
            S_kern += S_kern_dom
            if S_kern_dom != []: successful = True
            if undelete_dom != []: undo_list.append([1, undelete_dom])
            if k < 0 or is_edgeless(): break
        if use_cplex and kernelization.counter%f_lp == 0:
            S_lp, undelete_lp, k = lp_rule(k)
            S_kern += S_lp
            if S_lp != []: successful = True
            if undelete_lp != []: undo_list.append([1, undelete_lp])
        if kernelization.counter%f_deg3 == 0:     #TODO: we need to think about the order, shouldn't deg3 be before dom?
            S_kern_three, undo_list_deg3, k = degree_three_rule(k)
            S_kern += S_kern_three
            if undo_list_deg3 != []: 
                successful = True
                undo_list += undo_list_deg3
            if k < 0 or is_edgeless(): break
        if not successful: break     # TODO: Try one last time! if haven't tried one of the above before (counter)
    return S_kern, undo_list, k


def cancel_neighborhood(vertex, new_neigh_v):
    global max_degree
    global nb_edges
    #Decrement edge counter
    nb_edges -= len(new_neigh_v)
    for neigh in new_neigh_v:
            #remove edge for neigh
            g[neigh][1] -= 1
            g[neigh][2].remove(vertex)
            n_degree = g[neigh][1]
            degree_list[n_degree+1].remove(neigh)
            degree_list[n_degree].append(neigh)
    #remove edges for vertex
    g[vertex][2] = [i for i in g[vertex][2] if i not in new_neigh_v]
    old_degree = g[vertex][1]
    g[vertex][1] -= len(new_neigh_v)
    new_degree = g[vertex][1]
    degree_list[old_degree].remove(vertex)
    degree_list[new_degree].append(vertex)
    #If max_degree is obsolete, go through all degrees decreasing from max_degree to find the new value
    while (max_degree > 0) & (degree_list[max_degree] == []): max_degree -= 1



def correct_deg3 (S, v,a,b,c):
    in_S_list = []
    for n in [a,b,c]:
        if n in S: in_S_list.append(n)
    if in_S_list == [b]:
        S.remove(b)
        S.append(v)
    elif len(in_S_list) == 2:
        if in_S_list == [a,b]:
            S.remove(a)
            S.append(v)
        elif in_S_list == [b,c]:
            S.remove(b)
            S.append(v)
        elif in_S_list == [a,c]:
            S.remove(c)
            S.append(v)
    return S


def undo(S, undo_list, undelete=True):
    """
    INPUT: undo_list is list of lists of int and list of int   >>>>> [[int, [vertices]]]
    calls the right function to undo a change on G, depending on the int before every list of changed items
    1: undelete, 2: unmerge, 3: undo deg3 changes
    OUTPUT: None
    """
    for [indicator, vertices] in reversed(undo_list):
        if indicator == 1:
            if undelete: un_del_vert(vertices)
        elif indicator == 2:
            for vertex in reversed(vertices):
                if S is not None and vertex in S:
                    v, u, w = vertex
                    for vert in [vertex, v]: S.remove(vert)
                    S += [u, w]
            if undelete: un_merge_vert(vertices)
        elif indicator == 3:
            [(v,a,b,c), new_neigh_a, new_neigh_b, new_neigh_c] = vertices
            if undelete:
                # Change g back to how it was
                cancel_neighborhood(a, new_neigh_a)
                cancel_neighborhood(b, new_neigh_b + [a,c])
                cancel_neighborhood(c, new_neigh_c)
                un_del_vert([v])
            # Correct S according to deg3 rule
            if S is not None: S = correct_deg3(S,v,a,b,c)
    return S


def vc_branch(k):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: list of length at most k or None
    """
    global f_clique_lb
    global f_lp_lb
    vc_branch.counter += 1
    S = None
    if k < 0: return S
    # Return empty list if no edges are given:
    if is_edgeless(): return []
    S_kern, undo_list, k = kernelization(k)
    if k < 0: return undo(S, undo_list)
    # Return one degree neighbors list if no edges left:
    elif is_edgeless(): S = S_kern
    # If k is smaller than lower bound, no need to branch:
    elif k == 0 or (use_cplex and vc_branch.counter % f_lp_lb == 0 and k < lp_bound()): lp_bound.counter += 1
    elif vc_branch.counter % f_clique_lb == 0 and k < clique_bound(): clique_bound.counter += 1
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
    return undo(S, undo_list)


def heuristic_processing(vertex, counter, dom_freq):
    del_vert([vertex])
    S_one, undelete_one, _ = degree_one_rule(nb_vertices)
    S_new = [vertex] + S_one 
    undelete_new = [vertex] + undelete_one
    if kernelization.counter%f_deg2 == 0:
        S_two, undelete_two, unmerge_new, _ = degree_two_rule(nb_vertices)
        S_new += S_two
        undelete_new += undelete_two
    else:
        unmerge_new = []
    # if counter % dom_freq == 0:
    #     S_dom, undelete_dom = domination_rule(False)
    #     S_new += S_dom
    #     undelete_new += undelete_dom
    #     current_dom_freq = max(1, int((nb_edges / 15000) ** 5))
    #     if S_dom == []: dom_freq = current_dom_freq
    #     else: dom_freq = max(1, min(dom_freq, current_dom_freq) // (1 + len(S_dom)))
    return S_new, undelete_new, unmerge_new, dom_freq


def heuristic():
    S_heur, undo_list = [], []
    dom_freq = 1
    counter = 0
    while not is_edgeless() and max_degree > 0:
        counter += 1
        vertex = degree_list[max_degree][0]
        S_new, undelete_new, unmerge_new, dom_freq = heuristic_processing(vertex, counter, dom_freq)
        S_heur += S_new
        if unmerge_new != []: undo_list.append([2, unmerge_new]) 
        if undelete_new != []: undo_list.append([1, undelete_new])
    S_heur = undo(S_heur, undo_list)
    return S_heur, len(S_heur)


def vc_branch_constrained(sol_size, upper):
    vc_branch_constrained.counter += 1
    S = None
    if is_edgeless():
        if sol_size >= upper: return S, upper
        else: return [], sol_size
    if use_cplex and vc_branch_constrained.counter > 1 and sol_size + lp_bound() >= upper: return S, upper
    if vc_branch_constrained.counter > 1 and sol_size + clique_bound() >= upper: return S, upper
    S_kern, undo_list, _ = kernelization(upper)
    sol_size += len(S_kern)
    if is_edgeless():
        if sol_size < upper:
            S = S_kern
            upper = sol_size
    elif use_cplex and sol_size + lp_bound() >= upper: lp_bound.counter += 1
    elif sol_size + clique_bound() >= upper: clique_bound.counter += 1
    else:
        S_heur, heur_upper = heuristic()
        if sol_size + heur_upper < upper:
            S = S_kern + S_heur
            upper = sol_size + heur_upper
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
    S = undo(S, undo_list)
    return S, upper


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
    kernelization.counter = 0
    first_lower_bound_difference = 0
    high_degree_rule.counter = 0
    degree_zero_rule.counter = 0
    extreme_reduction_rule.counter = 0
    degree_one_rule.counter = 0
    degree_two_rule.counter = 0
    domination_rule.counter = 0
    degree_three_rule.counter = 0
    clique_bound.counter = 0
    lp_bound.counter = 0
    if is_edgeless(): S = []
    else:
        S_kern, undo_list, _ = kernelization(nb_vertices - 1)
        if is_edgeless(): S = undo(S_kern, undo_list, False)
        else:
            x = clique_bound()
            clique_bound.counter += 1
            y = starter_reduction_rule()
            kmin = max(x, y)
            first_lower_bound_difference = x - y
            if constrained_branching: S, _ = vc_branch_constrained(0, nb_vertices)
            else:
                for k in range(kmin, nb_vertices):
                    S = vc_branch(k)
                    if S is not None: break
            S = undo(S_kern + S, undo_list, False)
    print('#------------------#')
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
    print("#degree three rules: %s" % degree_three_rule.counter)
    print("#lower bounds: %s" % clique_bound.counter)


get_data()
vc()
