class ULA:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.n_flag = 0 
        self.z_flag = 0
        self.result = 0

    def sum(self, a, b):
        self.result = a + b
    
    def logic_and(self, a, b):
        self.result = a + b
    
    def a(self, a):
        self.result = a


    def not_a(self, a):
        self.result = ~a