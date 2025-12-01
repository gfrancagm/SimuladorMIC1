# constantes
import time

AMUX = 0
COND = 1
ALU = 2
SH = 3
MBR = 4
MAR = 5
RD = 6
WR = 7
ENC = 8
C = 9
B = 10
A = 11
ADDR = 12

class UC:
    def __init__(self):
        self.memoria_controle = [None] * 512 
        self.mir = []
        self.mpc = 0
        
        with open("memoria_controle.txt", "r") as arquivo:
            for idx, linha in enumerate(arquivo):
                _, conteudo = linha.split(":")
                self.memoria_controle[idx] = conteudo.split()
            
        self.n_flag = 0
        self.z_flag = 0
            
    def run(self, datapath):                
        
        while True:
            
            self.mir = self.memoria_controle[self.mpc]
            
            endereco_bar_a = int(self.mir[A], 2)
            endereco_bar_b = int(self.mir[B], 2)
            endereco_escrita_c = int(self.mir[C], 2)
            
            op_ula = self.mir[ALU]
            
            print("-" * 40)
            print(f"MPC: {self.mpc} | MIR: {' '.join(self.mir)}")
            
            datapath.ler_registradores(endereco_bar_a, endereco_bar_b)
            
            if self.mir[AMUX] == '1':
                datapath.latch_a = datapath.registrador[16]
            
            print(f"  -> Latch A: {datapath.latch_a} | Latch B: {datapath.latch_b}")
            
            resultado_ula = datapath.executar_ula(op_ula)
            
            print(f"  -> Resultado ULA: {resultado_ula}")
            print(f"  -> Flags Geradas: N={datapath.n_flag}, Z={datapath.z_flag}")
            
            if self.mir[ENC] == '1':
                datapath.escrever_registrador(endereco_escrita_c, resultado_ula)

            condicao_desvio = self.mir[COND]
            novo_endereco = int(self.mir[ADDR], 2)
            
            if datapath.n_flag == 1 and condicao_desvio == '01':
                self.mpc = novo_endereco
                print("  [!] Desvio por N=1 realizado")
            elif datapath.z_flag == 1 and condicao_desvio == '10':
                self.mpc = novo_endereco
                print("  [!] Desvio por Z=1 realizado")
            elif condicao_desvio == '11':
                self.mpc = novo_endereco
                print(f"  -> Novo MPC: {self.mpc}")    
            else:
                self.mpc += 1
           
            print(*datapath.registrador)
           
            input("\n---> Pressione ENTER para executar o próximo ciclo...")