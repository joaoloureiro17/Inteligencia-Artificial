from Grafo import Grafo
from Estafetas import *
from Entregas import *
import pdb

class Manager:
    def __init__(self):
        self.graph = Grafo()
        self.estafetas = populateEstafetas('Dataset/Estafetas.csv')
        self.entregas = populateEntregas('Dataset/Entregas.csv')
        self.trained = False
        
    def destinosEntregas (self, ids):
        destinos = []
        for id in ids:
            for entrega in self.entregas:
                if id == entrega.identificador:
                    destinos.append(entrega.destino)
        return destinos
    
    def entregasEstafeta(self, ids):
        res = []
        for id in ids:
            for entrega in self.entregas:
                if id == entrega.identificador:
                    res.append(entrega)
        return res
    
    def rotaBicicleta(self, kms, peso):
        vel = 10 - (peso * 0.6)
        return ((kms * 60) / vel) / 10
    
    def rotaMota(self, kms, peso):
        vel = 35 - (peso * 0.5)
        return ((kms * 60) / vel) / 10
    
    def rotaCarro(self, kms, peso):
        vel = 50 - (peso * 0.1)
        return ((kms * 60) / vel) / 10
    
    def resolverBFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.bfs(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
        
    def resolverDFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.dfs_search_tsp(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
    
    def resolverIDDFS(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.iddfs_tsp(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos

    def resolverCustoUniforme(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        a, b, c = self.graph.custoUniforme(estafeta.Ponto_Partida, destinos)
        return a, b, c, destinos
    
    def resolverGreedy(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        if self.trained:
            a, b, c, dest= self.graph.busca_gulosa(estafeta.Ponto_Partida, destinos, self.graph.trainedHeuristicFunction)
        else:
            a, b, c, dest= self.graph.busca_gulosa(estafeta.Ponto_Partida, destinos, self.graph.heuristicFunction)
        return a, b, c, dest
    
    def resolverA_Star(self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        destinos = self.destinosEntregas(estafeta.Lista_Encomendas)
        if self.trained:
            a, b, c, dest= self.graph.a_estrela(estafeta.Ponto_Partida, destinos, self.graph.trainedHeuristicFunction)
        else:
            a, b, c, dest= self.graph.a_estrela(estafeta.Ponto_Partida, destinos, self.graph.heuristicFunction)
        return a, b, c, dest
    
    def resolver(self, estafetaID):
        alg = ""
        minCusto = 800000
        pathBFS, custoBFS, expansaoBFS, destinosBFS = self.resolverBFS(estafetaID)
        pathDFS, custoDFS, expansaoDFS, destinosDFS = self.resolverDFS(estafetaID)
        pathIDDFS, custoIDDFS, expansaoIDDFS, destinosIDDFS = self.resolverIDDFS(estafetaID)
        pathCUn, custoCUn, expansaoCUn, destinosCUn = self.resolverCustoUniforme(estafetaID)
        pathGreedy, custoGreedy, expansaoGreedy, destinosGreedy = self.resolverGreedy(estafetaID)
        patha_star, custoa_star, expansaoa_star, destinosa_star = self.resolverA_Star(estafetaID)
        if custoBFS < minCusto:
            alg = "BFS"
            minCusto = custoBFS
        if custoDFS < minCusto:
            alg = "DFS"
            minCusto = custoDFS
        if custoIDDFS < minCusto:
            alg = "IDDFS"
            minCusto = custoIDDFS
        if custoCUn < minCusto:
            alg = "Custo Uniforme"
            minCusto = custoCUn
        if custoGreedy < minCusto:
            alg = "Greedy"
            minCusto = custoGreedy
        if custoa_star < minCusto:
            alg = "A*"
            minCusto = custoa_star
        
        if alg == "BFS":
            return alg, pathBFS, custoBFS, expansaoBFS, destinosBFS
        elif alg == "DFS":
            return alg, pathDFS, custoDFS, expansaoDFS, destinosDFS
        elif alg == "IDDFS":
            return alg, pathIDDFS, custoIDDFS, expansaoIDDFS, destinosIDDFS
        elif alg == "Custo Uniforme":
            return alg, pathCUn, custoCUn, expansaoCUn, destinosCUn
        elif alg == "Greedy":
            return alg, pathGreedy, custoGreedy, expansaoGreedy, destinosGreedy
        elif alg == "A*":
            return alg, patha_star, custoa_star, expansaoa_star, destinosa_star

    
    def entregasAtraso(self, entregasIDs, entregas, caminho, tempoFunc, pesos):
        caminho_temp = []
        atraso = []
        destinos = self.destinosEntregas(entregasIDs)
        for node in caminho:
            if node in destinos:
                for entrega in entregas:
                    if entrega.destino == node:
                        if tempoFunc(self.graph.custoCaminho(caminho_temp + [node]), pesos) > int(entrega.tempo):
                            atraso.append(entrega)
            caminho_temp.append(node)
        
        return atraso
        
    def pesos(self, entregas):
        sum = 0
        for entrega in entregas:
            sum = sum + int(entrega.peso)
        return sum
        
    def train(self):
        self.graph.trainHeuristic()
        self.trained = True
    
    def estafetaInfo (self, id):
        for estafeta in self.estafetas:
            if id == estafeta.Id:
                return str(estafeta) + ", Destinos: " + str(self.destinosEntregas(estafeta.Lista_Encomendas))
        
    def concluiEstafeta (self, estafetaID):
        estafeta = self.estafetas[estafetaID-1]
        entregas = self.entregasEstafeta(estafeta.Lista_Encomendas)
        sorted_objects = sorted(entregas, key=lambda obj: obj.tempo)
        custo_otimo = self.resolver(estafetaID)
        pesos = self.pesos(sorted_objects)
        if pesos <= 5:
            tempo = self.rotaBicicleta(custo_otimo[2], pesos)
            if tempo < int(sorted_objects[-1].tempo):
                return [], custo_otimo, "Bicileta"
            else:
                return self.entregasAtraso(estafeta.Lista_Encomendas, sorted_objects, custo_otimo[1], self.rotaMota, pesos), custo_otimo, "Mota"
        elif pesos <= 20:
            #pdb.set_trace()
            tempo = self.rotaMota(custo_otimo[2], pesos)
            if tempo < int(sorted_objects[-1].tempo):
                return [], custo_otimo, "Mota"
            else:
                return self.entregasAtraso(estafeta.Lista_Encomendas, sorted_objects, custo_otimo[1], self.rotaCarro, pesos), custo_otimo, "Carro"
        elif pesos <= 100:
            return self.entregasAtraso(estafeta.Lista_Encomendas, sorted_objects, custo_otimo[1], self.rotaCarro,pesos), custo_otimo, "Carro"
        