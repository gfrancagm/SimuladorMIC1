import tkinter as tk
from tkinter import ttk
import datetime

# --- CONFIGURAÇÕES DE ESTILO ---
CORES = {
    "fundo_base":     "#2b2b2b",  
    "fundo_painel":   "#3c3f41",  
    "texto_principal": "#ffffff", 
    "texto_secundario": "#cccccc",
    "destaque_azul":  "#007acc",  
    "destaque_verde": "#28a745",  
    "destaque_erro":  "#dc3545",  
    "console_bg":     "#1e1e1e",  
    "console_fg":     "#4af626",  
    "output_bg":      "#000000",  
    "output_fg":      "#00ffff",  
    "borda_caixa":    "#555555",  
    "caixa_inativa":  "#333333",  
    "caixa_ativa":    "#d63384",  
    "btn_control_bg": "#444444",  
    "btn_control_fg": "#ffffff",  
    "tabela_bg":      "#252526",
    "tabela_fg":      "#ffffff",
    "tabela_head":    "#333337"
}

FONTE_UI = ("Segoe UI", 10)
FONTE_TITULO = ("Segoe UI", 12, "bold")
FONTE_CODE = ("Consolas", 11)

# --- VARIÁVEIS DE ESTADO DA SIMULAÇÃO ---
SIMULACAO_ATIVA = False
DELAY_MS = 1000      # Tempo entre ciclos (1 segundo padrão)
PC_ATUAL = 0         # Contador de Programa simulado

# --- FUNCOES VISUAIS ---

#cria a caixa visual onde estao os componentes e pa
def criar_caixa(container, x, y, titulo):
    moldura = tk.Frame(container, bg=CORES["borda_caixa"], padx=1, pady=1)
    moldura.place(x=x, y=y, width=100, height=45) 
    lbl_componente = tk.Label(moldura, text=titulo, font=("Segoe UI", 10, "bold"), 
                              bg=CORES["caixa_inativa"], fg=CORES["texto_principal"])
    lbl_componente.pack(fill="both", expand=True)
    return lbl_componente 

def set_estado_componente(componente, ativo):
    """
    Define a cor do componente baseada em True (Ativo) ou False (Inativo).
    """
    if ativo:
        componente.config(bg=CORES["caixa_ativa"], fg="white")
    else:
        componente.config(bg=CORES["caixa_inativa"], fg=CORES["texto_principal"])

def criar_console_historico(container, x, y, width, height, titulo):
    """ Cria o terminal de histórico (Historico de mic1). """
    frame_console = tk.Frame(container, bg=CORES["borda_caixa"], bd=0)
    frame_console.place(x=x, y=y, width=width, height=height)

    lbl_titulo = tk.Label(frame_console, text=f" {titulo}", font=("Segoe UI", 9, "bold"), 
                          bg=CORES["borda_caixa"], fg=CORES["texto_principal"], anchor="w")
    lbl_titulo.pack(fill="x", side=tk.TOP, pady=2)

    frame_texto = tk.Frame(frame_console, bg=CORES["console_bg"])
    frame_texto.pack(fill="both", expand=True, padx=1, pady=(0,1))

    scrollbar = tk.Scrollbar(frame_texto)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    txt_console = tk.Text(frame_texto, bg=CORES["console_bg"], fg=CORES["console_fg"], 
                          font=("Consolas", 10), yscrollcommand=scrollbar.set, 
                          state="disabled", wrap="word", bd=0, padx=5, pady=5)
    txt_console.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=txt_console.yview)

    return txt_console

def criar_tela_saida(container):
    """ Cria a area de Output. """
    frame = tk.Frame(container, bg=CORES["fundo_base"])
    tk.Label(frame, text="Saída do Programa (Output):", font=FONTE_TITULO, 
             bg=CORES["fundo_base"], fg=CORES["texto_principal"]).pack(anchor="w", pady=(5, 0))
    frame_borda = tk.Frame(frame, bg=CORES["destaque_azul"], padx=1, pady=1)
    frame_borda.pack(fill="both", expand=True)
    txt_saida = tk.Text(frame_borda, height=8, width=35, font=("Consolas", 11),
                        bg=CORES["output_bg"], fg=CORES["output_fg"], 
                        state="disabled", bd=0, padx=10, pady=10)
    txt_saida.pack(fill="both", expand=True)
    return frame, txt_saida

