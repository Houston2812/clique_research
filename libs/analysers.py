import networkx as nx
import matplotlib.pyplot as plt

def analyze_graph(G: nx.Graph, cliques: bool = True):
    print("Graph Analysis:")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    print(f"Density: {nx.density(G):.3f}")
    
    if cliques:
        max_clique = set(nx.max_weight_clique(G, weight=None)[0])
        print(f"Maximum clique: {max_clique}")
        return max_clique
    return None

def calculate_correlation(list1, list2, handle_different_lengths='error'):
   
    if len(list1) != len(list2):
        if handle_different_lengths == 'error':
            raise ValueError(f"Lists have different lengths")
        elif handle_different_lengths == 'truncate':
            # Use the length of the shorter list
            min_length = min(len(list1), len(list2))
            list1 = list1[:min_length]
            list2 = list2[:min_length]
            print(f"Lists truncated to length {min_length}")
    
    n = len(list1)
    if n == 0:
        raise ValueError("Lists are empty")
    
    # Count matching strings
    matches = sum(1 for x, y in zip(list1, list2) if x == y)
    return matches / n

def calculate_inter_clique_density(G, cliques):
    # Convert cliques to sets for faster lookup
    clique_sets = [set(clique) for clique in cliques]
    
    # Find inter-clique edges
    inter_clique_edges = []
    for edge in G.edges():
        v1, v2 = edge
        # Find which cliques contain these vertices
        v1_clique = None
        v2_clique = None
        
        for idx, clique in enumerate(clique_sets):
            if v1 in clique:
                v1_clique = idx
            if v2 in clique:
                v2_clique = idx
                
        # If vertices belong to different cliques, it's an inter-clique edge
        if v1_clique is not None and v2_clique is not None and v1_clique != v2_clique:
            inter_clique_edges.append(edge)
    
    # Calculate maximum possible inter-clique edges
    max_inter_edges = 0
    for i in range(len(cliques)):
        for j in range(i + 1, len(cliques)):
            # Multiple number of vertices in each clique pair
            max_inter_edges += len(cliques[i]) * len(cliques[j])
    
    if max_inter_edges == 0:
        return 0.0, inter_clique_edges
        
    density = len(inter_clique_edges) / max_inter_edges
    return density, inter_clique_edges

