import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Constantes da tela
LARGURA = 600
ALTURA = 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game - Power Up!")

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)

# Tamanho dos blocos
TAMANHO_BLOCO = 20

# Relógio e velocidade base
clock = pygame.time.Clock()
velocidade_base = 10
velocidade = velocidade_base

# Função para gerar posição aleatória da comida
def gerar_fruta():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return [x, y]

# Função para gerar o power-up (posição aleatória)
def gerar_powerup():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return [x, y]

# Inicialização da cobra e da fruta
cobra = [[100, 100]]
direcao = 'DIREITA'
fruta = gerar_fruta()
powerup = None  # sem power-up no início
powerup_timer = 0  # tempo restante do efeito
pontuacao = 0

# Função para desenhar a cobra
def desenhar_cobra():
    for segmento in cobra:
        pygame.draw.rect(TELA, VERDE, pygame.Rect(segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

# Função para mostrar a pontuação e o estado do power-up
def mostrar_info():
    fonte = pygame.font.SysFont('arial', 24)
    texto = fonte.render(f'Pontuação: {pontuacao}', True, BRANCO)
    TELA.blit(texto, (10, 10))

    if powerup_timer > 0:
        tempo_txt = fonte.render(f'Boost: {powerup_timer // 30}s', True, AZUL)
        TELA.blit(tempo_txt, (10, 40))

# Loop principal do jogo
while True:
    clock.tick(velocidade)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            # Controle da direção
            if evento.key == pygame.K_UP and direcao != 'BAIXO':
                direcao = 'CIMA'
            elif evento.key == pygame.K_DOWN and direcao != 'CIMA':
                direcao = 'BAIXO'
            elif evento.key == pygame.K_LEFT and direcao != 'DIREITA':
                direcao = 'ESQUERDA'
            elif evento.key == pygame.K_RIGHT and direcao != 'ESQUERDA':
                direcao = 'DIREITA'

    # Move a cobra
    x, y = cobra[0]
    if direcao == 'CIMA':
        y -= TAMANHO_BLOCO
    elif direcao == 'BAIXO':
        y += TAMANHO_BLOCO
    elif direcao == 'ESQUERDA':
        x -= TAMANHO_BLOCO
    elif direcao == 'DIREITA':
        x += TAMANHO_BLOCO

    nova_cabeca = [x, y]
    cobra.insert(0, nova_cabeca)

    # Verifica se comeu a fruta
    if nova_cabeca == fruta:
        pontuacao += 1
        fruta = gerar_fruta()
        # Chance pequena de aparecer um power-up
        if powerup is None and random.random() < 0.2:
            powerup = gerar_powerup()
    else:
        cobra.pop()  # remove o último segmento

    # Verifica se pegou o power-up
    if powerup and nova_cabeca == powerup:
        velocidade = 20  # aumenta a velocidade
        powerup_timer = 180  # dura 6 segundos (30 FPS * 6)
        powerup = None  # remove o power-up

    # Diminui o tempo do power-up ativo
    if powerup_timer > 0:
        powerup_timer -= 1
    else:
        velocidade = velocidade_base

    # Verifica colisões
    if (x < 0 or x >= LARGURA or y < 0 or y >= ALTURA) or (nova_cabeca in cobra[1:]):
        break  # fim do jogo

    # Desenha tudo
    TELA.fill(PRETO)
    desenhar_cobra()
    pygame.draw.rect(TELA, VERMELHO, pygame.Rect(fruta[0], fruta[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
    if powerup:
        pygame.draw.rect(TELA, AZUL, pygame.Rect(powerup[0], powerup[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
    mostrar_info()
    pygame.display.flip()

# Fim de jogo
pygame.quit()
print(f"Fim de jogo! Sua pontuação foi: {pontuacao}")
