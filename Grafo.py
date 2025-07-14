import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import math
import heapq
import pdb
from collections import deque

default_pos_bi = {
    'Vila Nova de Famalicão': {'pos': (0, 0), 'connections': [('Gavião', 27), ('Antas', 22), ('Calendário', 27), ('Mouquim', 34), ('Louro', 40), ('Brufe', 30)]},
    'Antas': {'pos' : (0.9, -1.2), 'connections' : [('Vila Nova de Famalicão', 22), ('Calendário', 39), ('Esmeriz', 26), ('Vale', 52)]},
    'Calendário': {'pos' : (-1, -1.466), 'connections' : [('Vila Nova de Famalicão', 27), ('Brufe', 16), ('Antas', 39)]},
    'Gavião': {'pos' : (1.052, 1.736), 'connections' : [('Vila Nova de Famalicão', 27), ('Vale', 35), ('Mouquim', 30), ('Antas', 50)]},
    'Brufe': {'pos' : (-1.396, -0.1), 'connections' : [('Vila Nova de Famalicão', 30), ('Louro', 34), ('Outiz', 25), ('Calendário', 16)]},
    'Outiz': {'pos' : (-2.92, 0.954), 'connections' : [('Vilarinho', 52), ('Louro', 27), ('Brufe', 25)]},
    'Mouquim': {'pos' : (-0.447, 2.46), 'connections' : [('Louro', 16), ('Vila Nova de Famalicão', 34), ('Gavião', 30)]},
    'Esmeriz': {'pos' : (0.469, -3.559), 'connections' : [('Antas', 26)]},
    'Vale': {'pos' : (3.322, 1.123), 'connections' : [('Gavião', 35), ('Antas', 52)]},
    'Louro': {'pos' : (-1.383, 2.4), 'connections' : [('Vila Nova de Famalicão', 40), ('Brufe', 34), ('Outiz', 27), ('Mouquim', 16)]},
    'Vilarinho': {'pos' : (-2.839, -2.616), 'connections' : [('Outiz', 52)]}
}


