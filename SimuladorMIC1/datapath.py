from ula import ULA
from shifter import Shifter

PC = 0
AC = 1
SP = 2
IR = 3
TIR = 4
ZERO = 5
PLUS = 6
MINUS = 7
AMASK = 8
SMASK = 9
REG_A = 10
REG_B = 11
REG_C = 12
REG_D = 13
REG_E = 14
REG_F = 15
MBR = 16
MAR = 17

class Datapath:
    def __init__(self):
        self.registrador = [0] * 18
        self.registrador[PLUS] = 1
        self.registrador[MINUS] = -1
        self.registrador[AMASK] = 0x0FFF
        self.registrador[SMASK] = 0x00FF

        self.latch_a = 0
        self.latch_b = 0

        self.n_flag = 0
        self.z_flag = 0

        self.ula = ULA()
        self.shifter = Shifter()
        
    def ler_registradores(self, endereco_a, endereco_b):
        self.latch_a = self.registrador[endereco_a]
        self.latch_b = self.registrador[endereco_b]
        
    def escrever_registrador(self, endereco_c, valor):
        self.registrador[endereco_c] = valor

    def executar_ula(self, op_code):
        resultado, n, z = self.ula.operar(self.latch_a, self.latch_b, op_code)
        
        self.n_flag = n
        self.z_flag = z
        
        return resultado
    
    def executar_shifter(self, op_code, resultado_ula):
        resultado = self.shifter.operar(op_code, resultado_ula)
        
        return resultado
    
    def imprimir(self):
        print("\nREGISTRADORES DA VIA DE DADOS:")
        for idx, elem in enumerate(self.registrador):
            print(f"[{idx}] = {elem}")