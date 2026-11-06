
import random
import os
import time

# -----------------------------------
# JOGO DA MEMÓRIA - MATRIZ 6 x 6
# -----------------------------------

TAMANHO = 6
TOTAL_PARES = (TAMANHO * TAMANHO) // 2

# Símbolos das cartas
simbolos = [
    "A", "B", "C", "D", "E", "F",
    "G", "H", "I", "J", "K", "L",
    "M", "N", "O", "P", "Q", "R"
]

# Cada símbolo aparece duas vezes
cartas = simbolos * 2
random.shuffle(cartas)

# Criação da matriz 6 x 6
matriz = [
    cartas[i:i + TAMANHO]
    for i in range(0, len(cartas), TAMANHO)
]

# Matriz que controla as cartas descobertas
visiveis = [
    [False] * TAMANHO
    for _ in range(TAMANHO)
]

pares_encontrados = 0
tentativas = 0


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_tabuleiro():
    print("\n     JOGO DA MEMÓRIA - 6 x 6\n")

    # Cabeçalho das colunas
    print("    ", end="")
    for coluna in range(TAMANHO):
        print(f"{coluna + 1:3}", end="")
    print("\n")

    # Linhas da matriz
    for linha in range(TAMANHO):
        print(f"{linha + 1:2}  ", end="")

        for coluna in range(TAMANHO):
            if visiveis[linha][coluna]:
                print(f"{matriz[linha][coluna]:3}", end="")
            else:
                print(" X ", end="")

        print()

    print(f"\nPares encontrados: {pares_encontrados}/{TOTAL_PARES}")
    print(f"Tentativas: {tentativas}")


def selecionar_carta():
    while True:
        try:
            linha = int(input("Digite a linha (1 a 6): ")) - 1
            coluna = int(input("Digite a coluna (1 a 6): ")) - 1

            if not (0 <= linha < TAMANHO and
                    0 <= coluna < TAMANHO):
                print("Posição inválida!")
                continue

            if visiveis[linha][coluna]:
                print("Essa carta já foi descoberta!")
                continue

            return linha, coluna

        except ValueError:
            print("Digite somente números!")


# -----------------------------------
# EXECUÇÃO DO JOGO
# -----------------------------------

while pares_encontrados < TOTAL_PARES:

    limpar_tela()
    mostrar_tabuleiro()

    print("\nSelecione a primeira carta.")
    l1, c1 = selecionar_carta()
    visiveis[l1][c1] = True

    limpar_tela()
    mostrar_tabuleiro()

    print("\nSelecione a segunda carta.")
    l2, c2 = selecionar_carta()
    visiveis[l2][c2] = True

    tentativas += 1

    limpar_tela()
    mostrar_tabuleiro()

    # Verificação do par
    if matriz[l1][c1] == matriz[l2][c2]:

        print("\nPar encontrado!")
        pares_encontrados += 1

    else:

        print("\nCartas diferentes!")

        time.sleep(2)

        visiveis[l1][c1] = False
        visiveis[l2][c2] = False


# -----------------------------------
# FINALIZAÇÃO
# -----------------------------------

limpar_tela()
mostrar_tabuleiro()

print("\n================================")
print("       PARABÉNS! VOCÊ VENCEU!")
print("================================")
print(f"Total de tentativas: {tentativas}")
print(f"Total de pares: {pares_encontrados}")
print(f"================================")
