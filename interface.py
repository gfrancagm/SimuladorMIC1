import tkinter as tk
from tkinter import ttk

#Funcao para criar uma caixa
def criar_caixa(container, x, y, titulo):
    """
    Cria uma caixa visual na posicao X, Y escolhida.
    Retorna o widget (Label) do meio para que possamos mudar a cor depois.
    """
    # Moldura preta para dar o efeito de borda
    moldura = tk.Frame(container, bg="black", padx=2, pady=2)
    moldura.place(x=x, y=y, width=150, height=80) 

    # Area interna branca
    conteudo = tk.Frame(moldura, bg="white")
    conteudo.pack(fill="both", expand=True)

    # Titulo no topo da caixa
    lbl_titulo = tk.Label(conteudo, text=titulo, font=("Arial", 9, "bold"), bg="#ddd")
    lbl_titulo.pack(fill="x")

    # O valor que muda cor
    lbl_status = tk.Label(conteudo, text="", font=("Courier", 14), bg="white")
    lbl_status.pack(expand=True, fill="both")
    
    return lbl_status 

#muda a cor se tiver ativo
def mudar_cor_caixa(widget, ativa):
    """
    Altera a cor da caixa se a variavel 'ativa' for True.
    """
    if ativa:
        widget.config(bg="red") # Vermelho se for ativo
    else:
        widget.config(bg="white")   # Branco (Inativo)


#Manda as instrucoes da entrada para um arquivo
def salvar_arquivo(texto_validado):
    """
    Recebe o texto ja validado e escreve no arquivo.
    """
    try:
        # Cria/Sobrescreve o arquivo instrucoes.txt
        with open("instrucoes.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_validado)
    except Exception as e:
        print(f"Erro ao salvar: {e}")


#escreve na interface
def exibir_resultado(texto_validado):
    """
    Recebe o texto ja validado e exibe no Label da interface.
    """
    label_resultado.config(text=texto_validado, fg="blue")


#verificacao para ver se ta certo o formato das instrucoes
def processar_instrucoes():
    """
    Funcao principal: Le a entrada, valida o formato e chama as outras funcoes.
    """
    # "1.0" significa: Comece da linha 1, caractere 0.
    # "end-1c" significa: Vá até o final, removendo a última quebra de linha automática.
    conteudo_bruto = entrada.text.get("1.0", "end-1c") #Variavel que obtem as instrucoes.
    
    linhas = conteudo_bruto.splitlines()
    linhas_validas = []
    
    # Valida linha por linha antes de processar
    for linha in linhas:
        linha_limpa = linha.strip() 
        
        if not linha_limpa:
            continue # Pula linhas vazias
            
        partes = linha_limpa.split() 
        
        # Validacao: Precisa ter exatamente 2 partes (Instrucao + Operando)
        if len(partes) != 2:
            label_resultado.config(
                text=f"Erro de formato na linha:\n'{linha_limpa}'\n\nEsperado: INSTRUCAO OPERANDO", 
                fg="red"
            )
            return # Interrompe se houver erro
            
        linhas_validas.append(linha_limpa)

    # Se a lista de validas nao estiver vazia, prossegue
    if linhas_validas:
        texto_final = "\n".join(linhas_validas)
        
        salvar_arquivo(texto_final)    
        exibir_resultado(texto_final)
        
        #Teste para ver se a logica de mudar de cor ta certo
        # Exemplo: Se a primeira instrucao for "ADD", a caixa ACUMULADOR fica verde.
        primeira_instrucao = linhas_validas[0].split()[0].upper()
        
        if primeira_instrucao == "ADD":
            # Variavel ativa = True
            mudar_cor_caixa(caixa_acumulador, True)
        else:
            # Variavel ativa = False
            mudar_cor_caixa(caixa_acumulador, False)
            
    else:
        label_resultado.config(text="Nao ha instrucoes validas", fg="red") #texto e cor

# --- INTERFACE GRAFICA ---

root = tk.Tk()
root.title("Simulador processador")
root.geometry("1280x720") 

# Frame da ESQUERDA (Entradas)
frame_esquerda = tk.Frame(root)
frame_esquerda.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

tk.Label(frame_esquerda, text="Digite suas instrucoes (Ex: ADD 10):", font=("Arial", 10)).pack(anchor="w")

#Caixa de entrada de instrucoes
entrada = tk.Frame(frame_esquerda) # Frame auxiliar para organizar
entrada.pack()

# Criando a caixa de texto
entrada.text = tk.Text(entrada, height=15, width=40, font=("Arial", 10))
entrada.text.pack(pady=5)

# Botao chama a funcao principal de processamento
botao = tk.Button(frame_esquerda, text="Rodar instrucoes", command=processar_instrucoes, bg="#dddddd")
botao.pack(pady=5)

# Linha separadora
separador = ttk.Separator(frame_esquerda, orient='horizontal')
separador.pack(fill='x', padx=20, pady=10)

#Saida do programa (Status)
tk.Label(frame_esquerda, text="Resultado:", font=("Arial", 10, "bold")).pack()

label_resultado = tk.Label(frame_esquerda, text="...", font=("Arial", 12), justify="left")
label_resultado.pack(pady=10)

# Frame da DIREITA (Visualizacao do Processador)
frame_visualizacao = tk.Frame(root, bg="#f4f4f4", bd=2, relief="sunken")
frame_visualizacao.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

tk.Label(frame_visualizacao, text="AREA DE VISUALIZACAO", bg="#f4f4f4", font=("Arial", 12, "bold")).place(x=10, y=10)



#Exemplo de caixa.
caixa_acumulador = criar_caixa(frame_visualizacao, x=100, y=100, titulo="TEST1")

caixa_pc = criar_caixa(frame_visualizacao, x=300, y=100, titulo="TES2")
caixa_ir = criar_caixa(frame_visualizacao, x=200, y=250, titulo="REGISTRADORES")


#loop para manter a janela aberta.
root.mainloop()
