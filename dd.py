import pygame
import sys

pygame.init()

# Configuration audio
pygame.mixer.init()
pygame.mixer.set_num_channels(32)  # Nombre de canaux audio

# Configuration de la fenêtre
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Spatialisation sonore avec Pygame")

clock = pygame.time.Clock()

# Charger le son
sound = pygame.mixer.Sound("ressource/song.mp3")


# Fonction pour jouer le son à une position spécifique
def play_sound(position):
    channel = pygame.mixer.find_channel()  # Trouver un canal disponible
    if channel:
        distance = pygame.math.Vector2(position[0] - window_size[0] // 2, position[1] - window_size[1] // 2)
        max_distance = pygame.math.Vector2(window_size[0] // 2, window_size[1] // 2)

        # Volume en fonction de la distance
        volume = max(0, 1 - (distance.length() / max_distance.length()))
        channel.set_volume(volume)

        # Pan en fonction de la position horizontale
        pan = (position[0] - window_size[0] // 2) / (window_size[0] // 2)

        # Ajuster le volume et le pan
        channel.set_volume(volume)
        channel.set_pan(pan)

        channel.play(sound)


# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))  # Fond blanc

    # Obtenir la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Dessiner un cercle à la position de la souris
    pygame.draw.circle(screen, (0, 0, 255), (mouse_x, mouse_y), 10)

    # Jouer le son à la position de la souris
    play_sound((mouse_x, mouse_y))

    pygame.display.flip()
    clock.tick(60)  # Limiter la fréquence d'images à 60 FPS
