import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Erstellen des Fensters
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Spieler
player_width = 50
player_height = 50
player_x = WINDOW_WIDTH/2 - player_width/2
player_y = WINDOW_HEIGHT - player_height - 10
player_speed = 5

def draw_player():
    pygame.draw.rect(window, BLACK, (player_x, player_y, player_width, player_height))

# Schleife, die das Spiel ausführt
running = True
while running:
    # Überprüfen, ob das Spiel beendet werden soll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Bewegung des Spielers
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_width:
        player_x += player_speed
    elif keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - player_height:
        player_y += player_speed
    
    # Hintergrundfarbe
    window.fill(WHITE)
    
    # Zeichnen des Spielers
    draw_player()
    
    # Anzeigen des Spiels
    pygame.display.flip()

# Beenden von Pygame
pygame.quit()