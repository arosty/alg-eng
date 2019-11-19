import sys
import numpy as np

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
    for vertex in edge:
        if not vertex in g.keys():
            add_vertex(vertex)
        g[vertex][1] += 1
    g[edge[0]][2].append(edge[1])
    g[edge[1]][2].append(edge[0])

g = {}
max_degree = 0
degree_list = []
nb_vertices = 0

def get_data():
    """
    INPUT: None
    get_data reads standard input and creates the given graph
    OUTPUT: None
    """
    global max_degree
    global degree_list
    global nb_vertices
    # Get standard input:
    input_data = sys.stdin
    for counter, line in enumerate(input_data):
        if counter == 0:
            # Get number of vertices in the graph:
            nb_vertices = np.uint32(line.split()[0][1:])
        if counter > 0:
            # Get current edge and add it to the graph:
            current_edge = line.split()
            add_edge(current_edge)
    # Initializing degree_list:
    for i in range(nb_vertices):
        degree_list.append([])
    for vertex in g:
        degree = g[vertex][1]
        # Append vertex to the list located at its degree in degree_list:
        (degree_list[degree]).append(vertex)
        # If maximal degree vertex for now remember that it's the biggest one:
        if degree > max_degree:
            max_degree = degree
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
    for vertex in vertices:
        # 'Delete' vertex:
        ###Deleting in g
        g[vertex][0] = True
        nb_vertices -= 1
        ###Deleting in degree_list
        degree_vertex = g[vertex][1]
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
    for vertex in vertices:
        # 'Undelete' vertex:
        ###Undeleting in g
        g[vertex][0] = False
        nb_vertices += 1
        ###Undeleting in degree_list
        degree_vertex = g[vertex][1]
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
    return high_deg_vertex, neighbors


def get_neighbor(vertex):
    """
    INPUT: vertex is str
    get_neighbor returns the first neighbor
    OUTPUT: str
    """
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            return neighbor


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
    bound() returns a lower bound using clique cover, starting by smallest degree
    OUTPUT: int
    """
    global clique_list
    clique_list = []
    for list_degree_i in degree_list:
        for vertex in list_degree_i:
            inspect_vertex(vertex)
    return nb_vertices - len(clique_list)


def vc_branch(k):
    """
    INPUT: k is int
    vc_branch returns a vertex cover of size k if it exists in this graph and None otherwise
    OUTPUT: list of length at most k or None
    """
    vc_branch.counter += 1
    if k < 0:
        return None
    # Return empty list if no edges are given:
    if is_edgeless():
        return []
    # Get neighbors of vertices with degree one (if two are adjacent to each other, only one of them):
    degree_one_neighbors = get_degree_one_neighbors()
    # Reduce k according to new vertices:
    k -= len(degree_one_neighbors)
    if k < 0:
        return None
    # 'Delete' neighbors of degree one vertices:
    del_vert(degree_one_neighbors)
    # Return one degree neighbors list if no edges left:
    if is_edgeless():
        # 'Undelete' neighbors of degree one vertices:
        un_del_vert(degree_one_neighbors)
        return degree_one_neighbors
    elif k == 0:
        un_del_vert(degree_one_neighbors)
        return None
    #if k is smaller than lower bound, no need to branch
    if k < bound():
        un_del_vert(degree_one_neighbors)
        return None
    # Get vertices of first edge:
    u, neighbors = get_highest_degree_vertex()
    # 'Delete' first vertex from graph:
    del_vert([u])
    # Call function recursively:
    Su = vc_branch(k-1)
    # 'Undelete' first vertex from graph:
    un_del_vert([u])
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        un_del_vert(degree_one_neighbors)
        Su += degree_one_neighbors
        Su.append(u)
        return Su
    # 'Delete' second vertex from graph:
    del_vert(neighbors)
    # Call function recursively:
    Sv = vc_branch(k-len(neighbors))
    # 'Undelete' second vertex from graph:
    un_del_vert(neighbors + degree_one_neighbors)
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        Sv += neighbors + degree_one_neighbors
        return Sv
    return None


def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    vc_branch.counter = 0
    # Get neighbors of vertices with degree one (if two are adjacent to each other, only one of them):
    degree_one_neighbors = get_degree_one_neighbors()
    # Asign kmin to the number of neighbors of vertices with degree one:
    kmin = len(degree_one_neighbors)
    del_vert(degree_one_neighbors)
    if not is_edgeless():
        kmin += bound()
    un_del_vert(degree_one_neighbors)
    # Try the recursive function for every k until it gives a result:
    for k in range(kmin,len(g)):
        S = vc_branch(k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


get_data()
