
def add_vertex(g, vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    g[vertex] = [False, 0, []]
    return g


def add_edge(g, edge):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), edge is list of length 2
    add_vertex adds a new edge to the graph and returns this graph
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    for vertex in edge:
        if not vertex in g.keys():
            g = add_vertex(g, vertex)
        g[vertex][1] += 1
    g[edge[0]][2].append(edge[1])
    g[edge[1]][2].append(edge[0])
    return g


def get_data():
    """
    INPUT: None
    get_data reads standard input and returns the given graph
    OUTPUT: np.array of shape (nb_edges,2)
    """
    # Get standard input:
    input_data = sys.stdin
    g = {}
    max_degree = 0
    for counter, line in enumerate(input_data):
        if counter == 0:
            #get number of vertices in the graph
            nb_vertices = np.uint32(line.split()[0])
        if counter > 0:
            # Get current edge and add it to the graph:
            current_edge = line.split()
            g = add_edge(g, current_edge)
    degree_list = [[]]*nb_vertices
    for vertex in g:
        degree = g[vertex][1]
        #append vertex to the list located at its degree in degree_list
        degree_list[degree].append(vertex)
        #if maximal degree vertex for now remember that it's the biggest one
        if degree > max_degree:
            max_degree = degree
    # Return graph:
    return g,degree_list,max_degree


def print_result(vertices):
    """
    INPUT: vertices is np.array of shape (nb_vertices,)
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
    for vertex in vertices:
        # 'Delete' vertex:
        g[vertex][0] = True
        degree_vertex = g[vertex][1]
        degree_list[degree_vertex].remove(vertex)
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            if not g[adj_vert][0]:
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert].remove(adj_vert)
                degree_list[degree_adj_vert-1].append(adj_vert)
                g[adj_vert][1] -= 1
    while (max_degree > 0) & (degree_list[max_degree] == []):
        max_degree -= 1



def un_del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'undelete'
    un_del_vert 'undeletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    global max_degree
    for vertex in vertices:
        # 'Undelete' vertex:
        g[vertex][0] = False
        degree_vertex = g[vertex][1]
        degree_list[degree_vertex].append(vertex)
        #If the vertex has a higher degree than max_degree, we update max_degree
        if g[vertex][1] > max_degree:
            max_degree = g[vertex][1]

        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            if not g[adj_vert][0]:
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert].remove(adj_vert)
                degree_list[degree_adj_vert+1].append(adj_vert)
                g[adj_vert][1] += 1
                #if the neighbour has after undeletion a higher degree than max degree we update it
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
    # get one of the highest degree vertices
    if max_degree != 0:
        vertex = degree_list[max_degree][0]
        # If vertex not deleted then take first adjacent vertex and return it:
        if (not g[vertex][0]):
            for adj_vert in g[vertex][2]:
                if not g[adj_vert][0]:
                    return [vertex, adj_vert]


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
    [u,v] = get_edge()
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
    del_vert([v])
    # Call function recursively:
    Sv = vc_branch(k-1)
    # 'Undelete' second vertex from graph:
    un_del_vert([v])
    # If vertex cover found return it plus the second vertex:
    if Sv is not None:
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


g,degree_list,max_degree = get_data()
vc()
