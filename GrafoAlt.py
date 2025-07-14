import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import math
import heapq
from collections import OrderedDict


class Grafo:
    def __init__(self, graph_dict):
        self.nx = nx.Graph()
        self.g = graph_dict

        for node, connections in graph_dict.items():
            if len(node) == 1:
                node_name, node_pos = node[0], (0, 0)
            elif len(node) == 2:
                node_name, node_pos = node
            else:
                raise ValueError("Cada entrada do dicionário deve ter 1 ou 2 elementos.")

            self.nx.add_node(node_name)
            for connection, cost in connections:
                self.nx.add_edge(node_name, connection, weight=cost)

        # Calcular layout de mola
        pos = nx.spring_layout(self.nx, seed=455)

        ###############################aqui é necessário dar então a posição para a qual se pretende calculae a heuristica
        coords = pos['Calendário']

        # Adiciona heurísticas após a criação dos nós
        for node, position in pos.items():
            x_coor, y_coor = coords
            heuristic_value = math.sqrt((position[0] - x_coor) ** 2 + (position[1] - y_coor) ** 2) * 10
            self.nx.nodes[node]['heuristic'] = heuristic_value

    def iterative_deepening_dfs(self, start, target):
        path = []  # Caminho para a solução
        order_of_expansion = []  # Ordem de expansão

        def dfs(node, depth):
            order_of_expansion.append(node)
            if node == target:
                path.append(node)
                return True
            if depth > 0:
                for child in self.g.get(node, []):
                    if dfs((child[0],), depth - 1):
                        path.append(node)
                        return True
            return False

        depth = 0
        while not dfs(start, depth):
            depth += 1

        unique_list = list(OrderedDict.fromkeys(order_of_expansion))
        return path[::-1], unique_list, depth

    def procura_DFS(self, ponto_inicial, ponto_objetivo):
        visitados = set()  # armazenar nós visitados
        ordem_expansao = []  # Lista para armazenar a ordem de expansão dos nós

        # função auxiliar para converter tuplos em listas
        def converter_tuplos_para_lista(tuplos):
            return [item[0] for item in tuplos]

        # função para calcular o custo total dos arcos num dado caminho
        def calcular_custo_arcos(caminho):
            custo = 0
            for i in range(len(caminho) - 1):
                no_atual = caminho[i]
                no_seguinte = caminho[i + 1]
                for vizinho, custo_arco in self.g[no_atual]:
                    if vizinho == no_seguinte:
                        custo += custo_arco
                        break
            return custo

        
        # função principal da procura em profundidade
        def DFS(atual, caminho, custo):
            visitados.add(atual)
            ordem_expansao.append(atual)
            caminho.append(atual)

            if atual == ponto_objetivo:  # verifica se o nó atual é o objetivo
                return caminho, custo

            for vizinho, custo_arco in self.g[atual]:
                if vizinho not in visitados:
                    novo_custo = custo + custo_arco
                    resultado = DFS((vizinho,), caminho.copy(), novo_custo)
                    if resultado:
                        return resultado

            return None

        # inicia a procura DFS
        caminho, custo = DFS(ponto_inicial, [], 0)
        ordem_expansao = converter_tuplos_para_lista(ordem_expansao)
        unique_list = list(OrderedDict.fromkeys(ordem_expansao))
        return caminho, unique_list, custo

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        lis = self.g[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in lis:
            if nodo == node2[0]:
                custoT = custo
        return custoT

    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        expansao = []
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)
        # garantir que o start node não tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and not path_found:
            nodo_atual = fila.get()
            expansao.append(nodo_atual)
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.g[nodo_atual]:
                    if (adjacente,) not in visited:
                        fila.put((adjacente,))
                        parent[(adjacente,)] = nodo_atual
                        visited.add((adjacente,))

        # Reconstruir o caminho
        path = []
        custo = 0
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # função calcula custo caminho
            custo = self.calcula_custo(path)
        return path, custo, expansao

    def custoUniforme(self, inicio, fim):
        # Inicialização
        fila_prioridade = [(0, inicio, [])]
        visitados = set()
        expansao = []

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)

                if no_atual == fim:
                    return custo, caminho, expansao

                for vizinho, custo_aresta in self.g[no_atual]:
                    if (vizinho,) not in visitados:
                        heapq.heappush(fila_prioridade, (custo + custo_aresta, (vizinho,), caminho))

        return float('inf'), [], []
    
    def a_estrela(self, inicio, fim):
        # Inicialização
        fila_prioridade = [(0 + self.nx.nodes[inicio[0]]['heuristic'], inicio, [])]
        visitados = set()
        expansao = []

        # Imprimir custos das arestas
        #for node, connections in self.g.items():
        #    for connection, cost in connections:
        #        print(f"Aresta de {node} para {connection} com custo {cost}")

        # Imprimir heurísticas
        #for node, data in self.nx.nodes(data=True):
        #    print(f'Nó: {node}, Heurística: {data["heuristic"]:.2f}')

        while fila_prioridade:
            (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)
            if no_atual not in visitados:
                visitados.add(no_atual)
                caminho = caminho + [no_atual]
                expansao.append(no_atual)

                if no_atual == fim:
                    return round(custo, 2), caminho, expansao

                for vizinho, custo_aresta in self.g[no_atual]:
                    if (vizinho,) not in visitados:
                        # Adiciona custo da aresta e heurística do próximo nó
                        custo_total_vizinho = custo - self.nx.nodes[no_atual[0]]['heuristic'] + custo_aresta + self.nx.nodes[vizinho]['heuristic']
                        heapq.heappush(fila_prioridade, (custo_total_vizinho, (vizinho,), caminho))

        return float('inf'), [], []

    #função para ver cada heuristica
    #def imprimir_heuristicas(self):
    #    for node, data in self.nx.nodes(data=True):
    #        node_name = node
    #        heuristic_value = data['heuristic']
    #        print(f'Nó: {node_name}, Heurística: {heuristic_value:.2f}')


