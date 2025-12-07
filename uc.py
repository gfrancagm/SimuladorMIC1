import micro as micro

# constantes
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
        self.memoria_controle = [0] * 512 
        self.mir = []
        self.mpc = 0
        
        with open("memoria_controle.txt", "r") as arquivo:
            for idx, linha in enumerate(arquivo):
                _, conteudo = linha.split(":")
                self.memoria_controle[idx] = conteudo.split()
            
        self.n_flag = 0
        self.z_flag = 0        
    
    def executar_passo(self, datapath, mp):          
        micro.log_micro(self.mpc)
        self.mir = self.memoria_controle[self.mpc] 
        
        # --- Decodificação dos campos do MIR ---
        endereco_escrita_c = int(self.mir[C], 2)
        endereco_bar_b = int(self.mir[B], 2)
        endereco_bar_a = int(self.mir[A], 2)
        op_ula = self.mir[ALU]
        op_shift = self.mir[SH]
        
        datapath.ler_registradores(endereco_bar_a, endereco_bar_b)
        
        if self.mir[MAR] == '1':
            datapath.registrador[17] = datapath.latch_b 
                
        if self.mir[RD] == '1':  
            valor = mp.ler(datapath.registrador[17])
            datapath.registrador[16] = valor 
        
        if self.mir[AMUX] == '1':
            datapath.latch_a = datapath.registrador[16] 
        
        resultado_ula = datapath.executar_ula(op_ula)
        
        if self.mir[SH] != '00':    
            resultado_ula = datapath.executar_shifter(op_shift, resultado_ula)
            
        if self.mir[MBR] == '1':
            datapath.registrador[16] = resultado_ula    
        
        if self.mir[ENC] == '1':
            datapath.escrever_registrador(endereco_escrita_c, resultado_ula)

        if self.mir[WR] == '1':
            valor_mbr = datapath.registrador[16]
            endereco_mar = datapath.registrador[17]
            mp.escrever(endereco_mar, valor_mbr)

        condicao_desvio = self.mir[COND]
        novo_endereco = int(self.mir[ADDR], 2)
        
        # Lógica de Pulo
        if datapath.n_flag == 1 and condicao_desvio == '01':
            self.mpc = novo_endereco
        elif datapath.z_flag == 1 and condicao_desvio == '10':
            self.mpc = novo_endereco
        elif condicao_desvio == '11':
            self.mpc = novo_endereco
        else:
            self.mpc += 1
            