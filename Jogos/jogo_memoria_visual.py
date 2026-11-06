
import tkinter as tk
import random

# Configurações
ANIMAIS = [
    "🐶", "🐱", "🐵", "🦁", "🐯", "🐸",
    "🐼", "🐨", "🐷", "🐮", "🐰", "🦊",
    "🐻", "🐔", "🐧", "🐢", "🐙", "🦋"
]

TAMANHO = 6
cartas = ANIMAIS * 2
random.shuffle(cartas)

primeira = None
bloqueado = False
pares = 0
tentativas = 0

# Janela principal
janela = tk.Tk()
janela.title("Jogo da Memória - Animais")
janela.geometry("550x650")
janela.configure(bg="#176B45")
janela.resizable(False, False)

# Título
titulo = tk.Label(
    janela,
    text="🐾 JOGO DA MEMÓRIA 🐾",
    font=("Arial", 22, "bold"),
    bg="#176B45",
    fg="white"
)
titulo.pack(pady=15)

# Placar
placar = tk.Label(
    janela,
    text="Pares: 0/18     Tentativas: 0",
    font=("Arial", 15),
    bg="#176B45",
    fg="white"
)
placar.pack(pady=10)

# Tabuleiro
tabuleiro = tk.Frame(janela, bg="#176B45")
tabuleiro.pack(pady=10)

botoes = []

def atualizar_placar():
    placar.config(
        text=f"Pares: {pares}/18     Tentativas: {tentativas}"
    )

def virar_carta(indice):
    global primeira, bloqueado, pares, tentativas

    if bloqueado or botoes[indice]["text"] != "?":
        return

    botoes[indice].config(
        text=cartas[indice],
        bg="#FFFFFF"
    )

    if primeira is None:
        primeira = indice
    else:
        tentativas += 1
        atualizar_placar()

        segunda = indice

        if cartas[primeira] == cartas[segunda]:
            pares += 1
            primeira = None
            atualizar_placar()

            if pares == 18:
                mensagem.config(
                    text="🎉 PARABÉNS! VOCÊ VENCEU!"
                )
        else:
            bloqueado = True
            janela.after(
                1000,
                lambda: esconder_cartas(primeira, segunda)
            )

def esconder_cartas(a, b):
    global primeira, bloqueado

    botoes[a].config(text="?", bg="#F4D35E")
    botoes[b].config(text="?", bg="#F4D35E")

    primeira = None
    bloqueado = False

def reiniciar():
    global cartas, primeira, bloqueado, pares, tentativas

    cartas = ANIMAIS * 2
    random.shuffle(cartas)

    primeira = None
    bloqueado = False
    pares = 0
    tentativas = 0

    mensagem.config(text="")
    atualizar_placar()

    for botao in botoes:
        botao.config(text="?", bg="#F4D35E")

# Criar matriz 6x6
for linha in range(TAMANHO):
    for coluna in range(TAMANHO):
        indice = linha * TAMANHO + coluna

        botao = tk.Button(
            tabuleiro,
            text="?",
            font=("Arial", 22),
            width=4,
            height=2,
            bg="#F4D35E",
            command=lambda i=indice: virar_carta(i)
        )

        botao.grid(
            row=linha,
            column=coluna,
            padx=3,
            pady=3
        )

        botoes.append(botao)

# Mensagem
mensagem = tk.Label(
    janela,
    text="Encontre os 18 pares de animais!",
    font=("Arial", 13, "bold"),
    bg="#176B45",
    fg="white"
)
mensagem.pack(pady=15)

# Botão reiniciar
tk.Button(
    janela,
    text="🔄 NOVO JOGO",
    font=("Arial", 13, "bold"),
    bg="white",
    command=reiniciar
).pack(pady=10)

janela.mainloop()