class Grafo:
    def __init__(self, graph_dict=default_pos_bi):
        self.nx = nx.Graph()
        self.g = graph_dict
        self.trainedHeuristic = {}
        
        for node, data in graph_dict.items():
            node_name = node
            node_pos = data.get('pos', (0, 0))  # Default position is (0, 0) if not specified
            self.nx.add_node(node_name, pos=node_pos)

            for connection, cost in data.get('connections', []):
                self.nx.add_edge(node_name, connection, weight=cost)

    
    def heuristicFunction(self, initial_node, goal_node):
        if initial_node in self.nx.nodes:
            initial_pos = self.nx.nodes[initial_node]['pos']
        else:
            raise KeyError (f"{initial_node} does not exist in the graph")
        if goal_node in self.nx.nodes:
            goal_pos = self.nx.nodes[goal_node]['pos']
        else:
            raise KeyError (f"{goal_node} does not exist in the graph")
        
        #Usa-se a distância entre dois pontos num plano como heuristica com uma escala
        heuristic = (((goal_pos[0] - initial_pos[0]) **2 + (goal_pos[1] - initial_pos[1]) **2) **0.5) * 10
        return math.floor(heuristic)
    
    def trainedHeuristicFunction(self, initial_node, goal_node):
        if initial_node not in self.nx.nodes:
            raise KeyError (f"{initial_node} does not exist in the graph")
        if goal_node not in self.nx.nodes:
            raise KeyError (f"{goal_node} does not exist in the graph")
        if initial_node in self.trainedHeuristic:
            for item in self.trainedHeuristic[initial_node]:
                if item[0] == goal_node:
                    return item[1]  
        raise KeyError ("ERROR")
    
    def heuristicPath(self, start, goals):
        heuristicSum = 0
        begin = start
        for goal in goals:
            heuristicSum = heuristicSum + self.heuristicFunction(begin, goal)
            begin = goal
        return heuristicSum
    
    def iddfs(self, start, goal, depth):
        expansao = []
        def depth_limited_dfs(current, goal, depth_limit):
            return recursive_dfs(current, goal, depth_limit, 0, [], 0)

        def recursive_dfs(current, goal, depth_limit, current_depth, path, cost):
            expansao.append(current)
            if current in goal:
                return path + [current], current, expansao, cost, depth_limit

            if current_depth == depth_limit:
                return None

            for neighbor, custo in self.g[current]['connections']:
                if neighbor not in path:
                    result = recursive_dfs(neighbor, goal, depth_limit, current_depth + 1, path + [current], cost + custo)
                    if result is not None:
                        return result

            return None
        
        while True:
            result = depth_limited_dfs(start, goal, depth)
            if result is not None:
                return result
            depth += 1
    
    def iddfs_tsp(self, start, goalss):
        goals = goalss.copy()
        expansao = []
        node = start
        custoTotal = 0
        path = []
        initial_depth = 0
        while (goals != []):
            next_path, goal, next_expansao, next_custo, depth = self.iddfs(node, goals, initial_depth)
            path = path[:-1] + next_path
            expansao = expansao[:-1] + next_expansao
            custoTotal = custoTotal + next_custo
            goals.remove(goal)
            node = goal
            initial_depth = depth
        
        return path, custoTotal, expansao
    
    def dfs_search_tsp(self, start, goals, visited=None, path=None, expansao=None, custo=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        if expansao is None:
            expansao = []
        if custo is None:
            custo = 0

        visited.add(start)
        path.append(start)
        expansao.append(start)

        if start in goals:
            goals.remove(start)
            visited = set()
            if not goals:
                return path, custo, expansao

        for neighbor, cost in self.g[start]['connections']:
            if neighbor not in visited:
                custo = custo + cost
                result = self.dfs_search_tsp(neighbor, goals.copy(), visited, path.copy(), expansao, custo)
                if result:
                    return result

        return None
    
    def busca_gulosa(self, inicio, objetivos, function, destinos=None):
        if objetivos == []:
            return [], 0, [], []
        for objetivo in objetivos:
            fronteira = [(function(inicio, objetivo), inicio, [inicio], 0)]
        explorados = set()
        expansao = []
        if destinos is None:
            destinos = []

        while fronteira:
            _, estado_atual, path, custo = heapq.heappop(fronteira)

            if estado_atual in objetivos:
                # Se chegamos ao objetivo, retornamos o caminho
                objetivos.remove(estado_atual)
                destinos.append(estado_atual)
                next_path, next_custo, next_expansao, _ = self.busca_gulosa(estado_atual, objetivos, function, destinos)
                return path + next_path[1:], custo + next_custo, expansao + [estado_atual] + next_expansao[1:], destinos

            if estado_atual not in explorados:
                explorados.add(estado_atual)
                expansao.append(estado_atual)

                # Expandir os vizinhos e adicionar à fronteira
                for vizinho, cost in self.g[estado_atual]['connections']:
                    if vizinho not in explorados:
                        new_path = path + [vizinho]
                        new_custo = custo + cost
                        for objetivo in objetivos:
                            heapq.heappush(fronteira, (function(vizinho, objetivo), vizinho, new_path, new_custo))

        return None
    
    def bfs(self, start, goal):
        if goal == []:
            return [start], 0, [start]
        goals = goal.copy()
        queue = deque([(start, [start], 0)])
        expansao = [start]
        
        visited = set([start])

        
        if start == goal:
            return [start]

        while queue:
            
            current, path , totalCost= queue.popleft()
            
            for neighbor, cost in self.g[current]['connections']:
                if neighbor not in visited:
                    
                    if neighbor in goals:
                        goals.remove(neighbor)
                        next_path, next_cost, next_expansao = self.bfs(neighbor, goals)
                        return path + next_path, totalCost + cost + next_cost, expansao + next_expansao
                    
                    expansao = expansao + [neighbor]

                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], totalCost + cost))

        # If no path is found
        return None
    
    def custoUniforme (self, inicio, fins):
        # Inicialização
        if fins == []:
            return [], 0, []
        finss = fins.copy()
        fila_prioridade = [(0, inicio, [])]
        visitados = set()
        expansao = []

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)
                 
                if no_atual in finss:
                    finss.remove(no_atual)
                    next_caminho, next_custo, next_expansao = self.custoUniforme(no_atual, finss)
                    return (caminho + next_caminho[1:], custo + next_custo, expansao + next_expansao[1:])

                for vizinho, custo_aresta in self.g[no_atual]['connections']:
                    if vizinho not in visitados:
                        heapq.heappush(fila_prioridade, (custo + custo_aresta, vizinho, caminho))

        return [], float('inf'), []

    def a_estrela(self, inicio, fins, function, destinos=None):
        # Inicialização
        if fins == []:
            return [], 0, [], []
        for fim in fins:
            fila_prioridade = [(0 + function(inicio, fim), inicio, [])]
        visitados = set()
        expansao = []
        if destinos is None:
            destinos = []

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)

                if no_atual == fim:
                    fins.remove(no_atual)
                    destinos.append(no_atual)
                    next_path, next_custo, next_expansao, _ = self.a_estrela(no_atual, fins, function, destinos)
                    return caminho + next_path[1:], round(custo, 2) + next_custo, expansao + next_expansao[1:], destinos

                for vizinho, custo_aresta in self.g[no_atual]['connections']:
                    if vizinho not in visitados:
                        # Adiciona custo da aresta e heurística do próximo nó
                        custo_total_vizinho = custo - function(no_atual, fim) + custo_aresta + function(vizinho, fim)
                        heapq.heappush(fila_prioridade, (custo_total_vizinho, vizinho, caminho))

        return [], float('inf'), [], []

    def custoCaminho(self, path):
        cost = 0

        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            # Find the connection between the current and next nodes
            connections = self.g[current_node]['connections']
            for connection in connections:
                if connection[0] == next_node:
                    cost += connection[1]
                    break  # Break the loop once the connection is found
        return cost


    def trainHeuristic (self):
        keys = list(self.g.keys())

        for i in range(len(keys)):
            current_key = keys[i]
            
            for j in range(len(keys)):
                other_key = keys[j]
                path, _, _, _ = self.a_estrela(current_key, [other_key], self.heuristicFunction)
                newheuristic = self.heuristicPath(current_key, path)
                if current_key in self.trainedHeuristic:
                    self.trainedHeuristic[current_key].append((other_key, newheuristic))
                else:
                    self.trainedHeuristic[current_key] = [(other_key, newheuristic)]

            
    def visualize_graph_with_heuristic(self, goal_nodes, function):
        plt.clf()
        plt.ion()
        plt.title("Grafo com heurísticas em " + str (goal_nodes))
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}
        heuristic_labels = []
        offset = 0.2
        # Calculate heuristic values and position them slightly below the nodes
        for goal_node in goal_nodes:
            temp = [(pos[node][0], pos[node][1] - offset, f'H = {function(node, goal_node)}') for node in self.nx.nodes]
            heuristic_labels = heuristic_labels + temp
            offset = offset + 0.2

        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        
        # Draw heuristic values with custom formatting
        for (x, y, label) in heuristic_labels:
            plt.text(x, y, label, color='red', fontweight='bold', fontsize=8, ha='center', va='center')

        plt.show()
        plt.ioff()
        
    
    def visualize_solution(self, path, goals, algorithm, function, cost, heuristic=False):
        plt.clf()
        plt.ion()
        plt.title(algorithm + ": " + path[0] + " -> " + str(goals) + "\nCusto: " + str(cost))
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}

        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(self.nx, pos, edgelist=edges, edge_color='blue', width=4)
            
        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)
        
        if heuristic:
            heuristic_labels = []
            offset = 0.2
            # Calculate heuristic values and position them slightly below the nodes
            for goal_node in goals:
                temp = [(pos[node][0], pos[node][1] - offset, f'H = {function(node, goal_node)}') for node in self.nx.nodes]
                heuristic_labels = heuristic_labels + temp
                offset = offset + 0.2
            for (x, y, label) in heuristic_labels:
                plt.text(x, y, label, color='red', fontweight='bold', fontsize=8, ha='center', va='center')
        
        plt.show()
        plt.ioff()

    def visualize_graph(self):
        plt.clf()
        plt.ion()
        plt.title("Grafo Inicial")
        pos = nx.get_node_attributes(self.nx, 'pos')
        edge_labels = {(node1, node2): f'{cost}' for (node1, node2, cost) in self.nx.edges.data('weight')}

        nx.draw(self.nx, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='black', linewidths=1, alpha=0.7)
        nx.draw_networkx_edge_labels(self.nx, pos, edge_labels=edge_labels, font_color='red', font_size=8)

        plt.show()
        plt.ioff()


if __name__ == '__main__':
    graph = Grafo()
    graph.trainHeuristic()
    print(graph.trainedHeuristic)

