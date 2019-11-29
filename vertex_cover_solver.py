import sys

g = {}
max_degree = 0
degree_list = []
nb_vertices = 0
nb_edges = 0

def add_vertex(vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    g[vertex] = [False, 0, []]


def add_edge(edge):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), edge is list of length 2
    add_vertex adds a new edge to the graph and returns this graph
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    global max_degree
    global nb_edges
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
    # Initializing degree_list:
    degree_list = [[] for i in range(max_degree + 1)]
    for vertex in g:
        degree = g[vertex][1]
        # Append vertex to the list located at its degree in degree_list:
        degree_list[degree].append(vertex)
    nb_vertices = len(g)


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
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in vertices:
        #if vertex not yet deleted, delete it
        if not g[vertex][0]:
            # 'Delete' vertex:
            ###Deleting in g
            g[vertex][0] = True
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
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in reversed(vertices):
        #vertex deleted, undelete it
        if g[vertex][0]:
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
    INPUT: vertex
    get_neighbor returns the first neighbor
    OUTPUT: vertex
    """
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            return neighbor


def get_all_neighbors(vertex):
    """
    INPUT: vertex
    get_neighbor returns the first neighbor
    OUTPUT: list of vertices
    """
    neighbors = []
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            neighbors.append(neighbor)
    return(neighbors)

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
    # print('#S before append: ', S)
    # print('# vertices to append: ', vertices)
    if S == None: return None
    for vertex in vertices:
        if type(vertex) is str:
            if vertex not in S:
                S.append(vertex)
        else:
            v, u, w = vertex
            S = del_from_S(S,[v])
            for x in [u, w]:
                S = append_to_S(S, [x])
    # print('#S after append: ', S)
    return S


def del_from_S(S, vertices):
    # print('#S before del: ', S)
    # print('# vertices to remove: ', vertices)
    for vertex in vertices:
        if type(vertex) is str:
            # print('# removed vertex: ', vertex)
            # print('#S: ', S)
            if vertex in S: #Maybe better to have a bool parameter that says if it's recursive S or S_kern
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
        S_kern = append_to_S(S_kern, [high_degree_vertex])
        k -= 1
    undelete = S_kern[:]
    return S_kern, undelete, k


def degree_zero_rule():
    """
    INPUT: None
    degree_zero_rule deletes all degree zero vertices and returns them
    OUTPUT: list
    """
    if degree_list[0] != []:
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
    if nb_vertices > k ** 2 + k or nb_edges > k ** 2: k = -1
    return S_kern, undelete, k


def starter_reduction_rule():
    """
    INPUT: None
    starter_reduction_rule gives a lower bound for k according to the reduction rule
    OUTPUT: int
    """
    return int(.5 * max(-1 + (1 + 4 * nb_vertices) ** .5, 2 * nb_edges ** .5) + 0.999)



def get_degree_one_neighbors():
    """
    INPUT: None
    get_degree_one_neighbors return the neighbors of all vertices of degree one
    (if two vertices of degree one are adjacent to each other, it choses one of them)
    OUTPUT: list
    """
    # Initialize list of neighbors of vertices with one degree:
    neighbors = []
    # Iterate through all vertices of degree one and append its neighbor to the list (if not added already):
    for vertex in degree_list[1]:
        if vertex not in neighbors:
            neighbor = get_neighbor(vertex)
            if neighbor not in neighbors:
                neighbors.append(neighbor)
    return neighbors



def degree_one_rule (k):
    """
    INPUT: k is int 
    degree_one_rule deletes all degree one vertices and returns them, deletes all 
    of their neighbors and return them to add them to S. also returns the depth budget k changed by deletion
    OUTPUT: S_kern is list of vertices, undeleteis list of vertices, k is int
    """
    S_kern, undelete = [],[]
    if k < 0: return S_kern, undelete, k
    if degree_list[1] != []:
        # Get neighbors of vertices with degree one (if two are adjacent to each other, only one of them):
        degree_one_neighbors = get_degree_one_neighbors()
        # Reduce k according to new vertices:
        k -= len(degree_one_neighbors)
        if k < 0: return S_kern, undelete, k
        S_kern = append_to_S(S_kern, degree_one_neighbors)
        # 'Delete' neighbors of degree one vertices:
        del_vert(degree_one_neighbors)
        undelete.extend(degree_one_neighbors)
        S_kern_new, undelete_new, k = extreme_reduction_rule(k)
        S_kern += S_kern_new
        undelete += undelete_new
    return S_kern, undelete, k



def merge_vert (vertex, u, w):
    """
    INPUT: vertex of degree 2, and its two neighbors u and w
    to use only if vertex has degree 2 and there is no edge between u and w
    merges vertex and its 2 neighbors, but doesn't change k 
    OUTPUT: the name of the resulting merged_point
    """
    global nb_vertices
    global degree_list
    merged_point = (vertex, u, w)
    #add merged vertex and delete vertex and its neighbors
    del_vert([vertex, u, w])
    undelete = [vertex, u, w]
    
    add_vertex(merged_point)
    nb_vertices += 1
    #add edges towards every neighbor only once 
    for z in [u, w]:
        for n in g[z][2]:
            if not g[n][0]:
                if n not in g[merged_point][2]:
                    add_edge([merged_point,n])
                    n_degree = g[n][1]
                    degree_list[n_degree-1].remove(n)
                    degree_list[n_degree].append(n)
    #append the new merged_point in degree_list
    deg_merged_point = g[merged_point][1]
    len_degree_list = len(degree_list)
    # print('# problem point ', merged_point, g[merged_point])
    # print('# deg_merged_point ',deg_merged_point)
    # print('# len(degree_list) ', len(degree_list))
    # print('# deg_merged_point > len(degree_list)', deg_merged_point > len(degree_list))
    if deg_merged_point + 1 > len_degree_list:
        for i in range(deg_merged_point + 1 - len_degree_list):
            degree_list.append([])
    # print('# len(degree_list) ', len(degree_list))
    degree_list[deg_merged_point].append(merged_point)
    return(merged_point, undelete)
    
    
        
def un_merge_vert (merged_points):
    """
    INPUT: list of result vertices of a merge that must be 'v u w'
    cancels the merge that resulted in the vertices of merged_points, but doesn't change k 
    OUTPUT: None
    """        
    if merged_points != []:
        print ('#merged_points: ', merged_points, type(merged_points))
        for merged_point in reversed(merged_points):
            (vertex, u, w) = merged_point 
            del_vert([merged_point])
            un_del_vert([vertex, u, w])
        


def degree_two_rule (k):
    global max_degree
    S_kern = []
    undelete = []
    unmerge = []
    if k < 0: return S_kern, undelete, k, unmerge
    if max_degree < 2:
        return S_kern, undelete, k, unmerge
    while degree_list[2] != []:
        print('#S_kern ', S_kern) 
        print('#undelete ', undelete) 
        print('#k ', k)
        print('#unmerge ', unmerge) 
        vertex = degree_list[2][0]
        #u and w are the only 2 undeleted neighbors of vertex 
        [u, w] = get_all_neighbors(vertex)
        if w in g[u][2]:
            #if not k-2<0 we can preprocess
            if k-2 < 0: return S_kern, undelete, k-2, unmerge
            del_vert([vertex, u, w])
            S_kern = append_to_S(S_kern, [u,w])
            undelete.extend([vertex, u, w])
            k -= 2
        else:
            if k-1 < 0: return S_kern, undelete, k-1, unmerge
            merged_point, undelete_new = merge_vert(vertex, u, w)
            S_kern = append_to_S(S_kern, [vertex])
            undelete += undelete_new
            unmerge.append(merged_point)
            k -= 1
    S_kern_new, undelete_new, k = extreme_reduction_rule(k)
    S_kern += S_kern_new
    undelete += undelete_new
    return S_kern, undelete, k, unmerge






def kernalization(k):
    """
    INPUT: k is int 
    kernalization applies all the kernelization rules, and returns the depth budget k changed by the kernelization, 
    the vertices to add to the vertex cover, and all the deleted vertices that have to be undeleted afterwards 
    OUTPUT: S_kern is list of vertices, undeleteis list of vertices, k is int
    """
    S_kern, undelete, unmerge = [],[],[]
    # # Execute extreme reduction rules:
    # S_kern, undelete, k = extreme_reduction_rule(k)
    # unmerge = []
    # if k < 0: return S_kern, undelete, k
    # # Execute degree one rule:
    # S_kern_one, undelete_one, k = degree_one_rule(k)
    # S_kern += S_kern_one
    # undelete += undelete_one
    # Execute degree two rule:
    S_kern_two, undelete_two, k, unmerge_two = degree_two_rule(k)
    S_kern += S_kern_two
    undelete += undelete_two
    unmerge = list(set().union(unmerge, unmerge_two))
    return S_kern, undelete, k, unmerge


def vc_branch(k, S):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: list of length at most k or None
    """
    vc_branch.counter += 1
    print('#-------------------------------------rec step n°',vc_branch.counter,'-------------------------------------')
    if k < 0: return None
    # Return empty list if no edges are given:
    if is_edgeless(): return S
    S_kern, undelete, k, unmerge_kern = kernalization(k)
    if k < 0:
        un_merge_vert(unmerge_kern)
        un_del_vert(undelete)
        return None
    S = append_to_S(S, S_kern)
    # Return one degree neighbors list if no edges left:
    if is_edgeless(): return S
    # If k is smaller than lower bound, no need to branch:
    elif k == 0 or k < bound(): return None
    else:
        # Get vertices of first edge:
        u, neighbors = get_highest_degree_vertex()
        for vertices in u, neighbors:
            # 'Delete' first vertex from graph:    
            del_vert(vertices)
            # Call function recursively:
            S = vc_branch(k - len(vertices), S)
            # 'Undelete' first vertex from graph:
            un_del_vert(vertices)
            # If vertex cover found return it plus the first vertex:
            if S is not None:
                S = append_to_S(S, vertices + S_kern)
                break
    un_merge_vert(unmerge_kern)
    un_del_vert(undelete)
    return S

def print_all():
    print('g ', g)
    print('degree_list ', degree_list)
    print('max_degree ', max_degree)
    print('nb_vertices ', nb_vertices)
    print('nb_edges ', nb_edges, '\n')
    return

def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    # print_all()
    vc_branch.counter = 0
    if is_edgeless(): S = []
    else:
        # S_kern, _, _, _ = kernalization(nb_vertices - 1)
        # if is_edgeless(): S = S_kern
        # else:
        kmin = max(starter_reduction_rule(), bound())
        for k in range(kmin, nb_vertices):
            S = vc_branch(k,[])
            # if S is not None:
            #     S = append_to_S(S, S_kern)
            #     break
    print_result(S)
    print("#solution size: %s" % len(S))
    print("#recursive steps: %s" % vc_branch.counter)


get_data()
vc()
