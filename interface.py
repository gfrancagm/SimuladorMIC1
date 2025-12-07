import tkinter as tk
from tkinter import ttk
import datetime
from montador import traduzir_programa
from mp import MP
from uc import UC
from datapath import Datapath
import micro as micro

class SimuladorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador MIC-1 - Visualização Expandida")
        self.root.geometry("1360x768")
        
        self.CORES = {
            "fundo_base": "#2b2b2b", "fundo_painel": "#3c3f41",
            "texto_principal": "#ffffff", "destaque_azul": "#007acc",
            "destaque_verde": "#28a745", "caixa_ativa": "#d63384",
            "caixa_inativa": "#333333", "borda_caixa": "#555555",
            "btn_bg": "#444444", "btn_fg": "#ffffff"
        }
        self.FONTE_UI = ("Segoe UI", 10)
        self.FONTE_CODE = ("Consolas", 11)
        
        self.configurar_estilos()

        self.mp = MP()
        self.dp = Datapath()
        self.uc = UC()

        self.simulacao_ativa = False
        self.delay_ms = 1000
        
        self.criar_layout_principal()
        
        self.log_sistema("Simulador iniciado.")
        self.atualizar_interface()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#252526", fieldbackground="#252526", 
                        foreground="white", bordercolor=self.CORES["borda_caixa"], 
                        rowheight=25, font=("Consolas", 10))
        style.configure("Treeview.Heading", background="#333337", foreground="white", relief="flat")
        self.root.configure(bg=self.CORES["fundo_base"])

    def criar_layout_principal(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg=self.CORES["fundo_base"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- PAINEL ESQUERDO (Editor e Controles) ---
        p_esq = tk.Frame(main_frame, bg=self.CORES["fundo_base"], width=350)
        p_esq.pack(side=tk.LEFT, fill="y", padx=(0, 20))

        # Editor
        tk.Label(p_esq, text="Editor de Código:", fg="white", bg=self.CORES["fundo_base"]).pack(anchor="w")
        self.txt_codigo = tk.Text(p_esq, height=15, width=40, font=self.FONTE_CODE, bg="#1e1e1e", fg="#d4d4d4", bd=0)
        self.txt_codigo.pack(fill="x", pady=5)
        
        tk.Button(p_esq, text="CARREGAR & RESETAR", command=self.carregar_programa, 
                  bg=self.CORES["destaque_azul"], fg="white", relief="flat").pack(fill="x", pady=5)

        self.criar_painel_controle(p_esq)
        
        # Saída (Output) REMOVIDA conforme solicitado

        # --- PAINEL DIREITO (Visualização) ---
        p_dir = tk.Frame(main_frame, bg=self.CORES["fundo_painel"])
        p_dir.pack(side=tk.RIGHT, fill="both", expand=True)

        # 1. Caminho de Dados (Labels Hardware)
        self.labels_hardware = {}
        y_pos = 50
        for comp in ["LATCH A", "LATCH B", "ALU", "AMUX", "SHIFTER", "MAR", "MBR"]:
            self.labels_hardware[comp] = self.criar_caixa_hardware(p_dir, 20, y_pos, comp)
            y_pos += 60

        # 2. Tabela de Registradores
        self.tree_regs = self.criar_tabela(p_dir, 140, 50, ["Reg", "Dec", "Bin"], 340)
        
        self.tree_regs.column("Reg", width=50, anchor="center")
        self.tree_regs.column("Dec", width=70, anchor="center")
        self.tree_regs.column("Bin", width=220, anchor="center")
        
        for reg in ["PC", "AC", "SP", "IR", "TIR", "A", "B", "C", "D", "E", "F", "MBR", "MAR"]:
            self.tree_regs.insert("", "end", values=(reg, "0", "0"*16))

        # 3. Tabela de Memória (COM SCROLLBAR)
        frame_mem = tk.Frame(p_dir, bg=self.CORES["fundo_painel"])
        frame_mem.place(x=500, y=50, width=400, height=600) 

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_mem)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        colunas_mem = ["End", "Bin", "Dec"]
        self.tree_mem = ttk.Treeview(frame_mem, columns=colunas_mem, show="headings", yscrollcommand=scrollbar.set)
        
        # Configurar colunas
        self.tree_mem.heading("End", text="End")
        self.tree_mem.column("End", width=50, anchor="center")
        self.tree_mem.heading("Bin", text="Bin")
        self.tree_mem.column("Bin", width=220, anchor="center")
        self.tree_mem.heading("Dec", text="Dec")
        self.tree_mem.column("Dec", width=80, anchor="center")
        
        self.tree_mem.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree_mem.yview)

        for i in range(256):
            self.tree_mem.insert("", "end", values=(str(i), "0"*16, "0"))

        # 4. Log
        self.txt_log = tk.Text(p_dir, bg="#1e1e1e", fg="#4af626", width=35)
        self.txt_log.place(x=920, y=50, width=330, height=550) 

    def criar_painel_controle(self, parent):
        frame = tk.Frame(parent, bg=self.CORES["fundo_painel"], pady=10)
        frame.pack(fill="x")
        btns = [("⏸", self.pausar), ("▶", self.iniciar), ("⏹", self.parar), 
                ("⟳", self.resetar), ("Passo", self.executar_passo)]
        for txt, cmd in btns:
            tk.Button(frame, text=txt, command=cmd, bg=self.CORES["btn_bg"], fg="white", width=6).pack(side="left", padx=2)
        
        tk.Label(frame, text="Ms:", bg=self.CORES["fundo_painel"], fg="white").pack(side="left", padx=2)
        self.ent_delay = tk.Entry(frame, width=5)
        self.ent_delay.insert(0, "1000")
        self.ent_delay.pack(side="left")

    def criar_caixa_hardware(self, container, x, y, texto):
        lbl = tk.Label(container, text=texto, bg=self.CORES["caixa_inativa"], 
                       fg="white", font=("Segoe UI", 9, "bold"), relief="raised")
        lbl.place(x=x, y=y, width=100, height=40)
        return lbl

    def criar_tabela(self, container, x, y, colunas, largura):
        tree = ttk.Treeview(container, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=int(largura/len(colunas)), anchor="center")
        tree.place(x=x, y=y, width=largura, height=600) 
        return tree

    def log_sistema(self, msg):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert("end", f"[{hora}] {msg}\n")
        self.txt_log.see("end")

    def carregar_programa(self):
        codigo = self.txt_codigo.get("1.0", "end-1c")
        try:
            instrucoes_lista = traduzir_programa(codigo)
            if not codigo.strip():
                self.log_sistema("Código vazio!")
                return
            with open("instrucoes.txt", "w") as f:
                for line in instrucoes_lista:
                    f.write(line + "\n")
            
            self.mp = MP()
            self.dp = Datapath()
            self.uc = UC()
            self.log_sistema("Carregado e Resetado.")
            self.atualizar_interface()
        except Exception as e:
            self.log_sistema(f"Erro: {e}")

    def atualizar_interface(self, mpc_log=None):
        # 1. Atualizar Registradores (Dec + Bin)
        mapa = {0:"PC", 1:"AC", 2:"SP", 3:"IR", 4:"TIR", 10:"A", 11:"B", 12:"C", 16:"MBR", 17:"MAR"}
        
        for item in self.tree_regs.get_children():
            reg_nome = self.tree_regs.item(item, "values")[0]
            idx_encontrado = None
            for idx, nome in mapa.items():
                if nome == reg_nome:
                    idx_encontrado = idx
                    break
            
            if idx_encontrado is not None:
                val = self.dp.registrador[idx_encontrado]
                val_dec = str(val)
                val_bin = f"{val & 0xFFFF:016b}"
                self.tree_regs.item(item, values=(reg_nome, val_dec, val_bin))

        # 2. Atualizar Memória (Endereço, Bin, Dec)
        for i, item in enumerate(self.tree_mem.get_children()):
            val = self.mp.ler(i)
            bin_str = f"{val:016b}"
            self.tree_mem.item(item, values=(str(i), bin_str, str(val)))

        # 3. Log
        if mpc_log is not None:
            micro_txt = micro.mpc_to_micro.get(mpc_log, "---")
            self.log_sistema(f"MPC {mpc_log}: {micro_txt}")
        
        # 4. Highlight Hardware (Visualização de Componentes Ativos)
        if self.uc.mir:
            mir = self.uc.mir
            # Mapeamento dos índices do MIR (conforme uc.py):
            # 0:AMUX, 1:COND, 2:ALU, 3:SH, 4:MBR, 5:MAR, 6:RD, 7:WR, 8:ENC
            
            amux_active = (mir[0] == '1')
            shifter_active = (mir[3] != '00')
            
            # MAR ativo se Escrita no MAR ou Operação de Memória
            mar_active = (mir[5] == '1' or mir[6] == '1' or mir[7] == '1')
            
            # MBR ativo se Carga via C-Bus, Leitura ou Escrita na Memória
            mbr_active = (mir[4] == '1' or mir[6] == '1' or mir[7] == '1')
            
            # ALU ativa se resultado for usado (ENC=1 ou MBR=1) ou se Flags forem testadas
            # 01 e 10 em COND (índice 1) testam N e Z
            alu_active = (mir[8] == '1' or mir[4] == '1' or mir[1] in ['01', '10'])
            
            latch_a_active = alu_active
            # Latch B só é usado em Soma (00) e AND (01)
            latch_b_active = alu_active and (mir[2] in ['00', '01']) 
            
            states = {
                "AMUX": amux_active,
                "SHIFTER": shifter_active,
                "MAR": mar_active,
                "MBR": mbr_active,
                "ALU": alu_active,
                "LATCH A": latch_a_active,
                "LATCH B": latch_b_active
            }
            
            for comp, is_active in states.items():
                if comp in self.labels_hardware:
                    color = self.CORES["caixa_ativa"] if is_active else self.CORES["caixa_inativa"]
                    self.labels_hardware[comp].config(bg=color)
        else:
             # Se não houver instrução (reset), tudo inativo
             for lbl in self.labels_hardware.values():
                 lbl.config(bg=self.CORES["caixa_inativa"])

    def executar_passo(self):
        try:
            mpc_atual = self.uc.mpc
            self.uc.executar_passo(self.dp, self.mp)
            self.atualizar_interface(mpc_log=mpc_atual)
        except Exception as e:
            self.log_sistema(f"Erro fatal: {e}")
            self.simulacao_ativa = False

    def loop_simulacao(self):
        if self.simulacao_ativa:
            self.executar_passo()
            try: d = int(self.ent_delay.get())
            except: d = 1000
            self.root.after(d, self.loop_simulacao)

    def iniciar(self):
        if not self.simulacao_ativa:
            self.simulacao_ativa = True
            self.log_sistema("▶ Simulação iniciada")
            self.loop_simulacao()

    def pausar(self):
        self.simulacao_ativa = False
        self.log_sistema("⏸ Pausado")

    def parar(self):
        self.simulacao_ativa = False
        self.resetar()
        self.log_sistema("⏹ Parado")

    def resetar(self):
        self.mp = MP()
        self.dp = Datapath()
        self.uc = UC()
        self.atualizar_interface()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorUI(root)
    root.mainloop()

