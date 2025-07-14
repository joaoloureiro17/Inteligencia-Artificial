import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from collections import OrderedDict
def iterative_deepening_dfs(graph, start, target):
    visited = set()  # Conjunto para rastrear nós visitados
    path = []  # Caminho para a solução
    order_of_expansion = []  # Ordem de expansão

    def dfs(node, depth):
        if node in visited:
            return False
        visited.add(node)
        order_of_expansion.append(node)
        if node == target:
            path.append(node)
            return True
        if depth > 0:
            for child in graph.get(node, []):
                if dfs(child, depth - 1):
                    path.append(node)
                    return True
        return False

    depth = 0
    while not dfs(start, depth):
        visited.clear()  # Limpar nós visitados para a próxima iteração
        depth += 1

    unique_list = list(OrderedDict.fromkeys(order_of_expansion))
    return path[::-1], unique_list, depth
graph = {
    ('A',): [('B',), ('C',)],
    ('B',): [('D',), ('E',)],
    ('C',): [('F',)],
    ('D',): [('G',), ('H',)],
    ('E',): [('H',), ('I',)],
    ('F',): [('J',)],
    ('G',): [('K',), ('L',)],
    ('H',): [('M',)],
    ('I',): [],
    ('J',): [('N',), ('O',)],
    ('K',): [],
    ('L',): [],
    ('M',): [],
    ('N',): [],
    ('O',): []
}

solution, order_of_expansion, depth = iterative_deepening_dfs(graph, ('A',), ('M',))
print(solution, order_of_expansion, depth)