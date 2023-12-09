import inspect
import time
import pygame
import math
import sys


class Engine:

    def __init__(self):
        self.player_pos = None
        self.startBTN = None
        self.hauteur_screen = 480*2
        self.largeur_screen = self.hauteur_screen
        self.taille_carte = 9
        self.taille_block: int = self.largeur_screen // self.taille_carte
        self.profondeur_max = int(math.sqrt(2 * ((self.largeur_screen / 2) ** 2)))
        self.fov = math.pi / 3
        self.forward = True
        self.moitie_fov = self.fov / 2
        self.nombre_rayons = 120
        self.scale = (self.largeur_screen / 2) / self.nombre_rayons
        self.step_angle = self.fov / self.nombre_rayons
        self.scale = self.largeur_screen / self.nombre_rayons
        self.clock = pygame.time.Clock()
        self.player_x = (self.largeur_screen // 2)
        self.player_y = (self.largeur_screen // 2)
        self.player_angle = math.pi / 2
        self.carte = (
            '#########'
            '#  ## X #'
            '#       #'
            '#     ###'
            '##      #'
            '#   #   #'
            '#   #   #'
            '#       #'
            '#########'
        )

        self.dessine_texture = False
        self.game = None
        self.init_background = None
        pygame.init()
        pygame.mixer.init()
        self.game = pygame.display.set_mode((self.largeur_screen, self.hauteur_screen))
        pygame.display.set_caption("IUT Maze")
        self.sound = pygame.mixer.Sound('ressource/song.mp3')
        self.channel = pygame.mixer.find_channel()
        self.homeScreen()
        self.game_started = False
        self.game_background = pygame.image.load('ressource/desktop.jpeg').convert()
        self.start()

    def homeScreen(self):
        self.init_background = pygame.image.load('ressource/background.png').convert()
        self.game.blit(self.init_background, (0, 0))

        font = pygame.font.Font('Inter.ttf', 150)
        font.set_bold(True)
        Title = font.render('IUT MAZE', True, (72, 202, 228))
        self.game.blit(Title, (self.largeur_screen / 2 - Title.get_width() / 2, 100))

        pygame.draw.rect(self.game, (255, 255, 255),
                         (self.largeur_screen / 2 - 100, self.hauteur_screen - 200, 200, 100))
        font = pygame.font.Font('Inter.ttf', 50)
        font.set_bold(True)
        self.startBTN = font.render('START', True, (0, 0, 0))
        self.game.blit(self.startBTN, (self.largeur_screen / 2 - 80, self.hauteur_screen - 180))

    def keyEvent(self):
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT]: self.player_angle += 0.1
        if touches[pygame.K_RIGHT]: self.player_angle -= 0.1
        if touches[pygame.K_UP]:
            forward = True
            self.player_x += math.cos(self.player_angle) * 5
            self.player_y += -math.sin(self.player_angle) * 5
        if touches[pygame.K_DOWN]:
            forward = False
            self.player_x -= math.cos(self.player_angle) * 5
            self.player_y -= -math.sin(self.player_angle) * 5

    def hitWall(self):
        col = int(self.player_x / self.taille_block)
        lig = int(self.player_y / self.taille_block)
        block = lig * self.taille_carte + col

        if self.carte[block] == '#':
            if self.forward:
                self.player_x -= math.cos(self.player_angle) * 5
                self.player_y -= -math.sin(self.player_angle) * 5
            else:
                self.player_x += math.cos(self.player_angle) * 5
                self.player_y += -math.sin(self.player_angle) * 5
    @staticmethod
    def point_dans_triangle(x, y, x1, y1, x2, y2, x3, y3):
        detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / detT
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / detT
        gamma = 1 - alpha - beta

        return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1

    @staticmethod
    def split_string_by_length(input_string, chunk_length):
        return [input_string[i:i + chunk_length] for i in range(0, len(input_string), chunk_length)]

    def startGame(self):
        print("game started")
        self.time = time.time()
        self.channel.play(self.sound, -1)
        self.game_started = True
        self.game.fill((255, 255, 255))
        pygame.display.update()

    def position_relative(self, objectA, objectB,angle_a):
        x_a, y_a = objectA
        x_b, y_b = objectB

        angle_a_rad = angle_a

        # Calcul des coordonnées transformées par rapport à l'angle de regard de l'objet A
        x_a_transforme = (x_a - x_a) * math.cos(angle_a_rad) - (y_a - y_a) * math.sin(angle_a_rad) + x_a
        x_b_transforme = (x_b - x_a) * math.cos(angle_a_rad) - (y_b - y_a) * math.sin(angle_a_rad) + x_a

        if x_a_transforme < x_b_transforme:
            return "D"
        elif x_a_transforme > x_b_transforme:
            return "G"
        else:
            return "M"


    def getSound(self):
        index_x = self.carte.index('X')
        taille_cote = int(len(self.carte) ** 0.5)
        ligne, colonne = divmod(index_x, taille_cote)
        ligne *= 8
        colonne *= 8
        distance = math.sqrt((self.player_x - colonne) ** 2 + (self.player_y - ligne) ** 2)
        volume = math.exp(-0.001 * distance)
        self.channel.set_volume(volume, 0)
        direction = self.position_relative((self.player_x, self.player_y), (colonne, ligne), self.player_angle)
        print(direction)
        if direction == "D":
            print(volume%1, volume*0.8%1)
            self.channel.set_volume(volume%1, volume*0.8%1)
        elif direction == "G":
            print(volume*0.8%1, volume%1)
            self.channel.set_volume(volume*0.8%1, volume%1)
        print(distance)
        if distance < 200:
            self.channel.set_volume(0, 0)
            self.channel.stop()
            print("You win")
            print(f"Time : {round(time.time() - self.time, 2)}s")
            sys.exit(0)

    def rayons(self):
        angle_depart = self.player_angle + self.moitie_fov
        cible_x = 0.0
        cible_y = 0.0
        profondeur = 0.0
        for ray in range(self.nombre_rayons):
            for profondeur in range(self.profondeur_max):
                cible_x = self.player_x + math.cos(angle_depart) * profondeur
                cible_y = self.player_y - math.sin(angle_depart) * profondeur

                col = int(cible_x / self.taille_block)
                lig = int(cible_y / self.taille_block)
                tb = self.taille_block
                block = lig * self.taille_carte + col
                if self.carte[block] == '#':
                    est_horizontal = not (
                            (
                                self.point_dans_triangle(
                                    cible_x,
                                    cible_y,
                                    (col * tb),
                                    (lig * tb),
                                    (col * tb),
                                    ((lig * tb) + tb),
                                    (col * tb) + tb / 2,
                                    (lig * tb) + tb / 2)
                            ) or (
                                self.point_dans_triangle(
                                    cible_x,
                                    cible_y,
                                    ((col * tb) + tb / 2),
                                    ((lig * tb) + tb / 2),
                                    ((col * tb) + tb),
                                    (lig * tb),
                                    (col * tb) + tb,
                                    (lig * tb) + tb)
                            ))
                    couleur = 100 / (1 + profondeur * profondeur * 0.0001)
                    profondeur *= math.cos(self.player_angle - angle_depart)
                    hauteur_mur = 41000 / (profondeur + 0.0001)
                    if hauteur_mur > self.hauteur_screen:
                        hauteur_mur = self.hauteur_screen
                    if est_horizontal:
                        pygame.draw.rect(self.game, (couleur, 0, 0), (
                            ray * self.scale, (self.hauteur_screen /2) - hauteur_mur /2,
                            self.scale, hauteur_mur))
                    else:
                        pygame.draw.rect(self.game, (0, couleur, 0), (
                            ray * self.scale, (self.hauteur_screen / 2) - hauteur_mur / 2,
                            self.scale, hauteur_mur))
                    break
            angle_depart -= self.step_angle



    def start(self):
        while True:
            if self.game_started:
                self.game.blit(self.game_background, (0, 0))
                pygame.draw.rect(self.game, (15, 15, 15), (0, self.hauteur_screen / 2, self.largeur_screen, self.hauteur_screen / 2))
                self.hitWall()
                self.keyEvent()
                self.rayons()
                self.getSound()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.startBTN.get_rect(
                            topleft=(self.largeur_screen / 2 - 100, self.hauteur_screen - 200)).collidepoint(event.pos):
                        self.game_started = True
                        self.startGame()

            self.clock.tick(60)
            self.player_pos = (self.player_x, self.player_y)
            pygame.display.flip()


if __name__ == '__main__':
    engine = Engine()
