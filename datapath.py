import ula

class datapath:
    def __init__(self):
        # Registradores
        self.mar    = 0
        self.mbr    = 0
        self.pc     = 0
        self.sp     = 0
        self.ac     = 0
        self.ir     = 0
        self.tir    = 0
        self.ZERO   = 0
        self.PLUS   = 1
        self.MINUS  = -1
        self.amask  = 0
        self.smask  = 0
        self.n_flag = 0
        self.z_flag = 0

        self.ula = ula
