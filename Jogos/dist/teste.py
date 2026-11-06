import tkinter as tk

def clicar():
    texto.config(text="Você clicou no botão!")

janela = tk.Tk()

texto = tk.Label(janela, text="Clique no botão")
texto.pack()

botao = tk.Button(janela, text="Clique aqui", command=clicar)
botao.pack()

janela.mainloop()
