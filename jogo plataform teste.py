import pygame
import sys
import random

pygame.init()

# Janela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("jogo plataforma teste")

# Cores simples
BRANCO = (255, 255, 255)
CINZA = (180, 180, 180)
VERDE = (34, 177, 76)
AZUL = (50, 150, 255)
AMARELO = (255, 200, 0)
DOURADO = (255, 215, 0)
MARROM = (120, 70, 20)
PRETO = (0, 0, 0)
VERDE_GRAMA = (100, 200, 100)
LARANJA = (255, 140, 0)

clock = pygame.time.Clock()
FPS = 60

# Mundo
WORLD_WIDTH = 4000    # comprimento da fase
GROUND_HEIGHT = 40    # altura do chão

# Jogador 
PLAYER_W = 48
PLAYER_H = 48
player_x = 100.0
player_y = ALTURA - GROUND_HEIGHT - PLAYER_H
player_vx = 0.0
player_vy = 0.0

# Física / movimento
ACCEL = 1.0          # aceleração ao andar
FRICTION = 0.85      # atrito horizontal
MAX_SPEED = 14       # velocidade máxima normal
GRAVITY = 0.9        # gravidade
JUMP_SPEED = -16     # velocidade do pulo
on_ground = False    # flag chão

# Spin dash
charging = False     # carregando spin dash
spin_charge = 0      # valor de carga
SPIN_CHARGE_MAX = 40 # carga máxima
is_spinning = False  # em movimento spindash
spin_timer = 0       # tempo de spin ativo
SPIN_DURATION = 40   # duração do efeito

# Anéis e placar
rings = []           # lista de posições de anéis
ring_count = 0       # contador de anéis
for i in range(60):  # espalha vários anéis pela fase
    rx = 300 + i * 50 + random.randint(-20, 20)
    ry = ALTURA - GROUND_HEIGHT - 100 - random.randint(0, 120)
    rings.append([rx, ry])

# Plataformas (start, middle, end)
platforms = []
# chão contínuo
platforms.append(pygame.Rect(0, ALTURA - GROUND_HEIGHT, WORLD_WIDTH, GROUND_HEIGHT))
# plataformas elevadas 
platforms += [
    pygame.Rect(250, ALTURA - GROUND_HEIGHT - 120, 200, 20),
    pygame.Rect(550, ALTURA - GROUND_HEIGHT - 200, 220, 20),
    pygame.Rect(900, ALTURA - GROUND_HEIGHT - 100, 180, 20),
    pygame.Rect(1400, ALTURA - GROUND_HEIGHT - 160, 220, 20),
    pygame.Rect(1750, ALTURA - GROUND_HEIGHT - 90, 160, 20),
    pygame.Rect(2100, ALTURA - GROUND_HEIGHT - 220, 260, 20),
    pygame.Rect(2600, ALTURA - GROUND_HEIGHT - 140, 200, 20),
    pygame.Rect(3000, ALTURA - GROUND_HEIGHT - 100, 300, 20),
    pygame.Rect(3500, ALTURA - GROUND_HEIGHT - 180, 200, 20),
]

# Inimigos simples
enemies = []
# cada inimigo é dict com rect, dir e speed
enemies.append({"rect": pygame.Rect(600, ALTURA - GROUND_HEIGHT - 40 - 32, 32, 32), "dir": -1, "speed": 1.8})
enemies.append({"rect": pygame.Rect(1500, ALTURA - GROUND_HEIGHT - 160 - 32, 32, 32), "dir": 1, "speed": 1.6})
enemies.append({"rect": pygame.Rect(2600, ALTURA - GROUND_HEIGHT - 140 - 32, 32, 32), "dir": -1, "speed": 2.0})
enemies.append({"rect": pygame.Rect(3200, ALTURA - GROUND_HEIGHT - 32 - 32, 32, 32), "dir": 1, "speed": 1.4})

# chegada / anel final
goal_ring = pygame.Rect(WORLD_WIDTH - 200, ALTURA - GROUND_HEIGHT - 100, 64, 64)
level_complete = False
level_complete_timer = 0

# Camera / offset
camera_x = 0

# Fonte
font = pygame.font.SysFont(None, 28)
bigfont = pygame.font.SysFont(None, 56)

