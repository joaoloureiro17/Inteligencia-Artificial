from manager import Manager
import pdb
class Menu:
    def __init__(self):
        self.manager = Manager()
        self.heuristicF = self.manager.graph.heuristicFunction

    def __adicionarHeuristica (self):
        choice = input("Escolha o nó para a heurística se basear: ")
        ch_list = [item.strip() for item in choice.split(',')]
        for element in ch_list:
            if element not in self.manager.graph.nx.nodes:
                print("Um dos nós que escolheu não existe...")
                return
        self.manager.graph.visualize_graph_with_heuristic(ch_list, self.heuristicF)

    def entregasStr(self, entregas):
        res = ""
        for entrega in entregas:
            res = res + str(entrega) + "; "
        return res

    def __menuEstafeta (self, estafeta):
        print("Menu do " + self.manager.estafetaInfo(estafeta.Id))
        print("1. Aplicar BFS")
        print("2. Aplicar DFS")
        print("3. Aplicar IDDFS")
        print("4. Aplicar Custo Uniforme")
        print("5. Aplicar Greedy")
        print("6. Aplicar A*")
        print("7. Resolver Estafeta")
        print("8. Sair")
        choice = input("Opção (1-8): ")
        
        if choice == '1':
            caminho, custo, expansao, destinos= self.manager.resolverBFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "BFS", self.heuristicF, custo)
        elif choice == '2':
            caminho, custo, expansao, destinos= self.manager.resolverDFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "DFS", self.heuristicF, custo)
        elif choice == '3':
            caminho, custo, expansao, destinos= self.manager.resolverIDDFS(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "IDDFS", self.heuristicF, custo)
        elif choice == '4':
            caminho, custo, expansao, destinos= self.manager.resolverCustoUniforme(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "Custo Uniforme", self.heuristicF, custo)
        elif choice == '5':
            caminho, custo, expansao, destinos= self.manager.resolverGreedy(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "Greedy", self.heuristicF, custo, True)
        elif choice == '6':
            caminho, custo, expansao, destinos= self.manager.resolverA_Star(estafeta.Id)
            print (f"Caminho: {caminho}; Custo: {custo}; Expansão: {expansao}")
            self.manager.graph.visualize_solution(caminho, destinos, "A*", self.heuristicF, custo, True)
        elif choice == '7':
            res = self.manager.concluiEstafeta(estafeta.Id)
            print("Encomendas enteregues via: " + res[2])
            if res[0] == []:
                print("Tudo entregue a tempo")
                self.manager.graph.visualize_solution(res[1][1], res[1][4], res[1][0], self.heuristicF, res[1][2], True)
            else:
                print("Entregas em atraso " + self.entregasStr(res[0]))
                self.manager.graph.visualize_solution(res[1][1], res[1][4], res[1][0], self.heuristicF, res[1][2], True)
                print (f"Caminho: {res[1][1]}; Custo: {res[1][2]}; Expansão: {res[1][3]}")
        elif choice == '8':
            return
        else:
            print("Escholha entre 1 a 8.")

    def __escolherEstafeta(self):
        i = 0
        while(i < len(self.manager.estafetas)):
            print(self.manager.estafetaInfo(i+1))
            i = i + 1
        choice = input(f"Escholha o estafeta (1 - {i}): ")
        estafeta = self.manager.estafetas[int(choice) - 1]
        self.__menuEstafeta(estafeta)
        
        
        
    def iniciar(self):
        while True:
            print("1. Mostrar Grafo")
            print("2. Treinar Heurística")
            print("3. Adicionar Heurística")
            print("4. Escolher estafeta para correr o programa")
            print("5. Exit")

            choice = input("Insira a sua escolha (1-5): ")

            if choice == '1':
                self.manager.graph.visualize_graph()
            elif choice == '2':
                self.manager.train()
                self.heuristicF = self.manager.graph.trainedHeuristicFunction
                print("Heurística treinada")
            elif choice == '3':
                self.__adicionarHeuristica()
            elif choice == '4':
                self.__escolherEstafeta()
            elif choice == '5':
                print("A sair...")
                break
            else:
                print("Escolha entre 1 a 5.")


if __name__ == "__main__":
    visualizer = Menu()
    visualizer.iniciar()
