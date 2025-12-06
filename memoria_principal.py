class MP:
    def __init__(self):
        self.memoria = 1024 * [0]
        
        #INSERÇÃO DE PROGRAMA A FORÇA
        self.memoria[0] = "0000000000000001"
        self.memoria[1] = 10
        
    def ler(self, endereco):
        endereco = endereco & 0x0FFF
        
        valor = self.memoria[endereco]
        return valor
        
        