def criar_tabela_memoria(container, x, y, width, height):
    """ Cria a tabela de Memória Principal (4 colunas). """
    frame_mem = tk.Frame(container, bg=CORES["borda_caixa"], bd=0)
    frame_mem.place(x=x, y=y, width=width, height=height)

    lbl_titulo = tk.Label(frame_mem, text=" Memória Principal (MP)", font=("Segoe UI", 9, "bold"), 
                          bg=CORES["borda_caixa"], fg=CORES["texto_principal"], anchor="w")
    lbl_titulo.pack(fill="x", side=tk.TOP, pady=2)

    frame_tree = tk.Frame(frame_mem, bg=CORES["tabela_bg"])
    frame_tree.pack(fill="both", expand=True, padx=1, pady=(0,1))

    scrollbar = tk.Scrollbar(frame_tree)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    colunas = ("end", "bin", "dec", "hex")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", 
                        yscrollcommand=scrollbar.set, selectmode="browse")
    
    tree.heading("end", text="Endereço")
    tree.heading("bin", text="Binário")
    tree.heading("dec", text="Dec")
    tree.heading("hex", text="Hex")

    tree.column("end", width=40, anchor="center")
    tree.column("bin", width=110, anchor="center")
    tree.column("dec", width=40, anchor="center")
    tree.column("hex", width=40, anchor="center")

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    for i in range(20): 
        tree.insert("", "end", values=(str(i), "0000000000000000", "0", "0000"))

    return tree

#tabela de registrado
def criar_tabela_registradores(container, x, y, width, height):
    """ Cria a tabela de Valores dos Registradores (2 Colunas). """
    frame_reg = tk.Frame(container, bg=CORES["borda_caixa"], bd=0)
    frame_reg.place(x=x, y=y, width=width, height=height)

    lbl_titulo = tk.Label(frame_reg, text=" Registradores", font=("Segoe UI", 9, "bold"), 
                          bg=CORES["borda_caixa"], fg=CORES["texto_principal"], anchor="w")
    lbl_titulo.pack(fill="x", side=tk.TOP, pady=2)

    frame_tree = tk.Frame(frame_reg, bg=CORES["tabela_bg"])
    frame_tree.pack(fill="both", expand=True, padx=1, pady=(0,1))

    # Scrollbar (opcional aqui, pois a lista é pequena, mas bom ter)
    scrollbar = tk.Scrollbar(frame_tree)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    colunas = ("reg", "val")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", 
                        yscrollcommand=scrollbar.set, selectmode="browse")
    
    tree.heading("reg", text="Registrador")
    tree.heading("val", text="Valor")

    tree.column("reg", width=80, anchor="center")
    tree.column("val", width=80, anchor="center")

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    lista_regs = ["PC", "AC", "SP", "IR", "TIR", "A", "B", "C", "D", "E", "F"]
    for reg in lista_regs:
        tree.insert("", "end", values=(reg, "0"))

    return tree

# --- FUNÇÕES LÓGICAS E DE CONTROLE ---

def atualizar_registrador(nome_reg, novo_valor):
    """
    Atualiza programaticamente o valor de um registrador na tabela.
    """
    if 'tabela_registradores' in globals():
        # Procura na treeview a linha que tem o registrador certo
        for item_id in tabela_registradores.get_children():
            vals = tabela_registradores.item(item_id, "values")
            if vals[0] == nome_reg:
                # Atualiza mantendo o nome e trocando o valor
                tabela_registradores.item(item_id, values=(nome_reg, str(novo_valor)))
                return

