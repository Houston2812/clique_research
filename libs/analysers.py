import networkx as nx
import matplotlib.pyplot as plt


def analyze_graph(G: nx.Graph, cliques: bool = True):
    
    print("Graph Analysis:")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    print(f"Density: {nx.density(G):.3f}")
    
    # if nx.is_connected(G):
        # print(f"Average shortest path length: {nx.average_shortest_path_length(G):.2f}")
        # print(f"Diameter: {nx.diameter(G)}")
    # else:
        # print("Graph is not connected")
    
    if cliques:
        # cliques = list(nx.find_cliques(G))
        # print(f"{len(cliques)} cliques are present in the Graph")
        # cliques.sort(key=len, reverse=True)
        
        # print("\n5 Largest Cliques:")
        # for i, clique in enumerate(cliques[:5], 1):
        #     print(f"\tClique {i}: Size={len(clique)}, Nodes={clique}")

        # return cliques[0]
        max_clique = set(nx.max_weight_clique(G, weight=None)[0])
        print(f"Maximum clique: {max_clique}")
        return max_clique
    
    return None

    return None
    # print("Cliques in graph:")
    # for i, clique in enumerate(nx.find_cliques(G), 1):
    #     print(f"\tClique {i}: {clique}")

def calculate_correlation(list1, list2, handle_different_lengths='error'):
    """
    Calculate matching ratio between two lists of strings.
    
    Args:
        list1: First list of strings
        list2: Second list of strings
        handle_different_lengths: How to handle different length lists
            'error' - raise ValueError
            'truncate' - use overlapping parts
    
    Returns:
        Ratio of matching strings
    """
    if len(list1) != len(list2):
        if handle_different_lengths == 'error':
            raise ValueError(f"Lists have different lengths: {len(list1)} vs {len(list2)}")
        elif handle_different_lengths == 'truncate':
            # Use the length of the shorter list
            min_length = min(len(list1), len(list2))
            list1 = list1[:min_length]
            list2 = list2[:min_length]
            print(f"Warning: Lists truncated to length {min_length}")
    
    n = len(list1)
    if n == 0:
        raise ValueError("Lists are empty")
    
    # Count matching strings
    matches = sum(1 for x, y in zip(list1, list2) if x == y)
    return matches / n

def create_comparison_table(data_dict, title="String Matching Table", handle_different_lengths='truncate'):
    """
    Create a simple table showing string matching ratios.
    """
    variables = list(data_dict.keys())
    n = len(variables)
    
    # Calculate matching matrix
    match_matrix = []
    for var1 in variables:
        row = []
        for var2 in variables:
            try:
                match_ratio = calculate_correlation(
                    data_dict[var1], 
                    data_dict[var2],
                    handle_different_lengths
                )
                row.append(match_ratio)
            except ValueError as e:
                print(f"Error calculating matches between {var1} and {var2}: {e}")
                row.append(float('nan'))
        match_matrix.append(row)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    
    # Create table
    table = ax.table(
        cellText=[[f'{x:.2f}' if not isinstance(x, str) else x 
                   for x in row] for row in match_matrix],
        rowLabels=variables,
        colLabels=variables,
        cellLoc='center',
        loc='center',
        bbox=[0.2, 0.2, 0.6, 0.6]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    plt.title(title, pad=20)
    plt.show()

def calculate_inter_clique_density(G, cliques):
    """
    Calculate density of edges between cliques in a NetworkX graph.
    
    Args:
        G: NetworkX graph
        cliques: List of lists, where each inner list contains nodes of a clique
    
    Returns:
        float: Inter-clique density value between 0 and 1
        list: List of inter-clique edges
    """
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

def example_usage():
    # Create a graph with three cliques
    G = nx.Graph()
    
    # Define cliques
    cliques = [
        ['A', 'B', 'C'],     # Clique 1
        ['D', 'E', 'F'],     # Clique 2
        ['G', 'H']           # Clique 3
    ]
    
    # Add all nodes
    G.add_nodes_from([node for clique in cliques for node in clique])
    
    # Add edges within cliques
    for clique in cliques:
        for i in range(len(clique)):
            for j in range(i + 1, len(clique)):
                G.add_edge(clique[i], clique[j])
    
    # Add some inter-clique edges
    inter_clique_edges = [('C', 'D'), ('F', 'G'), ('A', 'E')]
    G.add_edges_from(inter_clique_edges)
    
    # Calculate density
    density, found_inter_edges = calculate_inter_clique_density(G, cliques)
    
    # Print results
    print("Graph information:")
    print(f"Nodes: {G.nodes()}")
    print(f"Total edges: {G.edges()}")
    print(f"\nCliques: {cliques}")
    print(f"Inter-clique edges: {found_inter_edges}")
    print(f"Inter-clique density: {density:.3f}")
    
    # Visualize the graph
    print("\nGraph visualization:")
    pos = nx.spring_layout(G)
    
    # Color nodes based on their clique
    colors = []
    for node in G.nodes():
        for i, clique in enumerate(cliques):
            if node in clique:
                colors.append(i)
                break
    
    # Draw the graph
    nx.draw(G, pos, 
           node_color=colors, 
           with_labels=True,
           node_size=500,
           font_size=16,
           font_weight='bold')
    
    # You can display the graph using:
    # import matplotlib.pyplot as plt
    # plt.show()

if __name__ == "__main__":
    example_usage()
