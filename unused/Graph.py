from collections import defaultdict, deque

class Graph:
    def __init__(self, adjacency_list):
        self.graph = defaultdict(list)
        self.build_graph(adjacency_list)

    def build_graph(self, adjacency_list):
        for idx, neighbors in enumerate(adjacency_list):
            for neighbor in neighbors:
                self.graph[idx].append(neighbor)
                self.graph[neighbor].append(idx)
    
    def is_connected(self, start_node, removed_node):
        visited = set()
        queue = deque([start_node])
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph[node]:
                    if neighbor != removed_node and neighbor not in visited:
                        queue.append(neighbor)
        
        return visited

    def remove_node_and_check(self, node_to_remove):
        nodes = set(self.graph.keys())
        nodes.discard(node_to_remove)
        if not nodes:
            return []
        
        start_node = next(iter(nodes))
        visited = self.is_connected(start_node, node_to_remove)
        
        if len(visited) == len(nodes):
            return []
        
        subgraphs = []
        remaining_nodes = nodes - visited
        subgraphs.append(list(visited))
        
        while remaining_nodes:
            start_node = next(iter(remaining_nodes))
            new_visited = self.is_connected(start_node, node_to_remove)
            subgraphs.append(list(new_visited))
            remaining_nodes -= new_visited
        
        return subgraphs