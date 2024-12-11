import networkx as nx

from typing import Set, Tuple

from .utils import timer

import networkx as nx

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