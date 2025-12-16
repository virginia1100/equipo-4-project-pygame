import pygame
import random
import array

pygame.init()

# Pantalla
ANCHO = 600
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego fácil")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

fuente = pygame.font.Font(None, 28)
reloj = pygame.time.Clock()

# Cargar imagen del jugador
homer_img = pygame.image.load("Homer_Simpson.jpg")
homer_img = pygame.transform.scale(homer_img, (50, 70))

def reiniciar():
    global jugador_rect, obj_rect, obstaculos, puntos
    global inicio, pausa, terminado, ganaste

    jugador_rect.x = 280
    jugador_rect.y = 180

    obj_rect.x = random.randint(0, 570)
    obj_rect.y = random.randint(0, 370)

    obstaculos.clear()
    for i in range(3):
        ox = random.randint(0, 570)
        oy = random.randint(-200, 0)
        vel = random.randint(2, 3)
        obstaculos.append([pygame.Rect(ox, oy, 30, 30), vel])

    puntos[0] = 0
    inicio = True
    pausa = False
    terminado = False
    ganaste = False

# Jugador
jugador_rect = pygame.Rect(280, 180, 40, 70)
vel_jugador = 5

# Objetivo
obj_rect = pygame.Rect(
    random.randint(0, 570),
    random.randint(0, 370),
    30, 30
)

# Obstáculos (lista)
obstaculos = []

# Puntos (array)
puntos = array.array('i', [0])

# Estados
inicio = True
pausa = False
terminado = False
ganaste = False

reiniciar()

jugando = True
while jugando:
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN:
            if inicio and evento.key == pygame.K_SPACE:
                inicio = False
            elif not inicio and evento.key == pygame.K_p:
                pausa = not pausa
            elif terminado and evento.key == pygame.K_r:
                reiniciar()

    # ----- INICIO -----
    if inicio:
        pantalla.blit(fuente.render("Comenzar", True, NEGRO), (260, 130))
        pantalla.blit(fuente.render("Presiona ESPACIO", True, NEGRO), (220, 160))
        pantalla.blit(fuente.render("Mover", True, NEGRO), (260, 190))
        pantalla.blit(fuente.render("¡Buena suerte!", True, NEGRO), (230, 220))
        pygame.display.update()
        continue

    # ----- PAUSA -----
    if pausa:
        pantalla.blit(fuente.render("Juego en pausa", True, NEGRO), (240, 180))
        pantalla.blit(fuente.render("Presione P para continuar", True, NEGRO), (180, 210))
        pygame.display.update()
        continue

    # ----- GAME OVER -----
    if terminado:
        if ganaste:
            pantalla.blit(fuente.render("Ganaste, juego terminado", True, NEGRO), (180, 180))
        else:
            pantalla.blit(fuente.render("Juego terminado", True, NEGRO), (230, 180))

        pantalla.blit(fuente.render("Presiona R para reiniciar", True, NEGRO), (200, 210))
        pantalla.blit(fuente.render("Ups! Intenta de nuevo", True, NEGRO), (230, 240))
        pygame.display.update()
        continue

    # ----- JUEGO -----
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador_rect.x -= vel_jugador
    if teclas[pygame.K_RIGHT]:
        jugador_rect.x += vel_jugador
    if teclas[pygame.K_UP]:
        jugador_rect.y -= vel_jugador
    if teclas[pygame.K_DOWN]:
        jugador_rect.y += vel_jugador

    # Dibujar jugador (sprite)
    pantalla.blit(homer_img, jugador_rect)

    # Objetivo
    pygame.draw.rect(pantalla, ROJO, obj_rect)

    # Obstáculos
    for obs in obstaculos:
        obs[0].y += obs[1]
        if obs[0].top > ALTO:
            obs[0].y = -30
            obs[0].x = random.randint(0, 570)

        pygame.draw.rect(pantalla, NEGRO, obs[0])

        if jugador_rect.colliderect(obs[0]):
            terminado = True

    # Colisión con objetivo
    if jugador_rect.colliderect(obj_rect):
        puntos[0] += 1
        obj_rect.x = random.randint(0, 570)
        obj_rect.y = random.randint(0, 370)

    if puntos[0] >= 10:
        terminado = True
        ganaste = True

    # Textos obligatorios
    pantalla.blit(fuente.render("¡Evita todos los obstáculos!", True, NEGRO), (10, 10))
    pantalla.blit(fuente.render("Presione P para pausar el juego.", True, NEGRO), (10, 35))
    pantalla.blit(fuente.render("Mover", True, NEGRO), (10, 60))
    pantalla.blit(fuente.render(f"Puntos: {puntos[0]}", True, NEGRO), (10, 85))

    pygame.display.update()
    reloj.tick(60)

pygame.quit()
