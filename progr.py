import pygame
import sys
import math


# La fonction "Point dans le triangle" renvoie vrai si le point x,y est dans le triangle (x1,y1,x2,y2,x3,y3).
# Elle est notamment utilisée pour déterminer de quel côté (vertical ou horizontal) un rayon touche un bloc
def point_dans_triangle(x, y, x1, y1, x2, y2, x3, y3):
    detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / detT
    beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / detT
    gamma = 1 - alpha - beta

    return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1


# La fonction "lance rayons" lance tous les rayons et pour chaque rayon, avance pas à pas jusqu'à rencontrer un block.
# Si un block est rencontré, alors un bout de mur est dessiné avec une hauteur qui depend de la longueur du rayon.
# Plus le rayon est long, plus le bout de mur est petit
def lance_rayons():
    angle_depart = player_angle + MOITIE_FOV
    cible_x = 0.0
    cible_y = 0.0
    profondeur = 0.0
    # pour chaque rayon
    for ray in range(NOMBRE_RAYONS):
        # on avance pas à pas
        for profondeur in range(PROFONDEUR_MAX):
            cible_x_prec = cible_x
            cible_y_prec = cible_y
            cible_x = player_x + math.cos(angle_depart) * profondeur
            cible_y = player_y - math.sin(angle_depart) * profondeur
            col = int(cible_x / TAILLE_BLOCK)
            lig = int(cible_y / TAILLE_BLOCK)
            print(col, player_y)
            block = lig * TAILLE_CARTE + col

            print(block)
            # Si le rayon atteint un block
            if CARTE[block] == '#':
                # on vérifie si l'impact est horizontal ou vertical
                est_horizontal = not (
                        (
                            point_dans_triangle(
                                cible_x,
                                cible_y,
                                (col * TAILLE_BLOCK),
                                (lig * TAILLE_BLOCK),
                                (col * TAILLE_BLOCK),
                                ((lig * TAILLE_BLOCK) + TAILLE_BLOCK),
                                (col * TAILLE_BLOCK) + TAILLE_BLOCK / 2,
                                (lig * TAILLE_BLOCK) + TAILLE_BLOCK / 2)
                        ) or (
                            point_dans_triangle(
                                cible_x,
                                cible_y,
                                ((col * TAILLE_BLOCK) + TAILLE_BLOCK / 2),
                                ((lig * TAILLE_BLOCK) + TAILLE_BLOCK / 2),
                                ((col * TAILLE_BLOCK) + TAILLE_BLOCK),
                                (lig * TAILLE_BLOCK),
                                (col * TAILLE_BLOCK) + TAILLE_BLOCK,
                                (lig * TAILLE_BLOCK) + TAILLE_BLOCK)
                        )
                )
                couleur = 100 / (1 + profondeur * profondeur * 0.0001)

                profondeur *= math.cos(player_angle - angle_depart)
                hauteur_mur = 21000 / (profondeur + 0.0001)

                if hauteur_mur > HAUTEUR_ECRAN: hauteur_mur == HAUTEUR_ECRAN
                # si le booleen "dessine texture" est a vrai, j'utilise la texture du mur, sinon je dessine des murs d'une couleur unie
                if (est_horizontal):
                        print(
                            (
                                HAUTEUR_ECRAN + ray * SCALE, (HAUTEUR_ECRAN / 2) - hauteur_mur / 2, SCALE, hauteur_mur)
                        )
                        pygame.draw.rect(fenetre, (couleur, 0, 0), (
                        HAUTEUR_ECRAN + ray * SCALE, (HAUTEUR_ECRAN / 2) - hauteur_mur / 2, SCALE, hauteur_mur))
                else:
                        pygame.draw.rect(fenetre, (0, couleur, 0), (
                        HAUTEUR_ECRAN + ray * SCALE, (HAUTEUR_ECRAN / 2) - hauteur_mur / 2, SCALE, hauteur_mur))
                break
        angle_depart -= STEP_ANGLE