def draw_background(offset_x):
    """Desenha fundo simples ."""
    # céu
    TELA.fill((129, 200, 255))
    # colinas simples repetidas
    hill_width = 400
    for i in range(-1, WORLD_WIDTH // hill_width + 2):
        cx = i * hill_width - offset_x * 0.3
        pygame.draw.ellipse(TELA, VERDE_GRAMA, (cx - 100, ALTURA - 220, hill_width + 200, 300))
    # algumas arvores simples
    for i in range(10):
        px = 200 + i * 450 - offset_x * 0.6
        py = ALTURA - GROUND_HEIGHT - 60
        pygame.draw.rect(TELA, MARROM, (px, py, 10, 50))
        pygame.draw.polygon(TELA, VERDE, [(px+5, py), (px+5+30, py-10), (px+5, py-20)])
        pygame.draw.polygon(TELA, VERDE, [(px+5, py-10), (px+5-30, py-20), (px+5, py-40)])

def world_to_screen(wx, wy, offset_x):
    """Converte coordenada do mundo para tela."""
    return int(wx - offset_x), int(wy)

def draw_platforms(offset_x):
    """Desenha plataformas e chão."""
    for plat in platforms:
        sx, sy = world_to_screen(plat.x, plat.y, offset_x)
        pygame.draw.rect(TELA, VERDE, (sx, sy, plat.w, plat.h))
        # borda para detalhe
        pygame.draw.rect(TELA, MARROM, (sx, sy, plat.w, 6))

def draw_rings(offset_x):
    """Desenha anéis."""
    for r in rings:
        sx, sy = world_to_screen(r[0], r[1], offset_x)
        pygame.draw.circle(TELA, AMARELO, (sx + 8, sy + 8), 8)
        pygame.draw.circle(TELA, DOURADO, (sx + 8, sy + 8), 4)

def draw_enemies(offset_x):
    """Desenha inimigos simples."""
    for e in enemies:
        sx, sy = world_to_screen(e["rect"].x, e["rect"].y, offset_x)
        pygame.draw.rect(TELA, LARANJA, (sx, sy, e["rect"].w, e["rect"].h))
        # olho
        pygame.draw.circle(TELA, PRETO, (sx + 8, sy + 8), 3)

def draw_goal(offset_x):
    """Desenha o anel final."""
    sx, sy = world_to_screen(goal_ring.x, goal_ring.y, offset_x)
    pygame.draw.circle(TELA, DOURADO, (sx + goal_ring.w // 2, sy + goal_ring.h // 2), 34)
    pygame.draw.circle(TELA, PRETO, (sx + goal_ring.w // 2, sy + goal_ring.h // 2), 12)

def clamp(value, a, b):
    """Limita valor entre a e b."""
    return max(a, min(b, value))

# Estado de invencibilidade curto após spin ou hit
invincible_timer = 0

# desenho jogador
def draw_player(px, py, spinning, offset_x):
    """Desenha jogador."""
    sx, sy = world_to_screen(px, py, offset_x)
    rect = pygame.Rect(sx, sy, PLAYER_W, PLAYER_H)
    color = (200, 200, 255) if not spinning else (80, 80, 200)
    pygame.draw.ellipse(TELA, color, rect)
    # óculos/olho simples
    pygame.draw.circle(TELA, PRETO, (sx + 34, sy + 18), 6)

# Mensagem no topo com pontuação
def draw_hud():
    txt = font.render(f"Rings: {ring_count}", True, PRETO)
    TELA.blit(txt, (10, 10))
    if charging:
        chargetxt = font.render(f"Charge: {spin_charge}", True, PRETO)
        TELA.blit(chargetxt, (10, 40))
    if is_spinning:
        spintxt = font.render("SPIN DASH!", True, PRETO)
        TELA.blit(spintxt, (10, 40))

# Loop principal
running = True
while running:
    dt = clock.tick(FPS)
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Spin dash: começa a carregar ao pressionar para baixo quando no chão
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and on_ground and not is_spinning:
                charging = True
                spin_charge = 0

        if event.type == pygame.KEYUP:
            # soltar o botão down ativa o spin dash se estava carregando
            if event.key == pygame.K_DOWN and charging:
                charging = False
                # aplica força baseada na carga
                burst = 6 + (spin_charge / SPIN_CHARGE_MAX) * 28
                # dispara para a direção que está pressionada (esquerda/direita)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player_vx = -burst
                else:
                    player_vx = burst
                is_spinning = True
                spin_timer = SPIN_DURATION
                invincible_timer = SPIN_DURATION  # invencível curto
                # pequena subida ao lançar
                player_vy = -2

    # Entradas para movimento normal
    keys = pygame.key.get_pressed()
    if not is_spinning:
        # acelera dependendo da tecla
        if keys[pygame.K_LEFT]:
            player_vx -= ACCEL
        elif keys[pygame.K_RIGHT]:
            player_vx += ACCEL
        else:
            # aplica atrito
            player_vx *= FRICTION

        # limita velocidade
        player_vx = clamp(player_vx, -MAX_SPEED, MAX_SPEED)
    else:
        # quando girando, fricção reduz mais devagar
        player_vx *= 0.995

    # pulo
    if keys[pygame.K_SPACE] and on_ground:
        player_vy = JUMP_SPEED
        on_ground = False

    # carregar spin dash se estiver segurando down
    if charging:
        spin_charge = min(SPIN_CHARGE_MAX, spin_charge + 1)

    # aplica gravidade
    player_vy += GRAVITY

    # atualiza posição
    player_x += player_vx
    player_y += player_vy

    # limites do mundo
    player_x = clamp(player_x, 0, WORLD_WIDTH - PLAYER_W)
    # cria rect do jogador no mundo
    player_rect = pygame.Rect(int(player_x), int(player_y), PLAYER_W, PLAYER_H)

    # colisões com plataformas (simples: verifica apenas correção vertical)
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            # se vinha caindo e penetramos no topo da plataforma
            if player_vy > 0 and player_rect.bottom - player_vy <= plat.top + 1:
                player_y = plat.top - PLAYER_H
                player_vy = 0
                on_ground = True
                player_rect.y = int(player_y)
            # colisão lateral simples: empurra para fora
            elif player_vx > 0 and player_rect.left < plat.right and player_rect.right > plat.right:
                player_x = plat.right
                player_vx = 0
            elif player_vx < 0 and player_rect.right > plat.left and player_rect.left < plat.left:
                player_x = plat.left - PLAYER_W
                player_vx = 0

    # atualiza rect depois de possíveis correções
    player_rect = pygame.Rect(int(player_x), int(player_y), PLAYER_W, PLAYER_H)

    # atualiza inimigos: caminham e trocam direção ao atingir bordas da plataforma abaixo deles
    for e in enemies:
        e["rect"].x += e["dir"] * e["speed"]
        # encontra plataforma sob o inimigo
        under = None
        for plat in platforms:
            if plat.left - 1 <= e["rect"].centerx <= plat.right + 1 and plat.top >= e["rect"].bottom:
                # verifica que está logo acima da plataforma
                if abs(plat.top - e["rect"].bottom) < 80:
                    under = plat
                    break
        # se não houver plataforma ou chegou na borda, inverte
        if under:
            if e["rect"].left < under.left or e["rect"].right > under.right:
                e["dir"] *= -1
        else:
            # cai se não tiver plataforma
            e["rect"].y += 4
        # colisão com jogador
        if player_rect.colliderect(e["rect"]):
            if invincible_timer <= 0:
                # se o jogador estiver descendo sobre o inimigo, derrota inimigo
                if player_vy > 2 and player_rect.bottom - e["rect"].top < 20:
                    # 'pula' no inimigo
                    player_vy = JUMP_SPEED / 2
                    # remove o inimigo
                    enemies.remove(e)
                else:
                    # dano: perde anéis e volta ao início do pedaço
                    ring_count = max(0, ring_count // 2)
                    player_x = max(50, player_x - 150)
                    player_vx = -6
                    player_vy = -6
                    invincible_timer = 90  # tempo de invencibilidade após dano
                    charging = False
                    is_spinning = False

    # coleta de anéis
    for r in rings[:]:
        rx, ry = r
        ring_rect = pygame.Rect(rx, ry, 16, 16)
        if player_rect.colliderect(ring_rect):
            rings.remove(r)
            ring_count += 1

    # colisão com ring final
    if player_rect.colliderect(goal_ring):
        level_complete = True
        level_complete_timer = 180

    # decrementa timers
    if spin_timer > 0:
        spin_timer -= 1
    else:
        is_spinning = False

    if invincible_timer > 0:
        invincible_timer -= 1

    # câmera segue jogador
    target_cam = player_x - LARGURA // 3
    camera_x += (target_cam - camera_x) * 0.12
    camera_x = clamp(camera_x, 0, WORLD_WIDTH - LARGURA)

    # desenha cena
    draw_background(camera_x)
    draw_platforms(camera_x)
    draw_rings(camera_x)
    draw_enemies(camera_x)
    draw_goal(camera_x)

    # desenha jogador
    draw_player(player_x, player_y, is_spinning, camera_x)

    # HUD
    draw_hud()

    # indicador de invencibilidade
    if invincible_timer > 0 and (invincible_timer // 6) % 2 == 0:
        # marcador piscando
        invtxt = font.render("INV", True, PRETO)
        TELA.blit(invtxt, (LARGURA - 80, 10))

    # se completar nível, mostra mensagem e pausa curta
    if level_complete:
        level_complete_timer -= 1
        msg = bigfont.render("Stage Clear!", True, PRETO)
        TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2 - 50))
        sub = font.render(f"Rings collected: {ring_count}", True, PRETO)
        TELA.blit(sub, (LARGURA // 2 - sub.get_width() // 2, ALTURA // 2 + 10))
        if level_complete_timer <= 0:
            # reiniciar ou encerrar fase para simplicidade
            running = False

    # HUD: instruções simples
    hint = font.render("Arrows: move  Space: jump  Down: hold to charge spin, release to dash", True, PRETO)
    TELA.blit(hint, (10, ALTURA - 28))

    pygame.display.flip()

pygame.quit()
print("Fase concluída. Obrigado por jogar!")
