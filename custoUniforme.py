import heapq

def custoUniforme (grafo, inicio, fim):
    # Inicialização
    fila_prioridade = [(0, inicio, [])]
    visitados = set()

    while fila_prioridade:
        (custo, no_atual, caminho) = heapq.heappop(fila_prioridade)

        if no_atual not in visitados:
            visitados.add(no_atual)
            caminho = caminho + [no_atual]

            if no_atual == fim:
                return (custo, caminho)

            for vizinho, custo_aresta in grafo[no_atual].items():
                if vizinho not in visitados:
                    heapq.heappush(fila_prioridade, (custo + custo_aresta, vizinho, caminho))

    return float('inf'), []