def atualizar_memoria(endereco, novo_valor_dec):
    """
    Atualiza uma linha da memória baseada no endereço.
    Calcula automaticamente Binário e Hexadecimal.
    """
    if 'tabela_memoria' in globals():
        try:
            end_alvo = int(endereco) # Garante que o endereço é inteiro
            val_int = int(novo_valor_dec) # Garante que o valor é inteiro
            
            # Formatações automáticas
            val_bin = f"{val_int:016b}" # Converte para binário de 16 bits
            val_hex = f"{val_int:04X}"  # Converte para Hex maiúsculo de 4 dígitos
            
            # Procura a linha correta na tabela
            for item_id in tabela_memoria.get_children():
                valores_linha = tabela_memoria.item(item_id, "values")
                
                # A coluna 0 é o endereço. Se bater com o alvo, atualiza.
                if int(valores_linha[0]) == end_alvo:
                    tabela_memoria.item(item_id, values=(str(end_alvo), val_bin, str(val_int), val_hex))
                    return # Para o loop após encontrar
                    
        except ValueError:
            log_mic(f"Erro ao atualizar memória: valor inválido.")

def log_mic(mensagem):
    if 'console_mic' in globals():
        console_mic.config(state="normal")
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        console_mic.insert("end", f"[{hora}] {mensagem}\n")
        console_mic.see("end")
        console_mic.config(state="disabled")

def escrever_saida(texto):
    if 'txt_saida_programa' in globals():
        txt_saida_programa.config(state="normal")
        txt_saida_programa.insert("end", f"{texto}\n")
        txt_saida_programa.see("end")
        txt_saida_programa.config(state="disabled")

# --- MOTOR DA SIMULAÇÃO ---

def executar_ciclo_unico():
    """ Executa apenas UM passo do processador (Busca/Decodifica/Executa) """
    global PC_ATUAL
    
    # 1. Simula incremento do PC
    PC_ATUAL += 1
    atualizar_registrador("PC", str(PC_ATUAL))
    
    # 2. Exemplo visual: Pisca a ALU rapidamente para indicar processamento
    # Aqui usamos o set_estado_componente dinamicamente
    set_estado_componente(caixa_alu, True)
    root.after(200, lambda: set_estado_componente(caixa_alu, False))
    
    log_mic(f">> Ciclo {PC_ATUAL} executado.")
    # Exemplo: Atualizar memória no ciclo 5 só para teste visual
    if PC_ATUAL == 5:
        atualizar_memoria(PC_ATUAL, 999)

def loop_simulacao():
    """ Função recursiva que chama a si mesma enquanto estiver ATIVA """
    if SIMULACAO_ATIVA:
        executar_ciclo_unico()
        # Agenda a próxima execução baseada no DELAY_MS
        root.after(DELAY_MS, loop_simulacao)

def btn_play():
    global SIMULACAO_ATIVA
    if not SIMULACAO_ATIVA:
        SIMULACAO_ATIVA = True
        log_mic("▶ Play: Simulação iniciada.")
        loop_simulacao() # Dá a partida no motor

def btn_pause():
    global SIMULACAO_ATIVA
    SIMULACAO_ATIVA = False
    log_mic("⏸ Pause: Simulação parada.")

def btn_stop():
    global SIMULACAO_ATIVA, PC_ATUAL
    SIMULACAO_ATIVA = False
    PC_ATUAL = 0
    atualizar_registrador("PC", "0")
    log_mic("⏹ Stop: Resetando PC.")

def btn_set_delay(entry_widget):
    global DELAY_MS
    try:
        valor = int(entry_widget.get())
        DELAY_MS = valor
        log_mic(f"Delay alterado para {DELAY_MS}ms")
    except:
        log_mic("Erro: Valor de delay inválido")

