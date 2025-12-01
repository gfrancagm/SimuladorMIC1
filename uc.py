class UC:
    def __init__(self):
        self.memoria_controle = [None] * 512 
        self.mpc = 0
        
        self.carregar_arquivo("memoria_controle.txt")
        
    def carregar_arquivo(self, arquivo):
        with open(arquivo, "r") as arquivo:
            for linha in arquivo:
                i = 0
                _, conteudo = linha.split(':')
                
                tokens = conteudo.split()
                
                self.memoria_controle[i] = tokens
                
                i += 1