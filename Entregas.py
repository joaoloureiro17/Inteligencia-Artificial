import csv

class Entrega:
    def __init__(self, identificador, destino, peso, volume, tempo):
        self.identificador = identificador
        self.destino = destino
        self.peso = peso
        self.volume = volume
        self.tempo = tempo

    def __str__(self):
        return f"Identificador: {self.identificador}, Destino: {self.destino}, Peso: {self.peso}, Volume: {self.volume}, Tempo: {self.tempo}"
    

def populateEntregas (path):
    entregas = []
    with open(path, 'r', encoding = 'utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv, delimiter=';')
        next(leitor_csv)
        for linha in leitor_csv:
            identificador, destino, peso, volume, tempo = linha
            entrega = Entrega(identificador, destino, peso, volume, tempo)
            entregas.append(entrega)
    return entregas
