# uc_microlog.py
# Dicionário MPC -> microinstrução (linha única para log)
mpc_to_micro = {
    0:  "mar:=pc; rd; Busca",
    1:  "pc:=pc + 1; rd; Busca",
    2:  "ir:=mbr; if n then goto 28; Busca/Identifica",
    3:  "tir:=lshift(ir + ir); if n then goto 19; Identifica",
    4:  "tir:=lshift(tir); if n then goto 11; Identifica",
    5:  "alu:=tir; if n then goto 9; Identifica",
    6:  "mar:=ir; rd; Executa",
    7:  "rd; Executa",
    8:  "ac:=mbr; goto 0; Executa",
    9:  "mar:=ir; mbr:=ac; wr; {0001 = STOD}",
    10: "wr; goto 0; Executa",
    11: "alu:=tir; if n then goto 15; Identifica",
    12: "mar:=ir; rd; {0010 = ADDD}",
    13: "rd; Executa",
    14: "ac:=mbr + ac; goto 0; Executa",
    15: "mar:=ir; rd; {0011 = SUBD}",
    16: "ac:=ac + 1; rd; Executa",
    17: "a:=inv(mbr); Executa",
    18: "ac:=ac + a; goto 0; Executa",
    19: "tir:=lshift(tir); if n then goto 25; Identifica",
    20: "alu:=tir; if n then goto 23;",
    21: "alu:=ac; if n then goto 0; {0100 = JPOS}",
    22: "pc:=band(ir,amask); goto 0;",
    23: "alu:=ac; if z then goto 22; {0101 = JZER}",
    24: "goto 0;",
    25: "alu:=tir; if n then goto 27;",
    26: "pc:=band(ir,amask); goto 0; {0110 = JUMP}",
    27: "ac:=band(ir,amask); goto 0; {0111 = LOCO}",
    28: "tir:=lshift(ir + ir); if n then goto 40;",
    29: "tir:=lshift(tir); if n then goto 35;",
    30: "alu:=tir; if n then goto 33;",
    31: "a:=ir + sp; {1000 = LODL}",
    32: "mar:=a; rd; goto 7;",
    33: "a:=ir + sp; {1001 = STOL}",
    34: "mar:=a; mbr:=ac; wr; goto 10;",
    35: "alu:=tir; if n then goto 38;",
    36: "a:=ir + sp; {1010 = ADDL}",
    37: "mar:=a; rd; goto 13;",
    38: "a:=ir + sp; {1011 = SUBL}",
    39: "mar:=a; rd; goto 16 ;",
    40: "tir:=lshift(tir); if n then goto 46;",
    41: "alu:=tir; if n then goto 44;",
    42: "alu:=ac; if n then goto 22; {1100 = JNEG}",
    43: "goto 0;",
    44: "alu:=ac; if z then goto 0; {1101 = JNZE}",
    45: "pc:=band(ir,amask); goto 0;",
    46: "tir:=lshift(tir); if n then goto 50;",
    47: "sp:=sp + (-1); {1110 = CALL}",
    48: "mar:=sp; mbr:=pc; wr;",
    49: "pc:=band(ir,amask); wr; goto 0;",
    50: "tir:=lshift(tir); if n then goto 65;",
    51: "tir:=lshift(tir); if n then goto 59;",
    52: "alu:=tir; if n then goto 56;",
    53: "mar:=ac; rd; {1111-0000 = PSHI}",
    54: "sp:=sp + (-1); rd;",
    55: "mar:=sp; wr; goto 10;",
    56: "mar:=sp; sp:=sp + 1; rd; {1111-0010 = POPI}",
    57: "rd;",
    58: "mar:=ac; wr; goto 10;",
    59: "alu:=tir; if n then goto 62;",
    60: "sp:=sp + (-1); {1111-0100 = PUSH}",
    61: "mar:=sp; mbr:=ac; wr; goto 10;",
    62: "mar:=sp; sp:=sp + 1; rd; {1111-0110 = POP}",
    63: "rd;",
    64: "ac:=mbr; goto 0;",
    65: "tir:=lshift(tir); if n then goto 73;",
    66: "alu:=tir; if n then goto 70;",
    67: "mar:=sp; sp:=sp + 1; rd; {1111-1000 = RETN}",
    68: "rd;",
    69: "pc:=mbr; goto 0;",
    70: "a:=ac; {1111-1010 = SWAP}",
    71: "ac:=sp;",
    72: "sp:=a; goto 0;",
    73: "alu:=tir; if n then goto 76;",
    74: "a:=band(ir,smask); {1111-1100 = INSP}",
    75: "sp:=sp + a; goto 0;",
    76: "a:=band(ir, smask); {1111-1110 = DESP}",
    77: "a:=inv(a);",
    78: "a:=a + 1; goto 75;",
}

def log_micro(mpc):
    """
    Escreve a microinstrução correspondente ao MPC atual.
    Não armazena nada — apenas imprime.
    """
    instr = mpc_to_micro.get(mpc, None)
    if instr is None:
        print(f"MPC {mpc}: <MPC desconhecido>")
    else:
        print(f"MPC {mpc}: {instr}")

# Exemplo de uso:
if __name__ == "__main__":
    # simula alguns MPCs vindos da UC
    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 12, 13, 14, 0, 78]
    for m in seq:
        log_micro(m)