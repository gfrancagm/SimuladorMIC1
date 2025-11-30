from ula import ULA
from uc import UC

class datapath:
    def __init__(self):
        # indices dos registradores
        self.pc = 0
        self.ac = 1
        self.sp = 2
        self.ir = 3
        self.tir = 4
        self.zero = 5
        self.plus = 6
        self.minus = 7
        self.amask = 8
        self.smask = 9
        self.reg_a = 10
        self.reg_b = 11
        self.reg_c = 12
        self.reg_d = 13
        self.reg_e = 14
        self.reg_f = 15 

        self.registers = [0] * 16

        self.ula = ULA()
        self.uc = UC()