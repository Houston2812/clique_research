import networkx as nx

from typing import Set, List

from .utils import timer

class BronKerbosch:
    """
    A class implementing the Bron-Kerbosch algorithm for finding maximal cliques
    in an undirected graph.
    """
    
    def __init__(self, graph: nx.Graph):
        """
        Initialize the BronKerbosch algorithm with a graph.
        
        Parameters:
            graph (nx.Graph): NetworkX undirected graph
        """
        self.graph = graph
        self.max_clique = set()  # For storing the maximum clique
        
    def _get_pivot(self, p: Set[int], x: Set[int]) -> int:
        """
        Choose a pivot vertex for optimization.
        
        Parameters:
            p (Set[int]): Set of prospective vertices
            x (Set[int]): Set of excluded vertices
            
        Returns:
            int: The chosen pivot vertex
        """
        return max(p.union(x), 
                  key=lambda u: len(set(self.graph.neighbors(u)).intersection(p)), 
                  default=None)
    
    def find_all_cliques(self, r: Set[int] = None, p: Set[int] = None, x: Set[int] = None) -> List[Set[int]]:
        """
        Find all maximal cliques in the graph using the Bron-Kerbosch algorithm.
        
        Parameters:
            r (Set[int]): Set of vertices in the current clique
            p (Set[int]): Set of prospective vertices
            x (Set[int]): Set of excluded vertices
            
        Returns:
            List[Set[int]]: List of all maximal cliques found
        """
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
        """
        Find the maximum clique in the graph using a modified Bron-Kerbosch algorithm.
        
        Parameters:
            r (Set[int]): Set of vertices in the current clique
            p (Set[int]): Set of prospective vertices
            x (Set[int]): Set of excluded vertices
            
        Returns:
            Set[int]: The maximum clique found
        """
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
        """
        Wrapper method with timer decorator for finding maximum clique.
        
        Returns:
            Set[int]: The maximum clique found
        """
        return self.find_maximum_clique()
    

def bron_kerbosch(graph: nx.Graph, r: Set[int] = None, p: Set[int] = None, x: Set[int] = None) -> List[Set[int]]:
    """
    Implements recursive Bron-Kerbosch algorithm with pivot for finding all maximal cliques.
    
    Parameters:
        - graph: NetworkX undirected graph
        - r: Set of vertices in the current clique
        - p: Set of prospective vertices
        - x: Set of excluded vertices
    
    Returns:
        - List of maximal cliques
    """

    if r is None:
        r = set()
        p = set(graph.nodes())
        x = set()
    
    cliques = []
    
    if not p and not x:
        return [r] if r else []
    
    pivot = max(p.union(x), key=lambda u: len(set(graph.neighbors(u)).intersection(p)), default=None)
    
    # Iterate through vertices in P \ N(pivot)
    pivot_neighbors = set(graph.neighbors(pivot)) if pivot is not None else set()
    for vertex in p.difference(pivot_neighbors):
        vertex_neighbors = set(graph.neighbors(vertex))
        
        # Recursive call with updated sets
        new_r = r.union({vertex})
        new_p = p.intersection(vertex_neighbors)
        new_x = x.intersection(vertex_neighbors)
        
        cliques.extend(bron_kerbosch(graph, new_r, new_p, new_x))
        
        # Move vertex from P to X
        p.remove(vertex)
        x.add(vertex)
    
    return cliques

def bron_kerbosch_max_clique(graph: nx.Graph, r: Set[int] = None, p: Set[int] = None, x: Set[int] = None) -> Set[int]:
    """
    Modified Bron-Kerbosch algorithm to find the maximum clique in an undirected graph.
    
    Parameters:
    - graph: NetworkX undirected graph
    - r: Set of vertices in the current clique
    - p: Set of prospective vertices
    - x: Set of excluded vertices
    
    Returns:
    - Set representing the maximum clique found
    """

    if r is None:
        r = set()
        p = set(graph.nodes())
        x = set()
    
    # Store the current maximum clique
    global max_clique
    if 'max_clique' not in globals():
        max_clique = set()
    
    # Update max_clique if current clique is larger
    if len(r) > len(max_clique):
        max_clique = r.copy()
    
    # Early stopping if we can't beat the current maximum
    if len(r) + len(p) <= len(max_clique):
        return max_clique
    
    # Choose pivot vertex for efficiency
    pivot = max(p.union(x), key=lambda u: len(set(graph.neighbors(u)).intersection(p)), default=None)
    
    # Iterate through vertices in P \ N(pivot)
    pivot_neighbors = set(graph.neighbors(pivot)) if pivot is not None else set()
    for vertex in sorted(p.difference(pivot_neighbors), 
                        key=lambda v: len(set(graph.neighbors(v)).intersection(p)), 
                        reverse=True):  # Degree ordering heuristic
        vertex_neighbors = set(graph.neighbors(vertex))
        
        # Recursive call with updated sets
        new_r = r.union({vertex})
        new_p = p.intersection(vertex_neighbors)
        new_x = x.intersection(vertex_neighbors)
        
        bron_kerbosch_max_clique(graph, new_r, new_p, new_x)
        
        # Move vertex from P to X
        p.remove(vertex)
        x.add(vertex)
    
    return max_clique

@timer
def bron_kerbosch_max_clique_finder(graph: nx.Graph) -> set:
    result: set = bron_kerbosch_max_clique(graph)
    return result