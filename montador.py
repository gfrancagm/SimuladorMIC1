# montador.py - Montador com suporte a Labels e DADOS para MIC-1/MAC-1

class Montador:
    def __init__(self):
        # Definição dos Opcodes
        self.OPCODES = {
            # Instruções de 12 bits de endereço (Opcode 4 bits)
            'LODD': '0000', 'STOD': '0001', 'ADDD': '0010', 'SUBD': '0011',
            'JPOS': '0100', 'JZER': '0101', 'JUMP': '0110', 'LOCO': '0111',
            'LODL': '1000', 'STOL': '1001', 'ADDL': '1010', 'SUBL': '1011',
            'JNEG': '1100', 'JNZE': '1101', 'CALL': '1110',
            
            # Instruções sem operando (Opcode 16 bits completo)
            'PSHI': '1111000000000000', 'POPI': '1111001000000000',
            'PUSH': '1111010000000000', 'POP':  '1111011000000000',
            'RETN': '1111100000000000', 'SWAP': '1111101000000000',
            
            # Instruções especiais (8 bits opcode + 8 bits imediato)
            'INSP': '11111100', 'DESP': '11111110'
        }
        self.tabela_simbolos = {}

    def _limpar_linha(self, linha):
        """Remove comentários e espaços em branco extras."""
        # Remove comentários (#)
        linha = linha.split('#')[0].strip()
        return linha

    def _passo_1_mapear_labels(self, linhas):
        """
        Passo 1: Identifica labels e associa aos endereços de memória.
        Retorna uma lista de linhas 'limpas' (apenas instruções ou dados).
        """
        linhas_processadas = []
        contador_programa = 0 # Endereço de memória atual (PC)

        for linha_bruta in linhas:
            linha = self._limpar_linha(linha_bruta)
            
            # Se a linha ficou vazia após limpar (era só comentário ou enter), pula
            if not linha:
                continue

            # Verifica se há definição de label (termina com :)
            if ':' in linha:
                partes = linha.split(':')
                label = partes[0].strip()
                
                # Registra o label apontando para o endereço atual
                if label in self.tabela_simbolos:
                    raise ValueError(f"Erro: Label '{label}' redefinido.")
                self.tabela_simbolos[label] = contador_programa
                
                # O restante da linha pode conter instrução/dado ou ser vazio
                resto_linha = partes[1].strip()
                if resto_linha:
                    linhas_processadas.append(resto_linha)
                    contador_programa += 1 
                    # Se tiver conteúdo depois do label, ocupa 1 espaço na memória
            else:
                linhas_processadas.append(linha)
                contador_programa += 1

        return linhas_processadas

    def _traduzir_instrucao(self, instrucao_str):
        """
        Converte uma linha para binário.
        Pode ser: Instrução, Pseudo-instrução ou Dado Bruto (número).
        """
        partes = instrucao_str.strip().split()
        if not partes:
            return None
        
        mnemonic = partes[0].upper()
        
        # --- VERIFICAÇÃO 1: É um NÚMERO (DADO BRUTO)? ---
        # Se a linha começar com um número (ex: "5", "-10"), tratamos como dado.
        # Isso corrige o erro de "Instrução Desconhecida" em variáveis.
        eh_numero = False
        try:
            val_dado = int(mnemonic)
            eh_numero = True
        except ValueError:
            eh_numero = False
            
        if eh_numero:
            # Converte o número para 16 bits (com suporte a negativos)
            val_dado = int(mnemonic)
            return format(val_dado & 0xFFFF, '016b')

        # --- VERIFICAÇÃO 2: Instruções da CPU ---
        
        # A. Instruções Sem Operando
        if mnemonic in ['PSHI', 'POPI', 'PUSH', 'POP', 'RETN', 'SWAP']:
            if len(partes) > 1:
                raise ValueError(f"{mnemonic} não aceita operandos.")
            return self.OPCODES[mnemonic]
        
        # B. Instruções Especiais (8 bits + 8 bits)
        elif mnemonic in ['INSP', 'DESP']:
            if len(partes) != 2:
                raise ValueError(f"{mnemonic} requer 1 operando numérico.")
            try:
                val = int(partes[1])
                if not (0 <= val <= 255): raise ValueError
            except:
                raise ValueError(f"Operando de {mnemonic} deve ser numérico (0-255).")
            return self.OPCODES[mnemonic] + format(val, '08b')
            
        # C. Instruções Padrão (4 bits opcode + 12 bits endereço)
        elif mnemonic in self.OPCODES:
            if len(partes) != 2:
                raise ValueError(f"{mnemonic} requer 1 operando (Endereço ou Label).")
            
            operando = partes[1]
            endereco_final = 0
            
            # Verifica se é Label ou Número Direto
            if operando in self.tabela_simbolos:
                endereco_final = self.tabela_simbolos[operando]
            else:
                try:
                    endereco_final = int(operando)
                except ValueError:
                    raise ValueError(f"Label não definido: '{operando}'")
            
            # Validação do tamanho do endereço (12 bits = 4095)
            if not (0 <= endereco_final <= 4095):
                raise ValueError(f"Endereço fora do limite (0-4095): {endereco_final}")
                
            return self.OPCODES[mnemonic] + format(endereco_final, '012b')
            
        # D. Instrução Realmente Desconhecida
        else:
            raise ValueError(f"Instrução desconhecida: '{mnemonic}'")

    def traduzir_programa(self, codigo_fonte):
        """Método principal chamado pela Interface."""
        self.tabela_simbolos = {} # Resetar tabela
        instrucoes_binarias = []
        
        linhas = codigo_fonte.strip().split('\n')
        
        try:
            # --- PASSO 1: Criar Tabela de Símbolos ---
            linhas_instrucoes = self._passo_1_mapear_labels(linhas)
            
            # --- PASSO 2: Gerar Código de Máquina ---
            for i, linha in enumerate(linhas_instrucoes):
                binario = self._traduzir_instrucao(linha)
                if binario:
                    instrucoes_binarias.append(binario)
                    
            return instrucoes_binarias
            
        except Exception as e:
            raise e

# Wrapper para manter compatibilidade
def traduzir_programa(codigo):
    m = Montador()
    return m.traduzir_programa(codigo)