def criar_painel_controle(container):
    frame = tk.Frame(container, bg=CORES["fundo_painel"], bd=1, relief="solid", padx=10, pady=10)
    
    tk.Label(frame, text="Controles da Simulação", font=("Segoe UI", 11), 
             bg=CORES["fundo_painel"], fg="white").pack(pady=(0,5), anchor="center")
    
    f_media = tk.Frame(frame, bg=CORES["fundo_painel"])
    f_media.pack(pady=5)
    estilo_btn = {"font": ("Segoe UI", 12), "width": 4, "bg": CORES["btn_control_bg"], 
                  "fg": CORES["btn_control_fg"], "relief": "raised", "bd": 1}

    # Botões Atualizados com Funções Reais
    tk.Button(f_media, text="⏸", command=btn_pause, **estilo_btn).pack(side="left", padx=2)
    tk.Button(f_media, text="▶",  command=btn_play,  **estilo_btn).pack(side="left", padx=2)
    tk.Button(f_media, text="⏹",  command=btn_stop,  **estilo_btn).pack(side="left", padx=2)
    tk.Button(f_media, text="⟳",  command=lambda: [log_mic("RESET"), escrever_saida("--- RESET ---")], **estilo_btn).pack(side="left", padx=2)

    f_delay = tk.Frame(frame, bg=CORES["fundo_painel"])
    f_delay.pack(pady=5)
    tk.Label(f_delay, text="Delay (ms): ", bg=CORES["fundo_painel"], fg="white").pack(side="left")
    
    entry_delay = tk.Entry(f_delay, width=5)
    entry_delay.insert(0, "1000") # Valor padrao
    entry_delay.pack(side="left", padx=2)
    
    tk.Button(f_delay, text="Set", bg=CORES["btn_control_bg"], fg="white", width=4,
              command=lambda: btn_set_delay(entry_delay)).pack(side="left", padx=2)

    
    # Botão para avançar um ciclo manualmente
    tk.Button(frame, text="Passar um ciclo", bg=CORES["btn_control_bg"], fg="white", width=30,
              command=executar_ciclo_unico).pack(pady=(2, 0))
    return frame

# --- PROCESSAMENTO ---

def salvar_arquivo(texto_validado):
    try:
        with open("instrucoes.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_validado)
        log_mic("Arquivo salvo.")
    except Exception as e:
        log_mic(f"Erro disco: {e}")

def processar_instrucoes():
    txt_saida_programa.config(state="normal")
    txt_saida_programa.delete("1.0", "end")
    txt_saida_programa.config(state="disabled")

    conteudo = entrada.text.get("1.0", "end-1c") 
    linhas = conteudo.splitlines()
    linhas_validas = []
    
    for linha in linhas:
        l = linha.strip() 
        if not l: continue
        parts = l.split() 
        if len(parts) < 1: # Validacao simplificada
            continue
        linhas_validas.append(l)

    if linhas_validas:
        salvar_arquivo("\n".join(linhas_validas))
        instrucao = linhas_validas[0].split()[0].upper()
        
        escrever_saida(f"Processando instrução inicial: {instrucao}")
        
        # --- LÓGICA DE DESTAQUE BOOLEANA ---
        
        # Define condições booleanas
        is_alu_ativa = (instrucao in ["ADD", "SUB", "MUL", "DIV"])
        is_mar_ativo = (instrucao in ["STR", "LDA"])
        is_shifter_ativo = (instrucao in ["SHR", "SHL"])
        
        # Aplica aos componentes usando a nova função
        set_estado_componente(caixa_alu, is_alu_ativa)
        set_estado_componente(caixa_mar, is_mar_ativo)
        set_estado_componente(caixa_shifter, is_shifter_ativo)
        
        # Garante que os outros desliguem se não forem usados
        if not is_alu_ativa: set_estado_componente(caixa_alu, False)
        if not is_mar_ativo: set_estado_componente(caixa_mar, False)
        if not is_shifter_ativo: set_estado_componente(caixa_shifter, False)

        # Atualiza PC como exemplo
        atualizar_registrador("PC", "1") 
    else:
        log_mic("Entrada vazia.")

# --- UI MAIN ---

root = tk.Tk()
root.title("Simulador de Processador - Completo?")
root.geometry("1360x768") 
root.configure(bg=CORES["fundo_base"])

# Estilos Treeview
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=CORES["tabela_bg"], fieldbackground=CORES["tabela_bg"], 
                foreground=CORES["tabela_fg"], bordercolor=CORES["borda_caixa"], lightcolor=CORES["borda_caixa"], darkcolor=CORES["borda_caixa"])
style.configure("Treeview.Heading", background=CORES["tabela_head"], foreground="white", relief="flat", font=("Segoe UI", 9, "bold"))
style.map("Treeview", background=[('selected', CORES["destaque_azul"])])

