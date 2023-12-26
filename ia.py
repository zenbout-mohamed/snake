import pygame
from pygame.locals import *
import time
import random


SIZE = 40  ##La taille de chaque bloc dans la grille du jeu##
BACKGROUND_COLOR = (255, 110, 255)

class Apple: # Représente la pomme que le serpent peut manger.
    def __init__(self, parent_screen): 
        self.parent_screen = parent_screen   #parent_screen : La surface Pygame sur laquelle le serpent est dessiné.
        self.image = pygame.image.load("./resources/apple.jpg").convert() # image : L'image du bloc de serpent.
        self.x = 120 # x, y : Les coordonnées de la pomme sur l'écran.
        self.y = 120




# ------------------------Fonction draw servant à dessiner la pomme à l'écran.-------------------------------
    def draw(self):  
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
        
# -------------------Fonction move déplace la pomme à une position aléatoire sur l'écran.------------------
    def move(self):  
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake: # Représente le serpent dans le jeu.
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("./resources/block.jpg").convert()
        self.direction = 'down' # direction : La direction actuelle dans laquelle le serpent se déplace.

        self.length = 1 # length : La longueur du serpent.
        self.x = [40] # x, y : Listes représentant les coordonnées x et y de chaque bloc du serpent.
        self.y = [40]



#------------------------- Fonctions move_left, move_right, move_up, move_down : Change la direction du serpent.-----------------------------
    def move_left(self): 
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
# -----------------------------Déplace le serpent dans sa direction actuelle.---------------------
    def walk(self): # walk : 
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw() 
# ---------------------Fonction draw permettant de dessiner le serpent à l'écran.-----------------------------
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()
# ---------------------Fonction increase_length permettant d'augmenter la longueur du serpent lorsqu'il mange une pomme.-----------------------------
    def increase_length(self): 
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game: # Représente le jeu dans son ensemble.
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jeu Snake :")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800)) # surface : La surface Pygame représentant la fenêtre du jeu.
        self.snake = Snake(self.surface) # snake : Une instance de la classe Snake.
        self.snake.draw()
        self.apple = Apple(self.surface) # apple : Une instance de la classe Apple.
        self.apple.draw() 
        
# ---------------------Fonction ai_control(self) détermine la prochaine action de l'IA en fonction de l'état actuel du jeu. ---------------------
    def ai_control(self):
        
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        apple_x, apple_y = self.apple.x, self.apple.y
        
        dist_x = apple_x - head_x
        dist_y = apple_y - head_y
        
        if head_x < apple_x:
            self.snake.move_right()
        elif head_x > apple_x:
            self.snake.move_left()
        elif head_y < apple_y:
            self.snake.move_down()
        elif head_y > apple_y:
            self.snake.move_up()
            
        if abs(dist_x) > abs(dist_y):
            if dist_x > 0:
                self.snake.move_right()
            else:
                self.snake.move_left()
        else:
            if dist_y > 0:
                self.snake.move_down()
            else:   
                self.snake.move_up()

# --------------------------Fonction play_background_music : Joue la musique de fond du jeu.------------------------------------
    def play_background_music(self): 
        pygame.mixer.music.load('./resources/sister-sledge.mp3')
        pygame.mixer.music.play(-1, 0)
        
# -----------------------Fonction qui permet de jouer un son (collision ou ding) en fonction de l'entrée.-------------------------------------
    def play_sound(self, sound_name): 
        if sound_name == "crash":
            sound = pygame.mixer.Sound("./resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("./resources/ding.mp3")

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()

#---------------------- Réinitialise le jeu en créant un nouveau serpent et une nouvelle pomme.-----------------------
    def reset(self): 
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

#---------------------- Fonction Collision entre 2 objets-------------------------------------------------------------
    def is_collision(self, x1, y1, x2, y2): 
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
# ----------------------Fonction rendre_background rend l'arrière-plan du jeu.---------------------------
    def render_background(self):  
        bg = pygame.image.load("./resources/golden.jpg")
        self.surface.blit(bg, (0,0))
# ------------------- Fonction play : Gère la logique du jeu, y compris la gestion des collisions et la mise à jour de l'affichage.-----
    def play(self): 
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score() # display_score : Affiche le score actuel à l'écran.
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred" #le mot-clé raise est utilisé pour déclencher délibérément une exception.
            #Lorsqu'une exception est levée, le programme génère une interruption normale de l'exécution du code et recherche le gestionnaire d'exception approprié pour traiter cette exception.

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"
# -------------Fonction permettant d'afficher le score---------------------------------
    def display_score(self):
        font = pygame.font.SysFont('Roboto',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))
        
# ----------------Fonction show_game_over : Affiche l'écran de fin de jeu.-----------------
    def show_game_over(self): 
        self.render_background()
        font = pygame.font.SysFont('Roboto', 30)
        line1 = font.render(f"Fin de la Partie ! Score :{self.snake.length}", True, (0, 100, 255))
        self.surface.blit(line1, (50, 100))
        line2 = font.render("Recommencer? : touche ENTRER, Quitter? touche ESC.", True, (0, 100, 255))
        self.surface.blit(line2, (350, 100))
        pygame.mixer.music.pause()
        pygame.display.flip()
        
# # # Boucle principale du jeu qui gère l'entrée de l'IA et exécute la logique du jeu.# # #
        
    def run(self): 
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
            
                    elif event.type == QUIT:
                        running = False
            try:
                if not pause:
                    # Nous devons appeler la focntion de l'IA pour que ce dernier puisse jouer.
                    self.ai_control()
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
    time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()
# Résumé du fontionnement du projet :

# Le jeu démarre avec un serpent et une pomme.
# La boucle principale du jeu (run) écoute l'entrée de l'IA et met à jour le jeu en conséquence.
# Le serpent se déplace dans la direction spécifiée, et les collisions sont vérifiées.
# Si le serpent mange une pomme, il grandit, et une nouvelle pomme apparaît.
# Si le serpent entre en collision avec lui-même ou avec les limites de la fenêtre, le jeu se termine, et l'écran de fin de jeu est affiché.
