import networkx as nx

from typing import Set, List

from .utils import timer

class BronKerbosch:
   
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.max_clique = set() 
        
    def _get_pivot(self, p: Set[int], x: Set[int]) -> int:
      
        return max(p.union(x), 
                  key=lambda u: len(set(self.graph.neighbors(u)).intersection(p)), 
                  default=None)
    
    def find_all_cliques(self, r: Set[int] = None, p: Set[int] = None, x: Set[int] = None) -> List[Set[int]]:
        if r is None:
            r = set()
            p = set(self.graph.nodes())
            x = set()
        
        cliques = []
        
        if not p and not x:
            return [r] if r else []
        
        pivot = self._get_pivot(p, x)
        pivot_neighbors = set(self.graph.neighbors(pivot)) if pivot is not None else set()
        
        for vertex in p.difference(pivot_neighbors):
            vertex_neighbors = set(self.graph.neighbors(vertex))
            
            new_r = r.union({vertex})
            new_p = p.intersection(vertex_neighbors)
            new_x = x.intersection(vertex_neighbors)
            
            cliques.extend(self.find_all_cliques(new_r, new_p, new_x))
            
            p.remove(vertex)
            x.add(vertex)
        
        return cliques
    
    def find_maximum_clique(self, r: Set[int] = None, p: Set[int] = None, x: Set[int] = None) -> Set[int]:
        
        if r is None:
            r = set()
            p = set(self.graph.nodes())
            x = set()
            self.max_clique = set()  # Reset max_clique for new search
        
        if len(r) > len(self.max_clique):
            self.max_clique = r.copy()
        
        if len(r) + len(p) <= len(self.max_clique):
            return self.max_clique
        
        pivot = self._get_pivot(p, x)
        pivot_neighbors = set(self.graph.neighbors(pivot)) if pivot is not None else set()
        
        for vertex in sorted(p.difference(pivot_neighbors), 
                           key=lambda v: len(set(self.graph.neighbors(v)).intersection(p)), 
                           reverse=True):
            vertex_neighbors = set(self.graph.neighbors(vertex))
            
            new_r = r.union({vertex})
            new_p = p.intersection(vertex_neighbors)
            new_x = x.intersection(vertex_neighbors)
            
            self.find_maximum_clique(new_r, new_p, new_x)
            
            p.remove(vertex)
            x.add(vertex)
        
        return self.max_clique

    @timer
    def find_max_clique(self) -> Set[int]:
        return self.find_maximum_clique()
    