import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)

# Tamanho da janela e células
LARGURA = 300
ALTURA = 400  # espaço extra para o placar
TAMANHO_CELULA = 100
linha_largura = 5

# Cria a tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha")

# Fonte
fonte = pygame.font.Font(None, 80)
fonte_pequena = pygame.font.Font(None, 36)

# Tabuleiro e variáveis globais
tabuleiro = [["" for _ in range(3)] for _ in range(3)]
jogador_atual = "X"
jogo_encerrado = False
vencedor = None
placar = {"X": 0, "O": 0, "Empate": 0}

# Estado do jogo
menu_ativo = True


# Função para desenhar o menu inicial
def desenhar_menu():
    TELA.fill(BRANCO)
    titulo = fonte_pequena.render("Jogo da Velha", True, PRETO)
    jogar = fonte_pequena.render("Clique para Jogar", True, AZUL)
    TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))
    TELA.blit(jogar, (LARGURA // 2 - jogar.get_width() // 2, 200))
    pygame.display.flip()


# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    TELA.fill(BRANCO)

    # Linhas verticais
    pygame.draw.line(TELA, PRETO, (TAMANHO_CELULA, 0), (TAMANHO_CELULA, 300), linha_largura)
    pygame.draw.line(TELA, PRETO, (2 * TAMANHO_CELULA, 0), (2 * TAMANHO_CELULA, 300), linha_largura)

    # Linhas horizontais
    pygame.draw.line(TELA, PRETO, (0, TAMANHO_CELULA), (LARGURA, TAMANHO_CELULA), linha_largura)
    pygame.draw.line(TELA, PRETO, (0, 2 * TAMANHO_CELULA), (LARGURA, 2 * TAMANHO_CELULA), linha_largura)

    # Desenha os X e O
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] != "":
                texto = fonte.render(tabuleiro[linha][coluna], True,
                                     AZUL if tabuleiro[linha][coluna] == "X" else VERMELHO)
                x = coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2 - texto.get_width() // 2
                y = linha * TAMANHO_CELULA + TAMANHO_CELULA // 2 - texto.get_height() // 2
                TELA.blit(texto, (x, y))

    # Placar simples
    pygame.draw.rect(TELA, CINZA, (0, 300, LARGURA, 100))
    texto_placar = fonte_pequena.render(
        f"X: {placar['X']}  O: {placar['O']}  Empate: {placar['Empate']}",
        True, PRETO)
    TELA.blit(texto_placar, (LARGURA // 2 - texto_placar.get_width() // 2, 330))

    # Mensagem de fim de jogo
    if jogo_encerrado:
        texto = f"{'Empate!' if vencedor is None else f'{vencedor} venceu!'}"
        msg = fonte_pequena.render(texto + " (clique)", True, PRETO)
        TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, 360))


# Função que verifica vitória
def checar_vencedor():
    global vencedor, jogo_encerrado

    # Linhas
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] != "":
            vencedor = linha[0]
            jogo_encerrado = True
            placar[vencedor] += 1
            return

    # Colunas
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] != "":
            vencedor = tabuleiro[0][col]
            jogo_encerrado = True
            placar[vencedor] += 1
            return

    # Diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != "":
        vencedor = tabuleiro[0][0]
        jogo_encerrado = True
        placar[vencedor] += 1
        return
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != "":
        vencedor = tabuleiro[0][2]
        jogo_encerrado = True
        placar[vencedor] += 1
        return

    # Empate
    if all(cell != "" for row in tabuleiro for cell in row):
        vencedor = None
        jogo_encerrado = True
        placar["Empate"] += 1


# Reinicia o tabuleiro (mas mantém o placar)
def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogo_encerrado, vencedor
    tabuleiro = [["" for _ in range(3)] for _ in range(3)]
    jogador_atual = "X"
    jogo_encerrado = False
    vencedor = None


# Loop principal
while True:
    if menu_ativo:
        desenhar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                menu_ativo = False  # sai do menu
        continue

    desenhar_tabuleiro()
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jogada do jogador
        elif evento.type == pygame.MOUSEBUTTONDOWN and not jogo_encerrado:
            x, y = pygame.mouse.get_pos()
            if y < 300:  # só pode clicar dentro do tabuleiro
                linha = y // TAMANHO_CELULA
                coluna = x // TAMANHO_CELULA

                if tabuleiro[linha][coluna] == "":
                    tabuleiro[linha][coluna] = jogador_atual
                    checar_vencedor()
                    if not jogo_encerrado:
                        jogador_atual = "O" if jogador_atual == "X" else "X"

        # Reinicia quando o jogo termina
        elif evento.type == pygame.MOUSEBUTTONDOWN and jogo_encerrado:
            reiniciar_jogo()
