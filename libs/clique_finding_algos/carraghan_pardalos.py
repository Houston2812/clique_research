import networkx as nx

from typing import Set, Tuple, Dict

from .utils import timer

import networkx as nx


@timer
def optimized_carraghan_pardalos(graph: nx.Graph):
  
    # Pre-compute and cache vertex degrees
    degree_map = {v: len(list(graph.neighbors(v))) for v in graph.nodes()}
    
    # Cache for vertex colors to avoid recomputation
    color_cache: Dict[frozenset, Dict[int, int]] = {}
    
    def color_vertices(vertices: Set[int]) -> Dict[int, int]:
      
        frozen_vertices = frozenset(vertices)
        if frozen_vertices in color_cache:
            return color_cache[frozen_vertices]
            
        colors = {}
        for vertex in sorted(vertices, key=lambda x: -degree_map[x]):
            used_colors = {colors[n] for n in graph.neighbors(vertex) if n in colors}
            for color in range(len(vertices)):
                if color not in used_colors:
                    colors[vertex] = color
                    break
        
        color_cache[frozen_vertices] = colors
        return colors

    def calculate_upper_bound(candidates: Set[int]) -> int:
       
        return len(set(color_vertices(candidates).values()))

    def backtrack(clique: Set[int], candidates: Set[int], best_size: int) -> Set[int]:
        if not candidates:
            return clique
            
        # If upper bound shows no better solution possible, prune
        if len(clique) + calculate_upper_bound(candidates) <= best_size:
            return clique
            
        max_clique = clique
        
        # Sort candidates by degree for better pruning
        sorted_candidates = sorted(candidates, key=lambda x: -degree_map[x])
        
        for v in sorted_candidates:
            if len(clique) + len(candidates) <= len(max_clique):
                break
                
            new_clique = clique | {v}
            # Optimize neighbor intersection
            new_candidates = candidates & set(graph.neighbors(v))
            
            result_clique = backtrack(new_clique, new_candidates, len(max_clique))
            if len(result_clique) > len(max_clique):
                max_clique = result_clique
                best_size = len(max_clique)
            
            candidates.remove(v)
            
        return max_clique

    # Start with vertices ordered by degree
    initial_candidates = set(sorted(graph.nodes(), key=lambda x: -degree_map[x]))
    return backtrack(set(), initial_candidates, 0)

