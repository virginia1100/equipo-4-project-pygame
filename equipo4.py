import pygame
import random
import array

pygame.init()
pygame.mixer.init()

# Pantalla
ANCHO = 600
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pygame")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

fuente = pygame.font.Font(None, 28)
reloj = pygame.time.Clock()

# ---- IMÁGENES ----
homer_img = pygame.image.load("Homer_Simpson.jpg")
homer_img = pygame.transform.scale(homer_img, (50, 70))

bart_img = pygame.image.load("bart-simpson.jpg")
bart_img = pygame.transform.scale(bart_img, (30, 30))

# ---- AUDIO ----
pygame.mixer.music.load("Audiohomero.mp3")

def reproducir_audio():
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)

def reiniciar():
    global jugador_rect, obj_rect, puntos
    global inicio, pausa, terminado, ganaste

    jugador_rect.x = 280
    jugador_rect.y = 180

    obj_rect.x = random.randint(0, 570)
    obj_rect.y = random.randint(0, 370)

    puntos[0] = 0
    inicio = True
    pausa = False
    terminado = False
    ganaste = False
    reproducir_audio()

# Jugador
jugador_rect = pygame.Rect(280, 180, 50, 70)
vel_jugador = 5

# Objetivo (Bart)
obj_rect = pygame.Rect(
    random.randint(0, 570),
    random.randint(0, 370),
    30, 30
)

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

    # ---- INICIO ----
    if inicio:
        pantalla.blit(fuente.render("Start now", True, NEGRO), (260, 130))
        pantalla.blit(fuente.render("Press SPACE to continue", True, NEGRO), (220, 160))
        pantalla.blit(fuente.render("Move with arrow keys", True, NEGRO), (260, 190))
        pantalla.blit(fuente.render("¡Good luck!", True, NEGRO), (230, 220))
        pygame.display.update()
        continue

    # ---- PAUSA ----
    if pausa:
        pantalla.blit(fuente.render("Paused game", True, NEGRO), (240, 180))
        pantalla.blit(fuente.render("Press P to continue", True, NEGRO), (180, 210))
        pygame.display.update()
        continue

    # ---- GAME OVER ----
    if terminado:
        pygame.mixer.music.stop()
        if ganaste:
            pantalla.blit(fuente.render("You win, game finished", True, NEGRO), (180, 180))
        else:
            pantalla.blit(fuente.render("Game over", True, NEGRO), (230, 180))

        pantalla.blit(fuente.render("Press R to restart", True, NEGRO), (200, 210))
        pantalla.blit(fuente.render("¡Good job!", True, NEGRO), (230, 240))
        pygame.display.update()
        continue

    # ---- JUEGO ----
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador_rect.x -= vel_jugador
    if teclas[pygame.K_RIGHT]:
        jugador_rect.x += vel_jugador
    if teclas[pygame.K_UP]:
        jugador_rect.y -= vel_jugador
    if teclas[pygame.K_DOWN]:
        jugador_rect.y += vel_jugador

    pantalla.blit(homer_img, jugador_rect)
    pantalla.blit(bart_img, obj_rect)

    # Colisión con Bart
    if jugador_rect.colliderect(obj_rect):
        puntos[0] += 1
        obj_rect.x = random.randint(0, 570)
        obj_rect.y = random.randint(0, 370)

    if puntos[0] >= 20:
        terminado = True
        ganaste = True

    pantalla.blit(fuente.render("Press P to pause the game.", True, NEGRO), (10, 35))
    pantalla.blit(fuente.render("Move", True, NEGRO), (10, 60))
    pantalla.blit(fuente.render(f"Score: {puntos[0]}", True, NEGRO), (10, 85))
    pantalla.blit(fuente.render("Catch the Barts! (20 times)", True, NEGRO), (10, 10))

    pygame.display.update()
    reloj.tick(60)

pygame.quit()

