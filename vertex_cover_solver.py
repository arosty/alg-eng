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

def get_data():
    """
    INPUT: None
    get_data reads standard input and creates the given graph
    OUTPUT: None
    """
    global max_degree
    global degree_list
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
    for vertex in vertices:
        # 'Delete' vertex:
        ###Deleting in g
        g[vertex][0] = True
        ###Deleting in degree_list
        degree_vertex = g[vertex][1]
        degree_list[degree_vertex].remove(vertex)
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            if not g[adj_vert][0]:
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert].remove(adj_vert)
                degree_list[degree_adj_vert-1].append(adj_vert)
                ###Updating g
                g[adj_vert][1] -= 1
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
    for vertex in vertices:
        # 'Undelete' vertex:
        ###Undeleting in g
        g[vertex][0] = False
        ###Undeleting in degree_list
        degree_vertex = g[vertex][1]
        degree_list[degree_vertex].append(vertex)
        # If the vertex has a higher degree than max_degree, we update max_degree
        if g[vertex][1] > max_degree:
            max_degree = g[vertex][1]
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            if not g[adj_vert][0]:
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert].remove(adj_vert)
                degree_list[degree_adj_vert+1].append(adj_vert)
                ###Updating g
                g[adj_vert][1] += 1
                #If the neighbour has after undeletion a higher degree than max degree we update it
                if g[adj_vert][1] > max_degree:
                    max_degree = g[adj_vert][1]


def is_edgeless():
    """
    INPUT: None
    is_edgeless returns True if the graph doesn't have any undeleted edges and False otherwise
    OUTPUT: True or False
    """
    return max_degree == 0


def get_edge():
    """
    INPUT: None
    get_edge returns the first edge
    OUTPUT: list of length 2
    """
    # Get one of the highest degree vertices:
    vertex = degree_list[max_degree][0]
    # If vertex not deleted then take first adjacent vertex and return it:
    for adj_vert in g[vertex][2]:
        if not g[adj_vert][0]:
            return [vertex, adj_vert]


def  highest_degree_vertex():
    """
    INPUT: None
    highest_degree_vertex returns the key to the highest degree vertex, and the list of all it's neigbours which aren't deleted
    OUTPUT: highest degree vertex as index of the dictionary, list of neighbours' key 
    """
    best_vertex = None
    neighbours = []
    degree_max = -1
    #For every vertex in the dic, we remember its key and neighbours if it has the best degree yet
    for k in g:
        if not g[k][0]:
            if g[k][1]>degree_max:
                degree_max = g[k][1]
                best_vertex = k
    #We have to get rid of the neighbours who have been deleted
    neigh_vert = None
    neighbours = g[best_vertex][2]
    for i in range (len(neighbours)):
        #pop the first neigbour vertex in the list
        neigh_vert = neighbours.pop(0)
        #if it hasn't been deleted we reinsert it at the end
        if not g[neigh_vert][0]:
            neighbours.append(neigh_vert)
    return best_vertex,neighbours


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
    # Get vertices of first edge:
    u,neighbours = highest_degree_vertex()
    # 'Delete' first vertex from graph:
    del_vert([u])
    # Call function recursively:
    Su = vc_branch(k-1)
    # 'Undelete' first vertex from graph:
    un_del_vert([u])
    # If vertex cover found return it plus the first vertex:
    if Su is not None:
        Su.append(u)
        return Su
    # 'Delete' second vertex from graph:
    del_vert(neighbours)
    # Call function recursively:
    Sv = vc_branch(k-len(neighbours))
    # 'Undelete' second vertex from graph:
    un_del_vert(neighbours)
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
        for v in neighbours:
            Sv.append(v)
        return Sv
    return None


def vc():
    """
    INPUT: None
    function to call to find and print the vertex cover in a benchmark understandable way
    OUTPUT:None, prints directly in the console
    """
    vc_branch.counter = 0
    # Try the recursive function for every k until it gives a result or k>kmax
    for k in range(len(g)):
        S = vc_branch(k)
        if S is not None:
            print_result(S)
            print("#recursive steps: %s" % vc_branch.counter)
            return None


get_data()
vc()
