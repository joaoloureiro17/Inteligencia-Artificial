def procura_DFS(grafo, ponto_inicial, ponto_objetivo):
    visitados = set() #armazena nós visitados
    ordem_expansao = [] #Lista para armazenar a ordem de expansão dos nós
    
    #função auxiliar para converter tuplos em listas
    def converter_tuplos_para_lista(tuplos):
        return [item[0] for item in tuplos]

    #função para calcular o custo total dos arcos num dado caminho
    def calcular_custo_arcos(caminho):
        custo = 0
        for i in range(len(caminho) - 1):
            no_atual = caminho[i]
            no_seguinte = caminho[i + 1]
            for vizinho, custo_arco in grafo[no_atual]:
                if vizinho == no_seguinte:
                    custo += custo_arco
                    break
        return custo

    #função principal da procura em profundidade 
    def DFS(atual, caminho, custo):
        visitados.add(atual)
        ordem_expansao.append(atual)
        caminho.append(atual)

        if atual == ponto_objetivo: #verifica se o nó atual é o objetivo
            return caminho, custo

        for vizinho, custo_arco in grafo[atual]:
            if vizinho not in visitados:
                novo_custo = custo + custo_arco
                resultado = DFS(vizinho, caminho.copy(), novo_custo)
                if resultado:
                    return resultado
        
        return None

    #inicia a procura DFS
    caminho, custo = DFS(ponto_inicial, [], 0)
    ordem_expansao = converter_tuplos_para_lista(ordem_expansao)

    return caminho, ordem_expansao, custo
