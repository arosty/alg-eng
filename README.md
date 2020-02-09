# Vertex Cover Solver

The project's goal is to solve the VERTEX COVER problem in the best computational time.

## What is new ?

The final version includes the following changes among many others:
* Reduction Rules:
    - Implementation of degree three reduction rule
    - Implementation of LP reduction rule
* Lower Bounds:
    - Implementation of LP lower bound
* Branching Strategy:
    - Implementation of Constrained Branching
The algorithm is now very flexible and many different parameters can be set.

The third version included the following changes among many small improvements:
* Reduction Rules:
    - Implementation of degree zero reduction rule
    - Implementation of high degree reduction rule
    - Updating degree one reduction rule
    - Implementation of 'extreme reduction rule'
    - Implementation of degree two reduction rule
    - Implementation of domination rule
* Lower Bound:
    - Implementation of clique cover lower bound

The second version included the following changes:
* Data structure :
    - Changing from local np.array list of edges to global dictionary incidence list 
    - Adding a global list that contains at index i all the vertices of degree i
    - Adding 2 global integers: highest degree and number of non-deleted vertices in the graph 
* Algorithm :
    - Graph preprocessing by adding to the vertex cover the neighbors of all degree 1 vertices
    - Refined search tree 
    - Clique-cover lower bound (clique cover created starting with lowest degree vertex)

## Download of test instances

The following command needs to be run in the "alg-eng-rosty-binetruy-1" directory.

```bash
curl -O http://fpt.akt.tu-berlin.de/alg-eng-data/data.zip
unzip data.zip
```

## Usage

```bash
python3 vertex_cover_solver.py < instance.file
```

## Special Requirements

CPLEX needs to be installed locally.
