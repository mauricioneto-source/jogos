
import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# =====================================
# CONFIGURAÇÕES
# =====================================

ANIMAIS = [
    "🐶", "🐱", "🐵", "🦁", "🐯", "🐸",
    "🐼", "🐨", "🐷", "🐮", "🐰", "🦊",
    "🐻", "🐔", "🐧", "🐢", "🐙", "🦋"
]

TAMANHO = 6
ARQUIVO_RANKING = "ranking.json"

# Variáveis do jogo
cartas = []
botoes = []

primeira = None
bloqueado = False
pares = 0
tentativas = 0

inicio = None
tempo_decorrido = 0
cronometro_ativo = False
jogo_finalizado = False

# =====================================
# RANKING
# =====================================

def carregar_ranking():
    if os.path.exists(ARQUIVO_RANKING):
        try:
            with open(ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                if isinstance(dados, list):
                    return dados
        except (json.JSONDecodeError, OSError):
            pass

    return []


def salvar_ranking(nome, tempo, tentativas):
    ranking = carregar_ranking()

    resultado = {
        "nome": nome,
        "tempo": tempo,
        "tentativas": tentativas
    }

    ranking.append(resultado)

    # Menor tempo e menor número de tentativas primeiro
    ranking.sort(
        key=lambda x: (
            x["tempo"],
            x["tentativas"]
        )
    )

    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as arquivo:
        json.dump(
            ranking,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def mostrar_ranking():
    ranking = carregar_ranking()

    tela = tk.Toplevel(janela)
    tela.title("Ranking dos Jogadores")
    tela.geometry("450x450")
    tela.configure(bg="#176B45")

    tk.Label(
        tela,
        text="🏆 RANKING DOS JOGADORES",
        font=("Arial", 18, "bold"),
        bg="#176B45",
        fg="white"
    ).pack(pady=15)

    if not ranking:
        tk.Label(
            tela,
            text="Ainda não existem resultados registrados.",
            font=("Arial", 12),
            bg="#176B45",
            fg="white"
        ).pack(pady=20)
    else:
        cabecalho = "POS.    JOGADOR       TEMPO     TENTATIVAS"

        tk.Label(
            tela,
            text=cabecalho,
            font=("Courier", 10, "bold"),
            bg="#176B45",
            fg="yellow"
        ).pack(pady=5)

        for posicao, jogador in enumerate(ranking[:10], start=1):
            minutos = jogador["tempo"] // 60
            segundos = jogador["tempo"] % 60

            texto = (
                f"{posicao:2}º   "
                f"{jogador['nome'][:12]:12} "
                f"{minutos:02}:{segundos:02}      "
                f"{jogador['tentativas']}"
            )

            tk.Label(
                tela,
                text=texto,
                font=("Courier", 11),
                bg="#176B45",
                fg="white"
            ).pack(pady=4)

    tk.Button(
        tela,
        text="FECHAR",
        font=("Arial", 12, "bold"),
        command=tela.destroy
    ).pack(pady=20)


# =====================================
# CRONÔMETRO
# =====================================

def atualizar_tempo():
    global tempo_decorrido

    if not cronometro_ativo:
        return

    tempo_decorrido = int(time.monotonic() - inicio)

    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60

    cronometro.config(
        text=f"⏱ Tempo: {minutos:02}:{segundos:02}"
    )

    janela.after(1000, atualizar_tempo)


def iniciar_cronometro():
    global inicio, cronometro_ativo

    if not cronometro_ativo:
        inicio = time.monotonic()
        cronometro_ativo = True
        atualizar_tempo()


# =====================================
# TABULEIRO
# =====================================

def atualizar_placar():
    placar.config(
        text=f"Pares: {pares}/18     Tentativas: {tentativas}"
    )


def esconder_cartas(a, b):
    global primeira, bloqueado

    if jogo_finalizado:
        return

    botoes[a].config(text="?", bg="#F4D35E")
    botoes[b].config(text="?", bg="#F4D35E")

    primeira = None
    bloqueado = False


def finalizar_jogo():
    global cronometro_ativo, jogo_finalizado

    cronometro_ativo = False
    jogo_finalizado = True

    nome = entrada_nome.get().strip()

    if not nome:
        nome = "Jogador"

    salvar_ranking(
        nome,
        tempo_decorrido,
        tentativas
    )

    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60

    mensagem.config(
        text="🎉 PARABÉNS! VOCÊ VENCEU!"
    )

    messagebox.showinfo(
        "Fim de jogo",
        f"Parabéns, {nome}!\n\n"
        f"Tempo: {minutos:02}:{segundos:02}\n"
        f"Tentativas: {tentativas}\n\n"
        "Seu resultado foi salvo no ranking!"
    )


def virar_carta(indice):
    global primeira, bloqueado, pares
    global tentativas

    if bloqueado or jogo_finalizado:
        return

    if botoes[indice]["text"] != "?":
        return

    # Inicia o cronômetro no primeiro clique
    iniciar_cronometro()

    botoes[indice].config(
        text=cartas[indice],
        bg="white"
    )

    if primeira is None:
        primeira = indice

    else:
        segunda = indice

        tentativas += 1
        atualizar_placar()

        if cartas[primeira] == cartas[segunda]:

            pares += 1
            primeira = None

            atualizar_placar()

            if pares == 18:
                finalizar_jogo()

        else:
            bloqueado = True

            a = primeira
            b = segunda

            janela.after(
                1000,
                lambda: esconder_cartas(a, b)
            )


# =====================================
# REINICIAR JOGO
# =====================================

def reiniciar():
    global cartas, primeira, bloqueado
    global pares, tentativas
    global inicio, tempo_decorrido
    global cronometro_ativo, jogo_finalizado

    cartas = ANIMAIS * 2
    random.shuffle(cartas)

    primeira = None
    bloqueado = False
    pares = 0
    tentativas = 0

    inicio = None
    tempo_decorrido = 0
    cronometro_ativo = False
    jogo_finalizado = False

    cronometro.config(text="⏱ Tempo: 00:00")

    mensagem.config(
        text="Encontre os 18 pares de animais!"
    )

    atualizar_placar()

    for indice, botao in enumerate(botoes):
        botao.config(
            text="?",
            bg="#F4D35E",
            state="normal"
        )



# =====================================
# INTERFACE PRINCIPAL LATERAL
# =====================================

janela = tk.Tk()
janela.title("Jogo da Memória - Animais")
janela.geometry("850x570")
janela.minsize(750, 500)
janela.configure(bg="#176B45")
janela.resizable(True, True)

# Iniciar maximizado
janela.state("zoomed")

# Título
tk.Label(
    janela,
    text="🐾 JOGO DA MEMÓRIA em PYTHON 🐾",
    font=("Arial", 23, "bold"),
    bg="#176B45",
    fg="white"
).pack(pady=12)

# Área principal: tabuleiro e informações
area_principal = tk.Frame(
    janela,
    bg="#176B45"
)
area_principal.pack(padx=15, pady=10)

# -------------------------------------
# LADO ESQUERDO - TABULEIRO
# -------------------------------------

lado_esquerdo = tk.Frame(
    area_principal,
    bg="#176B45"
)
lado_esquerdo.grid(row=0, column=0, padx=10)

tk.Label(
    lado_esquerdo,
    text="TABULEIRO 6 x 6",
    font=("Arial", 14, "bold"),
    bg="#176B45",
    fg="white"
).pack(pady=8)

tabuleiro = tk.Frame(
    lado_esquerdo,
    bg="#176B45"
)
tabuleiro.pack()

cartas = ANIMAIS * 2
random.shuffle(cartas)

botoes = []

for linha in range(TAMANHO):
    for coluna in range(TAMANHO):

        indice = linha * TAMANHO + coluna

        botao = tk.Button(
            tabuleiro,
            text="?",
            font=("Arial", 21),
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



# -------------------------------------
# LADO DIREITO - INFORMAÇÕES
# -------------------------------------

lado_direito = tk.Frame(
    area_principal,
    bg="#FFFFFF",
    width=210,
    height=420
)

lado_direito.grid(
    row=0,
    column=1,
    padx=15,
    sticky="n"
)

lado_direito.pack_propagate(False)

# Todos os elementos ficam em coluna
tk.Label(
    lado_direito,
    text="INFORMAÇÕES DO JOGO",
    font=("Arial", 12, "bold"),
    bg="#FFFFFF",
    fg="#176B45"
).pack(pady=(10, 8))

# Nome
tk.Label(
    lado_direito,
    text="Nome do jogador:",
    font=("Arial", 9, "bold"),
    bg="#FFFFFF",
    fg="#176B45"
).pack(pady=3)

entrada_nome = tk.Entry(
    lado_direito,
    font=("Arial", 10),
    justify="center",
    width=20
)
entrada_nome.pack(pady=3)

# Tempo
cronometro = tk.Label(
    lado_direito,
    text="Tempo: 00:00",
    font=("Arial", 11, "bold"),
    bg="#FFFFFF",
    fg="#176B45",
    anchor="center"
)
cronometro.pack(fill="x", pady=8)

# Pares
placar = tk.Label(
    lado_direito,
    text="Pares: 0/18",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#176B45",
    anchor="center"
)
placar.pack(fill="x", pady=5)

# Tentativas
tentativas_label = tk.Label(
    lado_direito,
    text="Tentativas: 0",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#176B45",
    anchor="center"
)
tentativas_label.pack(fill="x", pady=5)

# Mensagem
mensagem = tk.Label(
    lado_direito,
    text="Encontre os 18 pares!",
    font=("Arial", 9, "bold"),
    bg="#FFFFFF",
    fg="#176B45",
    wraplength=190,
    justify="center"
)
mensagem.pack(fill="x", pady=10)

# Botão novo jogo
tk.Button(
    lado_direito,
    text="NOVO JOGO",
    font=("Arial", 9, "bold"),
    width=18,
    command=reiniciar
).pack(pady=6)

# Botão ranking
tk.Button(
    lado_direito,
    text="VER RANKING",
    font=("Arial", 9, "bold"),
    width=18,
    command=mostrar_ranking
).pack(pady=6)


janela.mainloop()