# La fonction "dessine CARTE" dessine la partie gauche de l'écran, qui correspond à une vue du dessus et des rayons de la scène
def dessine_CARTE():
    for lig in range(8):
        for col in range(8):
            block = lig * TAILLE_CARTE + col

            pygame.draw.rect(
                fenetre,
                (200, 200, 200) if CARTE[block] == '#' else (100, 100, 100),
                (col * TAILLE_BLOCK, lig * TAILLE_BLOCK, TAILLE_BLOCK - 2, TAILLE_BLOCK - 2)

            )
    pygame.draw.circle(fenetre, (255, 0, 0), (int(player_x), int(player_y)), 8)
    pygame.draw.line(fenetre, (0, 255, 0), (player_x, player_y),
                     (player_x + math.cos(player_angle) * 50, player_y - math.sin(player_angle) * 50), 3)
    pygame.draw.line(fenetre, (0, 255, 0), (player_x, player_y), (
    player_x + math.cos(player_angle - MOITIE_FOV) * 50, player_y - math.sin(player_angle - MOITIE_FOV) * 50), 3)
    pygame.draw.line(fenetre, (0, 255, 0), (player_x, player_y), (
    player_x + math.cos(player_angle + MOITIE_FOV) * 50, player_y - math.sin(player_angle + MOITIE_FOV) * 50), 3)


# Début du code
forward = True
pygame.init()
pygame.mixer.init(channels=2)
HAUTEUR_ECRAN = 480
LARGEUR_ECRAN = HAUTEUR_ECRAN * 2
TAILLE_CARTE = 8
TAILLE_BLOCK = ((LARGEUR_ECRAN / 2) / TAILLE_CARTE)
PROFONDEUR_MAX = int(math.sqrt(2 * ((LARGEUR_ECRAN / 2) ** 2)))
FOV = math.pi / 3
MOITIE_FOV = FOV / 2
# Vous pouvez essayer avec moins de rayons pour voir ce que ça donne
NOMBRE_RAYONS = 120
STEP_ANGLE = FOV / NOMBRE_RAYONS
SCALE = (LARGEUR_ECRAN / 2) / NOMBRE_RAYONS

player_x = (LARGEUR_ECRAN / 2) / 2
player_y = (LARGEUR_ECRAN / 2) / 2
player_angle = math.pi / 2

dessine_texture = False

CARTE = (
    '########'
    '# x ## #'
    '#      #'
    '#    ###'
    '##     #'
    '#   #  #'
    '#   #  #'
    '########'
)

fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("IUT Maze")

# Il vous faudra utiliser votre propre texture
mur_texture = pygame.image.load('texture.png').convert()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    col = int(player_x / TAILLE_BLOCK)
    lig = int(player_y / TAILLE_BLOCK)

    block = lig * TAILLE_CARTE + col
    if CARTE[block] == '#':
        if forward == True:
            player_x -= math.cos(player_angle) * 5
            player_y -= -math.sin(player_angle) * 5
        else:
            player_x += math.cos(player_angle) * 5
            player_y += -math.sin(player_angle) * 5

    pygame.draw.rect(fenetre, (0, 0, 0), (0, 0, HAUTEUR_ECRAN, HAUTEUR_ECRAN))

    pygame.draw.rect(fenetre, (100, 100, 100), (480, HAUTEUR_ECRAN / 2, HAUTEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.draw.rect(fenetre, (200, 200, 200), (480, -HAUTEUR_ECRAN / 2, HAUTEUR_ECRAN, HAUTEUR_ECRAN))


    lance_rayons()
    touches = pygame.key.get_pressed()

    if touches[pygame.K_LEFT]: player_angle += 0.1
    if touches[pygame.K_RIGHT]: player_angle -= 0.1
    if touches[pygame.K_UP]:
        forward = True
        player_x += math.cos(player_angle) * 5
        player_y += -math.sin(player_angle) * 5
    if touches[pygame.K_DOWN]:
        forward = False
        player_x -= math.cos(player_angle) * 5
        player_y -= -math.sin(player_angle) * 5
    for event in pygame.event.get():
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            dessine_texture = not dessine_texture
    clock.tick(60)

    player_pos = (player_x, player_y)

    pygame.display.flip()