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