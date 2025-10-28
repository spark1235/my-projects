import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong Power-Ups")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Configurações da raquete
largura_raquete = 15
altura_raquete = 100
velocidade_raquete = 7

# Configurações da bola
tamanho_bola = 20
velocidade_inicial = 5

# Pontuação
pontuacao_esquerda = 0
pontuacao_direita = 0
fonte = pygame.font.Font(None, 74)

# Criar raquetes
raquete_esquerda = pygame.Rect(50, ALTURA // 2 - altura_raquete // 2, largura_raquete, altura_raquete)
raquete_direita = pygame.Rect(LARGURA - 50 - largura_raquete, ALTURA // 2 - altura_raquete // 2, largura_raquete, altura_raquete)

# Lista de bolas (começa com 1)
bolas = [pygame.Rect(LARGURA // 2 - tamanho_bola // 2, ALTURA // 2 - tamanho_bola // 2, tamanho_bola, tamanho_bola)]
velocidades_bolas = [[velocidade_inicial, velocidade_inicial]]

# Power-up
power_up = None
tipo_power_up = None  # "velocidade" ou "triplo"
tempo_proximo_power = random.randint(300, 600)  # frames até o próximo aparecer

# Controle de efeitos
efeito_triplo = False
efeito_velocidade = False

# Loop principal
clock = pygame.time.Clock()
while True:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and raquete_esquerda.top > 0:
        raquete_esquerda.y -= velocidade_raquete
    if teclas[pygame.K_s] and raquete_esquerda.bottom < ALTURA:
        raquete_esquerda.y += velocidade_raquete
    if teclas[pygame.K_UP] and raquete_direita.top > 0:
        raquete_direita.y -= velocidade_raquete
    if teclas[pygame.K_DOWN] and raquete_direita.bottom < ALTURA:
        raquete_direita.y += velocidade_raquete

    # Movimento das bolas
    for i, bola in enumerate(bolas):
        bola.x += velocidades_bolas[i][0]
        bola.y += velocidades_bolas[i][1]

        # Colisão com as bordas superior/inferior
        if bola.top <= 0 or bola.bottom >= ALTURA:
            velocidades_bolas[i][1] *= -1

        # Colisão com raquetes
        if bola.colliderect(raquete_esquerda) or bola.colliderect(raquete_direita):
            velocidades_bolas[i][0] *= -1

        # Colisão com power-up
        if power_up and bola.colliderect(power_up):
            if tipo_power_up == "velocidade" and not efeito_velocidade:
                # Aumenta velocidade de todas as bolas
                for v in velocidades_bolas:
                    v[0] *= 1.5
                    v[1] *= 1.5
                efeito_velocidade = True
            elif tipo_power_up == "triplo" and not efeito_triplo:
                # Cria duas novas bolas independentes
                novas_bolas = []
                novas_vels = []
                for _ in range(2):
                    nova = pygame.Rect(bola.x, bola.y, tamanho_bola, tamanho_bola)
                    novas_bolas.append(nova)
                    novas_vels.append([
                        random.choice([-1, 1]) * velocidade_inicial,
                        random.choice([-1, 1]) * velocidade_inicial
                    ])
                bolas.extend(novas_bolas)
                velocidades_bolas.extend(novas_vels)
                efeito_triplo = True
            power_up = None  # Remove power-up da tela

        # Pontuação
        if bola.left <= 0:
            pontuacao_direita += 1
            # Reset do jogo e efeitos
            bolas = [pygame.Rect(LARGURA // 2 - tamanho_bola // 2, ALTURA // 2 - tamanho_bola // 2, tamanho_bola, tamanho_bola)]
            velocidades_bolas = [[velocidade_inicial, velocidade_inicial]]
            efeito_triplo = False
            efeito_velocidade = False
            power_up = None
            tempo_proximo_power = random.randint(300, 600)
            break
        if bola.right >= LARGURA:
            pontuacao_esquerda += 1
            bolas = [pygame.Rect(LARGURA // 2 - tamanho_bola // 2, ALTURA // 2 - tamanho_bola // 2, tamanho_bola, tamanho_bola)]
            velocidades_bolas = [[velocidade_inicial, velocidade_inicial]]
            efeito_triplo = False
            efeito_velocidade = False
            power_up = None
            tempo_proximo_power = random.randint(300, 600)
            break

    # Gerar power-up aleatório
    tempo_proximo_power -= 1
    if tempo_proximo_power <= 0 and not power_up:
        tipo_power_up = random.choice(["velocidade", "triplo"])
        power_up = pygame.Rect(
            random.randint(100, LARGURA - 100),
            random.randint(100, ALTURA - 100),
            30, 30
        )

    # Desenhar
    tela.fill(PRETO)
    pygame.draw.rect(tela, BRANCO, raquete_esquerda)
    pygame.draw.rect(tela, BRANCO, raquete_direita)

    for bola in bolas:
        pygame.draw.ellipse(tela, BRANCO, bola)

    pygame.draw.aaline(tela, BRANCO, (LARGURA // 2, 0), (LARGURA // 2, ALTURA))

    # Power-up na tela
    if power_up:
        cor = VERMELHO if tipo_power_up == "velocidade" else AZUL
        pygame.draw.rect(tela, cor, power_up)

    # Mostrar pontuação
    texto_esquerda = fonte.render(str(pontuacao_esquerda), True, BRANCO)
    texto_direita = fonte.render(str(pontuacao_direita), True, BRANCO)
    tela.blit(texto_esquerda, (LARGURA // 4, 10))
    tela.blit(texto_direita, (LARGURA * 3 // 4, 10))

    pygame.display.flip()
    clock.tick(60)
