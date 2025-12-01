from ula import ULA

pc = 0
ac = 1
sp = 2
ir = 3
tir = 4
zero = 5
plus = 6
minus = 7
amask = 8
smask = 9
reg_a = 10
reg_b = 11
reg_c = 12
reg_d = 13
reg_e = 14
reg_f = 15
mbr = 16
mar = 17

class Datapath:
    def __init__(self):
        self.registrador = [0] * 18
        self.registrador[plus] = 1
        self.registrador[minus] = -1

        self.latch_a = 0
        self.latch_b = 0

        self.ula = ULA()
        
    def executar(self):
        
        pass

        
        