class MP:
    def __init__(self):
        self.memoria = 1024 * [0]
        self.carregar_programa()
        
    def carregar_programa(self):
        with open("instrucoes.txt", "r") as arquivo:
            for idx, linha in enumerate(arquivo):
                self.memoria[idx] = int(linha.strip(), 2)
                        
    def ler(self, endereco):
        endereco = endereco & 0x0FFF
        
        valor = self.memoria[endereco]
        return valor
    
    def escrever(self, endereco, valor):
        endereco = endereco & 0x0FFF
        
        self.memoria[endereco] = valor
        print(f"[MEM] Escrita no endereço {endereco}: {valor}")