def visualize_graph(graph):
    pos = nx.spring_layout(graph, seed=455)
    labels = nx.get_edge_attributes(graph, 'weight')

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    for node, (x, y) in pos.items():
        heuristic_value = graph.nodes[node]['heuristic']
        plt.text(x, y + 0.012, f'{heuristic_value:.2f}', color='red', fontsize=8, ha='center', va='center')

    plt.title("Grafo Visual com Heurística")
    plt.show()


if __name__ == "__main__":
    graph_dict = {
        ('Vila Nova de F',): [('Gavião', 5), ('Antas', 4), ('Calendário', 3), ('Mouquim', 4)],
        ('Antas',): [('Calendário', 4), ('Requião', 6), ('Seide', 6)],
        ('Calendário',): [('Brufe', 10)],
        ('Gavião',): [('Vale', 8), ('Mouquim', 4), ('Antas', 5)],
        ('Requião',): [('Vale', 7), ('Seide', 8)],
        ('Brufe',): [('Louro', 9), ('Outiz', 10)],
        ('Outiz',): [('Vilarinho', 11), ('Louro', 4)],
        ('Mouquim',): [],
        ('Seide',): [],
        ('Vale',): [],
        ('Louro',): [],
        ('Vilarinho',): []
    }

    graph = Grafo(graph_dict)
    
    #graph.imprimir_heuristicas()  # Adicione esta linha

    print("DFS: ", graph.procura_DFS(('Vila Nova de F',), ('Seide',)))
    print("BFS: ", graph.procura_BFS(('Vila Nova de F',), ('Seide',)))
    print("UCS: ", graph.custoUniforme(('Vila Nova de F',), ('Brufe',)))
    print("A*: ", graph.a_estrela(('Vila Nova de F',), ('Outiz',)))

    visualize_graph(graph.nx)
