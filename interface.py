import tkinter as tk
from tkinter import ttk

def exibir_na_tela():
    """
    Pega o texto da caixa Multilinha (Text) e exibe no Label.
    """
    # "1.0" significa: Comece da linha 1, caractere 0.
    # "end-1c" significa: Vá até o final, removendo a última quebra de linha automática.

    #Variavel que obtem o conteudo da entrada.
    conteudo = entrada.text.get("1.0", "end-1c")
    print(f"{conteudo}")
    if conteudo.strip(): #verifica se esta vazio
        label_resultado.config(text=conteudo, fg="blue")
    else:
        label_resultado.config(text="Nao ha instrucoes", fg="red") #texto e cor

root = tk.Tk()
root.title("Simulador processador")
root.geometry("1280x720") 

#Interface para entrada de instrucoes
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=5, padx=(0, 900))

tk.Label(frame_entrada, text="Digite suas instrucoes:", font=("Arial", 10)).pack(anchor="w")

#Caixa de entrada de instrucoes
entrada = tk.Frame(frame_entrada) # Frame auxiliar para organizar
entrada.pack()

# Criando a caixa de texto
entrada.text = tk.Text(entrada, height=15, width=40, font=("Arial", 10))
entrada.text.pack(pady=5)

botao = tk.Button(frame_entrada, text="Rodar instrucoes", command=exibir_na_tela, bg="#dddddd")
botao.pack(pady=5)

# Linha separadora
separador = ttk.Separator(root, orient='horizontal')
separador.pack(fill='x', padx=20, pady=10)

#Saida do programa
frame_saida = tk.Frame(root)
frame_saida.pack(pady=10, padx=(0, 900))

tk.Label(frame_saida, text="Resultado:", font=("Arial", 10, "bold")).pack()


label_resultado = tk.Label(frame_saida, text="...", font=("Arial", 12), justify="left")
label_resultado.pack(pady=10)

#loop para manter a janela aberta.
root.mainloop()