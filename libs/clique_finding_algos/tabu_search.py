import random
import networkx as nx

from typing import Set

from .utils import timer

class TabuCliqueFinder:
    def __init__(self, graph: nx.Graph, tabu_tenure: int = 10, max_iterations: int = 100):
        self.graph = graph
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        # Dictionary storing tabu moves with their expiration time
        self.tabu_list = {}  
        
    def is_clique(self, vertices: Set[int]) -> bool:
        # Use NetworkX's subgraph method to check if vertices form a clique
        if len(vertices) <= 1:
            return True
        subgraph = self.graph.subgraph(vertices)
        n = len(vertices)
        return subgraph.number_of_edges() == (n * (n - 1)) // 2
    
    def get_neighbors(self, current_solution: Set[int]) -> list[Set[int]]:
        neighbors = []
        potential_additions = set(self.graph.nodes()) - current_solution
        
        for vertex in potential_additions:
            if all(vertex in self.graph.neighbors(v) for v in current_solution):
                new_solution = current_solution | {vertex}
                neighbors.append(new_solution)
        
        # Try removing one vertex at a time
        for vertex in current_solution:
            new_solution = current_solution - {vertex}
            # Don't allow empty solutions
            if len(new_solution) > 0:  
                neighbors.append(new_solution)
                
        return neighbors
    
    def is_tabu(self, move: Set[int], iteration: int) -> bool:
        move_key = frozenset(move)
        return move_key in self.tabu_list and self.tabu_list[move_key] > iteration
    
    @timer
    def find_maximum_clique(self) -> Set[int]:
        
        # Start with a random vertex as initial solution
        current_solution = {random.choice(list(self.graph.nodes()))}
        best_solution = current_solution.copy()
        
        iteration = 0
        while iteration < self.max_iterations:
            neighbors = self.get_neighbors(current_solution)
            
            # Filter out tabu moves unless they lead to a better solution
            valid_moves = [
                neighbor for neighbor in neighbors
                if not self.is_tabu(neighbor, iteration) or len(neighbor) > len(best_solution)
            ]
            
            if not valid_moves:
                iteration += 1
                continue
                
            # Select the best non-tabu neighbor
            next_solution = max(valid_moves, key=len)
            
            # Update tabu list
            move_key = frozenset(next_solution)
            self.tabu_list[move_key] = iteration + self.tabu_tenure
            
            # Update current solution
            current_solution = next_solution
            
            # Update best solution if necessary
            if len(current_solution) > len(best_solution) and self.is_clique(current_solution):
                best_solution = current_solution.copy()
            
            iteration += 1
            
            # Clean up expired tabu moves
            self.tabu_list = {k: v for k, v in self.tabu_list.items() if v > iteration}
    
        return best_solution