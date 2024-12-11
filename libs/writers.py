import json
import networkx as nx
import matplotlib.pyplot as plt

from pathlib import Path

def graph_to_json(G: nx.Graph, filename: str, is_single_clique: bool = False) -> dict:
    default_weight: int= 1

    single_output_folder: Path = Path("graphs/single/")
    multiple_output_folder: Path = Path("graphs/multiple/")
    output: Path = None

    if check_directories(single_output_folder, create=True):
        print(f"Created directories for: {single_output_folder}")
    else:
        print(f"Directory does not exist: {single_output_folder}")

    if check_directories(multiple_output_folder, create=True):
        print(f"Created directories for: {multiple_output_folder}")
    else:
        print(f"Directory does not exist: {multiple_output_folder}")

    if is_single_clique:
        output = single_output_folder / filename
    else:
        output = multiple_output_folder / filename

    graph: dict = {}
    
    for node in G.nodes():
        neighbors: dict = {}
        for neighbor in G.neighbors(node):
            connection: int = G.get_edge_data(node, neighbor).get('weight', default_weight)
            neighbors[neighbor] = connection
        
        graph[node] = neighbors
    
    # Write to JSON file
    with open(output, 'w') as f:
        json.dump(graph, f, indent=4)
    
    return graph

def check_directories(path: Path, create: bool =False) -> bool:
    if create:
        path.mkdir(parents=True, exist_ok=True)
        return True
    return path.exists()

def load_graph_from_json(json_path: Path) -> nx.Graph:
    G: nx.Graph = nx.Graph()
   
    with open(json_path, 'r') as f:
        adj_list = json.load(f)
    
        for node, neighbors in adj_list.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

    return G