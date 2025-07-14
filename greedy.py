def busca_gulosa(grafo, inicio, objetivo, heuristica):
    fronteira = [(heuristica(inicio), inicio)]
    explorados = set()

    while fronteira:
        _, estado_atual = fronteira.pop(0)

        if estado_atual == objetivo:
            # Se chegamos ao objetivo, retornamos o caminho
            return reconstruir_caminho(grafo, inicio, objetivo)

        if estado_atual not in explorados:
            explorados.add(estado_atual)

            # Expandir os vizinhos e adicionar à fronteira
            for vizinho in grafo[estado_atual]:
                if vizinho not in explorados:
                    custo = heuristica(vizinho)
                    fronteira.append((custo, vizinho))
            
            # Ordenar a fronteira com base na heurística
            fronteira.sort(key=lambda x: x[0])

    return None

def reconstruir_caminho(grafo, inicio, objetivo):
    # Implementação simples para reconstruir o caminho
    caminho = [objetivo]
    atual = objetivo

    while atual != inicio:
        anterior = min(grafo[atual], key=lambda x: grafo[atual][x])
        caminho.insert(0, anterior)
        atual = anterior

    return caminho