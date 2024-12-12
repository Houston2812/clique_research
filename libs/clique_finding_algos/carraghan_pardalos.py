import networkx as nx

from typing import Set, Tuple, Dict

from .utils import timer

import networkx as nx


@timer
def optimized_carraghan_pardalos(graph: nx.Graph):
    """
    Optimized implementation of Carraghan-Pardalos algorithm for finding maximal cliques.
    
    Key optimizations:
    1. Vertex ordering by degree
    2. Upper bound pruning
    3. Coloring-based pruning
    4. Neighbor degree optimization
    5. Cache for vertex colors
    """
    
    # Pre-compute and cache vertex degrees
    degree_map = {v: len(list(graph.neighbors(v))) for v in graph.nodes()}
    
    # Cache for vertex colors to avoid recomputation
    color_cache: Dict[frozenset, Dict[int, int]] = {}
    
    def color_vertices(vertices: Set[int]) -> Dict[int, int]:
        """
        Colors vertices greedily for pruning purposes.
        Returns a dictionary mapping vertex to color number.
        """
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
        """
        Calculates upper bound using vertex coloring.
        Fewer colors means smaller possible clique size.
        """
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

@timer
def carraghan_pardalos_maximal_clique(graph: nx.Graph):
    def backtrack(clique, candidates):
        if not candidates:
            return clique

        max_clique = clique
        for v in list(candidates):
            new_clique = clique | {v}
            new_candidates = candidates & set(graph.neighbors(v))
            result_clique = backtrack(new_clique, new_candidates)

            if len(result_clique) > len(max_clique):
                max_clique = result_clique

            candidates.remove(v)

        return max_clique

    return backtrack(set(), set(graph.nodes()))


@timer
def carraghan_pardalos_maximal_clique_pivot(graph: nx.Graph):
    def backtrack(clique, candidates, excluded):
        if not candidates and not excluded:
            return clique

        max_clique = clique
        pivot = next(iter(candidates | excluded))  # Pivot optimization
        pivot_neighbors = set(graph.neighbors(pivot))

        for v in list(candidates - pivot_neighbors):
            new_clique = clique | {v}
            new_candidates = candidates & set(graph.neighbors(v))
            new_excluded = excluded & set(graph.neighbors(v))
            result_clique = backtrack(new_clique, new_candidates, new_excluded)

            if len(result_clique) > len(max_clique):
                max_clique = result_clique

            candidates.remove(v)
            excluded.add(v)

        return max_clique

    return backtrack(set(), set(graph.nodes()), set())

# class CarraghanPardalosCF:
#     def __init__(self, graph: nx.Graph):
#         self.graph = graph
#         self.n = graph.number_of_nodes()
#         # Convert graph to adjacency matrix form as used in the paper
#         self.adj_matrix = nx.to_numpy_array(graph, dtype=int)
#         # Best solution found so far
#         self.max_clique_size = 0
#         self.max_clique = set()
#         # Order vertices by degree (as specified in the paper)
#         self.vertex_order = sorted(graph.nodes(), 
#                                  key=lambda v: graph.degree(v),
#                                  reverse=True)
#         # Create reverse mapping for vertex ordering
#         self.vertex_index = {v: i for i, v in enumerate(self.vertex_order)}

#     def compute_upper_bound(self, candidates: Set[int], current_size: int) -> int:
#         if not candidates:
#             return current_size
        
#         colors = {}
#         uncolored = candidates.copy()

#         color = 0
#         while uncolored:
#             color_class = set()
#             for v in sorted(uncolored, key=lambda x: self.vertex_index[x]):
#                 if all(not self.is_connected(v, u) for u in color_class):
#                     color_class.add(v)
            
#             for v in color_class:
#                 colors[v] = color
#                 uncolored.remove(v)

#             color += 1

#         return current_size + color
    
#     def get_neighbors(self, vertex: int, candidates: Set[int]) -> Set[int]:
#         neighbors: Set[int] = set()
#         for v in candidates:
#             if self.is_connected(vertex, v):
#                 neighbors.add(v)
        
#         return neighbors
#         # return {v for v in candidates if self.is_connected(vertex, v)}

#     def is_connected(self, v1: int, v2: int) -> bool:
#         # return self.adj_matrix[self.vertex_index[v1]][self.vertex_index[v2]] == 1

#         if self.adj_matrix[self.vertex_index[v1]][self.vertex_index[v2]] == 1:
#             return True
#         else:
#             return False
        
#     def expand(self, candidates: Set[int], current_clique: Set[int]) -> None:
#         while candidates:
#             upper_bound = self.compute_upper_bound(candidates, len(current_clique))
#             if upper_bound <= self.max_clique_size:
#                 return
            
#             vertex = max(candidates, key=lambda v: len(self.get_neighbors(v, candidates)))
#             candidates.remove(vertex)

#             new_candidates = candidates & self.get_neighbors(vertex, candidates)
#             new_clique = current_clique | {vertex}
#             if len(new_clique) > self.max_clique_size:
#                 self.max_clique_size = len(new_clique)
#                 self.max_clique = new_clique

#             if new_candidates:
#                 self.expand(new_candidates, new_clique)

#     @timer
#     def find_maximum_clique(self) -> Tuple[Set[int], float]:
#         initial_candidates = set(self.vertex_order)
#         self.expand(initial_candidates, set())

#         return self.max_clique