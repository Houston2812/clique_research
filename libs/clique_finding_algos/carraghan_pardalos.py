import networkx as nx

from typing import Set, Tuple, Dict

from .utils import timer

import networkx as nx

def compute_degree_map(graph: nx.Graph) -> Dict[int, int]:
    return {v: len(list(graph.neighbors(v))) for v in graph.nodes()}

def sort_by_degree(vertices: Set[int], degree_map: Dict[int, int]) -> list:
    return sorted(vertices, key=lambda x: -degree_map[x])

def color_vertices(graph: nx.Graph, vertices: Set[int], degree_map: Dict[int, int], color_cache: Dict[frozenset, Dict[int, int]]) -> Dict[int, int]:
    visited_vertices = frozenset(vertices)
    if visited_vertices in color_cache:
        return color_cache[visited_vertices]
        
    colors = {}
    for vertex in sort_by_degree(vertices, degree_map):
        used_colors = {colors[n] for n in graph.neighbors(vertex) if n in colors}
        for color in range(len(vertices)):
            if color not in used_colors:
                colors[vertex] = color
                break
    
    color_cache[visited_vertices] = colors
    return colors

def calculate_upper_bound(graph: nx.Graph, candidates: Set[int], degree_map: Dict[int, int], color_cache: Dict[frozenset, Dict[int, int]]) -> int:
    colors = color_vertices(graph, candidates, degree_map, color_cache)
    return len(set(colors.values()))

def find_new_candidates(graph: nx.Graph, vertex: int, candidates: Set[int]) -> Set[int]:
    return candidates & set(graph.neighbors(vertex))

def backtrack(graph: nx.Graph, clique: Set[int], candidates: Set[int], 
             best_size: int, degree_map: Dict[int, int], 
             color_cache: Dict[frozenset, Dict[int, int]]) -> Set[int]:
    
    if not candidates:
        return clique
        
    # Pruning using upper bound
    if len(clique) + calculate_upper_bound(graph, candidates, degree_map, color_cache) <= best_size:
        return clique
        
    max_clique = clique
    sorted_candidates = sort_by_degree(candidates, degree_map)
    
    for v in sorted_candidates:
        if len(clique) + len(candidates) <= len(max_clique):
            break
            
        new_clique = clique | {v}
        new_candidates = find_new_candidates(graph, v, candidates)
        
        result_clique = backtrack(graph, new_clique, new_candidates, 
                                len(max_clique), degree_map, color_cache)
        
        if len(result_clique) > len(max_clique):
            max_clique = result_clique
            best_size = len(max_clique)
        
        candidates.remove(v)
        
    return max_clique

@timer
def optimized_carraghan_pardalos(graph: nx.Graph) -> Set[int]:
    degree_map = compute_degree_map(graph)
    color_cache: Dict[frozenset, Dict[int, int]] = {}
    
    initial_candidates = set(sort_by_degree(graph.nodes(), degree_map))
    return backtrack(graph, set(), initial_candidates, 0, degree_map, color_cache)