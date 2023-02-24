import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WIDTH = 500
HEIGHT = 500

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Erstellen des Fensters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Spiel")

# Spielfigur
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - player_size * 2]

# Hindernisse
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

# Geschwindigkeit
SPEED = 10

# Schleife zum Ausführen des Spiels
game_over = False
clock = pygame.time.Clock()


## FUNCTIONS -----------------------------------------------------------------------------------------------------
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True

    return False


def draw_player(screen, player_pos, player_size):
    pygame.draw.rect(screen, BLACK,)

while not game_over:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Tastenabfrage
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= SPEED
    elif keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += SPEED

    # Bewegung der Hindernisse
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)

    # Hinzufügen neuer Hindernisse
    if random.randint(0, 10) == 0:
        enemy_list.append([random.randint(0, WIDTH - enemy_size), 0])

    # Kollisionserkennung
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            game_over = True
            break

    # Hintergrund zeichnen
    screen.fill(WHITE)

    # Spielfigur zeichnen
    draw_player(screen, player_pos, player_size)

    # Hindernisse zeichnen
    for enemy_pos in enemy_list:
        draw_enemy(screen, enemy_pos, enemy_size)

    # Aktualisierung des Bildschirms
    pygame.display.update()

    # FPS
    clock.tick(30)

# Beenden von Pygame
pygame.quit()
