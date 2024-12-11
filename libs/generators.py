import math
import random
import networkx as nx

from typing import  List, Tuple

def generate_clique(n: int) -> nx.Graph:
    return nx.complete_graph(n)

def generate_multiple_cliques(sizes: list, connections: int = 0) -> nx.Graph:
    G: nx.Graph = nx.Graph()
    offset: int = 0
    clique_nodes: list = []
    
    # Generate each clique
    for size in sizes:
        nodes = list(range(offset, offset + size))
        clique_nodes.append(nodes)
        clique = generate_clique(size)
        # Relabel nodes to avoid conflicts
        mapping = {i: i + offset for i in range(size)}
        clique = nx.relabel_nodes(clique, mapping)
        G.add_edges_from(clique.edges())
        offset += size
    
    # Add random connections between cliques
    for _ in range(connections):
        clique1, clique2 = random.sample(clique_nodes, 2)
        node1 = random.choice(clique1)
        node2 = random.choice(clique2)
        G.add_edge(node1, node2)
    
    return G

def generate_random_graph_config( min_cliques: int = 3, max_cliques: int = 10, min_nodes_per_clique: int = 1, max_nodes_per_clique: int = 100 ) -> Tuple[List[int], int, str]:
    """
    Generate a random list and a target number within [0, sum(list)].
    
    Args:
        min_size: Minimum length of the list
        max_size: Maximum length of the list
        min_value: Minimum value for list elements
        max_value: Maximum value for list elements
    """
    
    size = random.randint(min_cliques, max_cliques)
    cliques = [random.randint(min_nodes_per_clique, max_nodes_per_clique) for _ in range(size)]
    
    # total = sum(cliques)
    # connections = random.randint(0, total)
    
    filename = f"multiple_clique_graph_{'_'.join(map(str, cliques))}.json"
    return cliques, filename

def interclique_connections_calculator(clique_sizes: list, style: str = "") -> int:
    # num_edges = G.number_of_edges()
    # num_nodes = G.number_of_nodes()


    num_nodes = sum(clique_sizes)
    possible_num_edges = math.ceil((num_nodes * (num_nodes - 1)) / 2)
    current_num_edges = 0
    for clique in clique_sizes:
        current_num_edges += clique * (clique - 1) / 2

    connections = 0

    if style == "sparse":
        connections = math.ceil(possible_num_edges / 9)
    elif style == "dense":
        connections = math.ceil((possible_num_edges - current_num_edges) * 0.85)

    return connections         