# HEADER
tk.Label(root, text="SIMULADOR DE CPU - v0.5aaaaaaaaaaaaa nao aguento mais", font=("Segoe UI", 14, "bold"), 
         bg=CORES["fundo_painel"], fg=CORES["destaque_azul"], height=2).pack(fill="x")

frame_main = tk.Frame(root, bg=CORES["fundo_base"])
frame_main.pack(fill="both", expand=True, padx=20, pady=10)

# --- ESQUERDA (Editor e Controles) ---
frame_esquerda = tk.Frame(frame_main, bg=CORES["fundo_base"], width=320)
frame_esquerda.pack(side=tk.LEFT, fill="y", padx=(0, 20))

tk.Label(frame_esquerda, text="Editor de Código:", font=FONTE_TITULO, bg=CORES["fundo_base"], fg="white").pack(anchor="w")
f_input = tk.Frame(frame_esquerda, bg=CORES["destaque_azul"], padx=1, pady=1)
f_input.pack(fill="x")
entrada = tk.Frame(f_input, bg=CORES["fundo_base"])
entrada.pack(fill="x")
entrada.text = tk.Text(entrada, height=10, width=35, font=FONTE_CODE, bg="#1e1e1e", fg="#d4d4d4", bd=0, padx=5, pady=5)
entrada.text.pack(fill="x")

tk.Button(frame_esquerda, text="CARREGAR", command=processar_instrucoes, 
          bg=CORES["destaque_azul"], fg="white", relief="flat", pady=4).pack(fill="x", pady=5)

painel = criar_painel_controle(frame_esquerda)
painel.pack(fill="x", pady=10)

frame_out, txt_saida_programa = criar_tela_saida(frame_esquerda)
frame_out.pack(fill="both", expand=True, pady=(5,0))

# --- DIREITA (Painel Visual) ---
frame_vis = tk.Frame(frame_main, bg=CORES["fundo_painel"], bd=1, relief="flat")
frame_vis.pack(side=tk.RIGHT, fill="both", expand=True)

tk.Label(frame_vis, text="Datapath, Valores e Memória", font=FONTE_TITULO, bg=CORES["fundo_painel"], fg="#ccc").place(x=20, y=10)

# COLUNA 1: Caminho de Dados (Visual)
x_c1, y_start, gap = 20, 50, 55 
tk.Label(frame_vis, text="Datapath", font=("Segoe UI", 9), bg=CORES["fundo_painel"], fg="#888").place(x=x_c1, y=y_start-20)

caixa_latch_a = criar_caixa(frame_vis, x_c1, y_start, "LATCH A")
caixa_latch_b = criar_caixa(frame_vis, x_c1, y_start + gap, "LATCH B")
caixa_alu     = criar_caixa(frame_vis, x_c1, y_start + gap*2, "ALU")
caixa_amux    = criar_caixa(frame_vis, x_c1, y_start + gap*3, "AMUX")
caixa_shifter = criar_caixa(frame_vis, x_c1, y_start + gap*4, "SHIFTER")
caixa_mar     = criar_caixa(frame_vis, x_c1, y_start + gap*5, "MAR")
caixa_mbr     = criar_caixa(frame_vis, x_c1, y_start + gap*6, "MBR")

# COLUNA 2: Valores dos Registradores (TABELA)
x_c2 = 140
tabela_registradores = criar_tabela_registradores(frame_vis, x=x_c2, y=y_start, width=190, height=550)

# COLUNA 3: Memoria Principal (Deslocada para a direita)
x_c3 = 350
tabela_memoria = criar_tabela_memoria(frame_vis, x=x_c3, y=y_start, width=340, height=550)

# COLUNA 4: Historico
x_c4 = 710
console_mic = criar_console_historico(frame_vis, x=x_c4, y=y_start, width=280, height=550, titulo="Historico")

log_mic("Registradores inicializados.")
log_mic("Interface pronta.")
atualizar_registrador("IR", "1")
atualizar_memoria(5, 255)
set_estado_componente(caixa_amux, True)

root.mainloop()
