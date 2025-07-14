import csv
from Entregas import *

class Estafetas:
    def __init__(self, Id, Ponto_Partida, Lista_Encomendas):
        self.Id = Id
        self.Ponto_Partida = Ponto_Partida 
        self.Lista_Encomendas =Lista_Encomendas
        
    def __str__(self):
        return f"Estafeta: {self.Id}, Ponto de Partida: {self.Ponto_Partida}, Encomendas Atribuidas: {len(self.Lista_Encomendas)}"
    
def populateEstafetas(caminho_do_csv):
    estafetas = []
    with open(caminho_do_csv, 'r', encoding='utf-8') as arquivo_csv: #o encoding= 'utf-8' é para conseguir imprimir os caracteres com acento
        leitor_csv = csv.reader(arquivo_csv, delimiter=';')

        next(leitor_csv, None)
        for linha in leitor_csv:
            Id = int(linha[0])
            Ponto_Partida = linha[1]
            Lista_Encomendas = linha[2].split(',')  #na lista das encomendas, estas estão separadas por vírgulas

            estafeta = Estafetas(Id, Ponto_Partida, Lista_Encomendas)
            estafetas.append(estafeta)
    return estafetas
