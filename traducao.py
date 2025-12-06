# tradutor.py - Tradutor de instruções assembly para binário

# Dicionário com os opcodes em binário para cada mnemônico
OPCODES = {
    'LODD': '0000',
    'STOD': '0001', 
    'ADDD': '0010',
    'SUBD': '0011',
    'JPOS': '0100',
    'JZER': '0101',
    'JUMP': '0110',
    'LOCO': '0111',
    'LODL': '1000',
    'STOL': '1001',
    'ADDL': '1010',
    'SUBL': '1011',
    'JNEG': '1100',
    'JNZE': '1101',
    'CALL': '1110',
    'PSHI': '1111000000000000',
    'POPI': '1111001000000000',
    'PUSH': '1111010000000000',
    'POP':  '1111011000000000',
    'RETN': '1111100000000000',
    'SWAP': '1111101000000000',
    'INSP': '11111100',
    'DESP': '11111110'
}

def traduzir_instrucao(instrucao_str):
    """
    Converte uma instrução assembly em string para binário
    seguindo o formato da tabela.
    
    Args:
        instrucao_str (str): Instrução no formato "MNEMONICO operando"
        
    Returns:
        str: Instrução em binário de 16 bits
    """
    # Divide a instrução em partes
    partes = instrucao_str.strip().split()
    
    if not partes:
        raise ValueError("Instrução vazia")
    
    mnemonic = partes[0].upper()
    
    # Instruções sem operando (com opcode completo)
    if mnemonic in ['PSHI', 'POPI', 'PUSH', 'POP', 'RETN', 'SWAP']:
        if len(partes) > 1:
            raise ValueError(f"{mnemonic} não recebe operando")
        return OPCODES[mnemonic]
    
    # Instruções INSP e DESP (8 bits de opcode + 8 bits Y)
    elif mnemonic in ['INSP', 'DESP']:
        if len(partes) != 2:
            raise ValueError(f"{mnemonic} requer um operando Y")
        
        y = int(partes[1])
        if y < 0 or y > 255:
            raise ValueError(f"Operando Y deve estar entre 0 e 255: {y}")
        
        # Converte Y para 8 bits binário
        y_bin = format(y, '08b')
        return OPCODES[mnemonic] + y_bin
    
    # Instruções com operando X de 12 bits
    else:
        if len(partes) != 2:
            raise ValueError(f"{mnemonic} requer um operando X")
        
        x = int(partes[1])
        if x < 0 or x > 4095:
            raise ValueError(f"Operando X deve estar entre 0 e 4095: {x}")
        
        # Converte X para 12 bits binário
        x_bin = format(x, '012b')
        return OPCODES[mnemonic] + x_bin

def traduzir_programa(programa_str):
    """
    Converte um programa completo (múltiplas instruções) para binário.
    
    Args:
        programa_str (str): Programa com uma instrução por linha
        
    Returns:
        list: Lista de instruções em binário (16 bits cada)
    """
    instrucoes_bin = []
    linhas = programa_str.strip().split('\n')
    
    for numero_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        
        # Ignora linhas vazias e comentários
        if not linha or linha.startswith('#'):
            continue
            
        try:
            binario = traduzir_instrucao(linha)
            instrucoes_bin.append(binario)
        except Exception as e:
            raise ValueError(f"Erro na linha {numero_linha}: {linha}\n{str(e)}")
    
    return instrucoes_bin
