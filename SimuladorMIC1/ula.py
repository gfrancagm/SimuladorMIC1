class ULA:
    def operar(self, a, b, op_code):
        result = 0
        
        if isinstance(a, str):
            a = int(a)
            
        if isinstance(b, str):
            b = int(b)

        if op_code == "00": 
            result = a + b
        elif op_code == "01": 
            result = a & b
        elif op_code == "10":
            result = a
        elif op_code == "11":
            result = ~a 

        result = result & 0xFFFF # força o resultado a ser um número de 16 bits

        if result == 0:
            z_flag = 1
        else: 
            z_flag = 0

        if (result & 0x8000) != 0: # pega o MSB do resultado
            n_flag = 1
        else: 
            n_flag = 0

        return result, n_flag, z_flag