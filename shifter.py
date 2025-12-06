class Shifter:
    def operar(self, sh_code, resultado):
        # Lógica padrão do Shifter MIC-1
        if sh_code == '01':
            # SRA 1 (Shift Right Arithmetic)
            resultado = resultado >> 1
        elif sh_code == '10':
            # SLL 8 (Shift Left Logical 8 bits)
            resultado = (resultado << 1) & 0xFFFF
            
        return resultado