class ULA:
    def operar(self, a, b, op_code):
        result = 0

        if op_code == 0: # soma
            result = a + b
        if op_code == 1: # lógica and
            result = a & b
        if op_code == 2: # A
            result = a
        if op_code == 3:
            result = ~a # inverso

        result = result & 0xFFFF
    
        z_flag = 1 if result == 0 else 0

        n_flag = 1 if (result >> 15) & 1 else 0
        
        return result, z_flag, n_flag