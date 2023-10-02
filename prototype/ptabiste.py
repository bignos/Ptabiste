#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#-------------------------------------------------------------------------------
# Objectif:
# Faire un jeu simple qui n'utilise qu'une entrée utilisateur:
# - Action
# 
# Le type de jeu 'Runner' permet d'avoir cette simplicité d'interaction utilisateur.
#
# - Le joueur représenté par un Personnage est placé au centre de l'écran.
# - Le Personnage court en permanence.
# - Quand l'utilisateur appui  sur Action Le Personnage saute.
# - Le Fond est déplacer en permanence de la droite vers la gauche pour donner
#       l'impression à l'utilisateur que le personnage avance.
# - Le Parcourt contient des Obstacle que le Personnage devra éviter en sautant.
# - Si le Personnage touche un Obstacle, la partie ce termine.
# - Le Parcourt doit avoir des Obstacles placés aléatoirement.
# - Le Parcourt est infinie.
# - Plus la distance parcouru par le Personnage augmente plus la difficulté augmente.
# - La difficulté est augmenté en augmentant la fréquence des obstacles.
# - Le Score dépend uniquement de la distance parcouru par le Personnage.
#
# Déroulement classique d'une partie:
# 1- Écran de titre du jeu
# 2- L'utilisateur appui sur Action
# 3- Lancement de la partie
# 4- Le Personnage à touché un Obstacle
# 5- La partie ce termine
# 6- Écran de score de l'utilisateur
# 7- Retour à l'écran de titre du jeu
# 
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Entités:
#
# - Personnage
# - Joueur
# - Action
# - Fond
# - Parcourt
# - Obstacle
# - Difficulté
# - Distance
# - Score
# - Partie
# - EcranTitre
# - EcranScore
# 
# Relation entre les Entités:
# - Le Personnage est joué par le Joueur
# - L'Action est produite par le Joueur
# - Le Parcourt contient le Fond et les Obstacles
# - La Distance est lié à la Partie
# - La Difficulté est lié à la Partie
# - Le Score est lié au Joueur
# - L'EcranScore dépend du Score
# 
# Entité isolé
# - EcranTitre
#
# Entité abstraite
# - VisuelJeu
#       -> Fond
#       -> Sprite
#           -> Personnage
#           -> Obstacle
# - Ecran
#       -> EcranTitre
#       -> EcranScore
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Taches:
# - Initialiser Pygame                                                      [x]
# - Initier les Entités:                                                    [ ]
#   - VisuelJeu                                                             [ ]
#   - Sprite                                                                [x]
#   - Personnage                                                            [x]
#   - Joueur                                                                [ ]                
#   - Action                                                                [ ]
#   - Fond                                                                  [x]
#   - Parcourt                                                              [ ]
#   - Obstacle                                                              [x]
#   - Difficulté                                                            [x]
#   - Distance                                                              [ ]
#   - Score                                                                 [x]
#   - Partie                                                                [ ]
#   - Ecran                                                                 [ ]
#   - EcranTitre                                                            [x]
#   - EcranScore                                                            [ ]
# - Chercher éléments graphiques                                            [ ]
#   - Personnage avec animation de course                                   [x]
#   - Obstacle                                                              [x]
#   - Fond                                                                  [x]
#   - Sol                                                                   [ ]
# - Chercher éléments sonores                                               [ ]
#   - Musique partie                                                        [x]
#   - Musique EcranTitre                                                    [ ]
#   - Bruitages                                                             [ ]
#       - Lancement de la partie                                            [ ]
#       - Sauter                                                            [x]
#       - Collision avec Obstacle                                           [x]
#       - Fin de Partie                                                     [ ]
#       - Présentation du Score                                             [ ]
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Notes:
# [mercredi 8 mai 2019]
# ---------------------
# * Début du prototype
# ------------------------------------------------------------------------------
# [lundi 27 mai 2019]
# -------------------
# my_event = pygame.event.Event(KEYDOWN, key=K_SPACE, mod=0, unicode=u' ')
# pgame.event.post(my_event)
#
# CATONKEYBOARD = USEREVENT+1
# my_event = pygame.event.Event(CATONKEYBOARD, message="Bad cat!")
# pgame.event.post(my_event)
#
# for event in pygame.event.get():
#   if event.type == CATONKEYBOARD:
#       print(event.message)
# ------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

import random
import pygame
from pygame.locals import *


class Ptabiste:
    """ Class principal du jeu Ptabiste """

    """ Constantes de configuration du prototype """
    CONFIG = {
            'ResolutionWidth'  : 1920,
            'ResolutionHeight' : 1080,
            'DisplayFlags'     : pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME,
            # 'DisplayFlags'     : pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN,
            'ImageFond'        : 'resources/Fond/background.png',
            'SpritePersonnage' : 'resources/Personnage/coolCat.png',
            'SpriteRock'       : 'resources/Obstacles/rock_round.png',
            'SpriteEye'        : 'resources/Obstacles/eyeball.png',
            'SpriteZombie'     : 'resources/Obstacles/zombie.png',
            'Music'            : 'resources/Musique/happy.mp3',
            'SonSauter'        : 'resources/Bruitages/sauter.ogg',
            'SonCollision'     : 'resources/Bruitages/ghost.ogg',
            # 'SonCollision'     : 'resources/Bruitages/explosion.ogg',
            'ScrollingSpeed'   : 10,
            'FondY'            : -464
            }

    OPTION = {
            'Music' : True
            }

    def __init__(self):
        self._running       = False
        self._screen        = None
        self.width          = self.CONFIG['ResolutionWidth']
        self.height         = self.CONFIG['ResolutionHeight']
        self.size           = self.width, self.height
        self.offscreen      = pygame.Surface(self.size)
        self.scrollingSpeed = self.CONFIG['ScrollingSpeed']
        self.next           = ''
        self._grayscaled    = False

    def start(self):
        self._load_resources()
        if self._init() == False:
            self._quit()

        while( self._running ):
            for event in pygame.event.get():
                self._on_event(event)
            if not self.personnage.isDead():
                self._logic()
                self._render()
        self._cleanup()

    # Private
    def _load_resources(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.CONFIG['Music'])

    def _init(self):
        pygame.init()
        self._screen                = pygame.display.set_mode(self.size, self.CONFIG['DisplayFlags'])
        self._running               = True
        self._clock                 = pygame.time.Clock()

        self._joystickInitialisation()

        if self.OPTION['Music']:
            pygame.mixer.music.play(-1)

        self.fond       = Fond()
        self.personnage = Personnage(self._screen.get_width()//3, 2*self._screen.get_height()//3)

        rock            = Rock(self._screen.get_width(), 2*self._screen.get_height()//3)
        eye             = Eye(self._screen.get_width()*2, (2*self._screen.get_height()//3)-30)
        zombie          = Zombie(self._screen.get_width()*2, (2*self._screen.get_height()//3)-160)
        self.generator  = ObstacleGenerator([rock, eye, zombie], max_active=1)

        self.score      = Score()
        self.difficulty = Difficulty()

        self._renderOffscreen()
        self._fadeIn()


    def _on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._quit()
            if event.key:
                self.personnage.actionSauter()
        if event.type == pygame.JOYBUTTONDOWN:
            self.personnage.actionSauter()
        if event.type == pygame.QUIT:
            self._quit()

    def _logic(self):
        self.fond.update(self.difficulty)
        self.personnage.update()
        self.generator.update(self.difficulty)
        self.score.update()

        if (self.score.counter % 100) == 0:
            self.difficulty.increase()

        if self.generator.isCollision(self.personnage):
            self.personnage.actionMourir()

        if self.personnage.isDead() and not self._grayscaled:
            self._grayscaled = True
            pygame.mixer.music.stop()
            self.offscreen.blit(Tools.convertToGray(self.offscreen), (0,0))
            self._fadeOut()
            self.next = 'MENU'
            self._running = False


    def _render(self):
        if not self.personnage.isDead():
            self._renderOffscreen()
        self._screen.blit(self.offscreen, (0,0))

        self._clock.tick(30)

        pygame.display.flip()

    def _renderOffscreen(self):
        self.offscreen.fill([0,0,0])
        self.fond.render(self.offscreen) 
        self.personnage.render(self.offscreen)
        self.generator.render(self.offscreen)
        self.score.render(self.offscreen)

    def _fadeIn(self):
        for alpha in range(0,255,2):
            self.offscreen.set_alpha(alpha)
            self._screen.fill([0,0,0])
            self._screen.blit(self.offscreen, (0,0))
            pygame.display.flip()

    def _fadeOut(self):
        for alpha in range(255,0,-2):
            self.offscreen.set_alpha(alpha)
            self._screen.fill([0,0,0])
            self._screen.blit(self.offscreen, (0,0))
            pygame.display.flip()

    def _joystickInitialisation(self):
        if not pygame.joystick.get_init(): 
            pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()

    def _joystickCleanup(self):
        for joystick in self.joysticks:
            joystick.quit()
        pygame.joystick.quit()

    def _cleanup(self):
        pygame.mixer.quit()
        if self.next == 'EXIT':
            self._joystickCleanup()
            pygame.quit()

    def _quit(self):
        self._running = False
        self.next = 'EXIT'


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, increment):
        """
        increment tuple (increment x, increment y)
        return a tuple
        """
        self.x = self.x + increment[0]
        self.y = self.y + increment[1]

    def get(self):
        return (self.x, self.y)

class Fond:

    def __init__(self):
        self.image          = pygame.image.load(Ptabiste.CONFIG['ImageFond']).convert()
        self.position       = Position(0,Ptabiste.CONFIG['FondY'])
        self.positionClone  = Position(self.image.get_width(),Ptabiste.CONFIG['FondY'])
        self.scrollingSpeed = Ptabiste.CONFIG['ScrollingSpeed']
        self.InitialScrollingSpeed = self.scrollingSpeed

    def update(self, difficulty):
        self.scrollingSpeed = self.InitialScrollingSpeed + (difficulty.get() // 5)
        if self.position.x < -self.image.get_width():
            self.position.x = (self.positionClone.x - self.scrollingSpeed) + self.image.get_width()
        else:
            self.position.move((-self.scrollingSpeed, 0))

        if self.positionClone.x < -self.image.get_width():
            self.positionClone.x = (self.position.x - self.scrollingSpeed) + self.image.get_width()
        else:
            self.positionClone.move((-self.scrollingSpeed, 0))


    def render(self,surface):
        surface.blit(self.image, self.position.get())
        surface.blit(self.image, self.positionClone.get())

class Score:

    def __init__(self, x=0, y=0):
        self.score    = 0
        self.counter  = 0
        self.text     = 'Score:'
        self.message  = self._generateMessage()
        self.fontSize = 60
        self.position = Position(x,y)
        self.font     = None
        if pygame.font.get_init():
            self.font = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        else:
            raise Exception('pygame.font not initialized')

    def get(self):
        return self.score

    def update(self):
        if(self.counter % 10) == 0:
            self.score += 1
            self.message = self._generateMessage()
        self.counter += 1

    def render(self, surface):
        textSurface = self.font.render(self.message, True, [255,0,0])
        surface.blit(textSurface, self.position.get())

    def _generateMessage(self):
        return '{} {}'.format(self.text, self.score)

class Difficulty:

    def __init__(self, initial_difficuty=1):
        self.difficuty = initial_difficuty

    def increase(self):
        self.difficuty += 1

    def get(self):
        return self.difficuty


class Sprite:

    def __init__(self, sprite_image_path, column, line, x=0, y=0, zoom=1, slow=1, invert=False, linear=False):
        self.position      = Position(x,y)
        self.column        = column
        self.line          = line
        self.image         = pygame.transform.rotozoom(pygame.image.load(sprite_image_path), 0, zoom).convert_alpha()
        if invert:
            self.image     = pygame.transform.flip(self.image, True, False)
        self.linear        = linear
        self.decalWidth    = self.image.get_width()//column
        self.decalHeight   = self.image.get_height()//line
        self.rect          = pygame.rect.Rect(0,0,self.decalWidth,self.decalHeight)
        self.slow          = slow
        self.mask          = pygame.mask.from_surface(self.getRealSurface())

        self._slow_counter = 0

        self.loopDecrement = 1

    def nextImage(self):        
        if (self._slow_counter % self.slow) == 0:
            if self.linear:
                self.processNextImageLinear()
            else:
                self.processNextImageReverse()
        self._slow_counter += 1
        if self._slow_counter > 1000 * self.slow:
            self._slow_counter = 0

    def processNextImageReverse(self):
        if ((self.loopDecrement == 1) and (self.rect.x < self.decalWidth * (self.column-1))) \
                or ((self.loopDecrement == -1) and (self.rect.x > 0)):
                    self.rect.x += self.decalWidth * self.loopDecrement
        else:
            self.rect.y += self.decalHeight * self.loopDecrement
            self.rect.x = 0 if self.loopDecrement == 1 else (self.decalWidth * (self.column-1))

        if self.line > 1:
            if (self.loopDecrement == 1)  and (self.rect.y == self.decalHeight * (self.line-1)):
                self.rect.x = (self.decalWidth * (self.column-1))
                self.loopDecrement = -1
            if (self.loopDecrement == -1) and (self.rect.y == 0):
                self.rect.x = 0
                self.loopDecrement = 1
        else:
            if (self.loopDecrement == 1) and (self.rect.x == self.decalWidth * (self.column-1)):
                self.loopDecrement = -1
            if (self.loopDecrement == -1) and (self.rect.x == 0):
                self.loopDecrement = 1

    def processNextImageLinear(self):
        if self.rect.x < self.decalWidth * (self.column-1): 
            self.rect.x += self.decalWidth
        else:
            if self.rect.y < self.decalHeight * (self.line-1):
                self.rect.y += self.decalHeight
            else:
                self.rect.y = 0
            self.rect.x = 0

    def setImage(self, tab_x, tab_y):
        self.rect.x = self.decalWidth  * tab_x
        self.rect.y = self.decalHeight * tab_y

    def render(self, surface):
        # pygame.draw.rect(surface, (255,0,0), self.getRealRect(), 1) # Visual debug
        if (self.position.x < surface.get_width()) and\
                (self.position.x > -self.rect.w) and\
                (self.position.y < surface.get_height()) and\
                (self.position.y > -self.rect.h):
                    surface.blit(self.image, self.position.get(), self.rect)

    def getRealRect(self):
        return pygame.rect.Rect(self.position.x, self.position.y, self.rect.w, self.rect.h)

    def getRealSurface(self):
        return self.image.subsurface(self.rect)

    def isCollision(self, otherSprite):
        rectSelf  = self.getRealRect()
        rectOther = otherSprite.getRealRect() 
        if rectSelf.colliderect(rectOther):
            offset = (otherSprite.position.x - self.position.x, \
                    otherSprite.position.y - self.position.y)
            if self.mask.overlap(otherSprite.mask,offset):
                return True
        return False



class Personnage(Sprite):

    def __init__(self, x, y):
        super().__init__(Ptabiste.CONFIG['SpritePersonnage'], 1,6, x,y, slow=5)
        self.jumpHeight   = 450
        self.jumpSpeed    = 50
        self.sonSauter    = pygame.mixer.Sound(Ptabiste.CONFIG['SonSauter'])
        self.sonCollision = pygame.mixer.Sound(Ptabiste.CONFIG['SonCollision'])
        self.force        = 21
        self.mass         = 1

        self._dead        = False
        self._jumpPhase   = False
        self._deadPhase   = False

        self._angle       = 0
        self._force       = self.force

    def update(self):
        if self._deadPhase:
            self.phaseMourir()
        elif self._jumpPhase:
            self.phaseSauter()
        else:
            self.phaseCourse()

    def phaseCourse(self):
        self.nextImage()

    def phaseSauter(self):
        if self._jumpPhase:
            signe = 1 if self._force > 0 else -1
            F = signe * int(( 0.1 * self.mass * (self._force*self._force) ))
            self.position.move((0,-F))
            self._force -= 1

            if self.position.y >= self._initialPosition.y:
                self.position.y = self._initialPosition.y
                self._force = self.force 
                self._jumpPhase = False

    def phaseMourir(self):
        if not self.isDead():
            self.position.x -= 25
            self.position.y -= 16
            self._angle -= 20
            if self._angle > 360:
                self._angle = 0
            if self.position.x < -self.rect.w:
                self._dead = True

    def actionSauter(self):
        if not self._jumpPhase and not self._deadPhase:
            self.sonSauter.play()
            self.setImage(0,2)
            self._initialPosition = Position(self.position.x, self.position.y)
            self._jumpPhase       = True

    def actionMourir(self):
        if not self._deadPhase:
            self.sonCollision.play()
            self._deadPhase = True

    def isDead(self):
        return self._dead

    def render(self, surface):
        if self._deadPhase:
            rotateSprite = pygame.transform.rotate(self.getRealSurface(), self._angle)
            surface.blit(rotateSprite, self.position.get())
        else:
            super().render(surface)


class Obstacle(Sprite):

    def __init__(self, sprite_image_path, column, line, x=0, y=0, zoom=1, slow=1, invert=False, linear=False):
        super().__init__(sprite_image_path, column, line, x, y, zoom, slow, invert, linear)
        self.speed = Ptabiste.CONFIG['ScrollingSpeed']
        self.initialSpeed = self.speed
        self.active = False

    def update(self, difficulty):
        if self.active:
            if (self.position.x > (-self.rect.w)):
                self.position.x -= self.speed + (self.speed//2)
                self.nextImage()
            else:
                self.active = False

    def generate(self, difficulty):
        self.active = True
        random.seed()
        randVariation = random.randint(1, 2000)
        self.position.x = Ptabiste.CONFIG['ResolutionWidth'] + randVariation
        self.speed = self.initialSpeed + (difficulty.get()//4) + random.randint(-5,5) 
        if self.speed <= 7: 
                self.speed = 8 


class Rock(Obstacle):
    
    def __init__(self, x, y):
        super().__init__(Ptabiste.CONFIG['SpriteRock'],4,3, x, y,zoom=5, slow=6)


class Eye(Obstacle):
    
    def __init__(self, x, y):
        super().__init__(Ptabiste.CONFIG['SpriteEye'],4,1, x, y,zoom=3, slow=6, invert=True)

class Zombie(Obstacle):
    
    def __init__(self, x, y):
        super().__init__(Ptabiste.CONFIG['SpriteZombie'],1,10, x, y,zoom=1, slow=6, linear=True)

class ObstacleGenerator():
    
    def __init__(self, obstacles=[], max_active=1):
        self.obstacles = obstacles
        self.max_active = max_active

    def add(self, obstacle):
        self.obstacles.append(obstacles)

    def update(self, difficulty):
        if self.getActives() < self.max_active:
            self.generate(difficulty)

        [obstacle.update(difficulty) for obstacle in self.obstacles]

    def render(self, surface):
        [obstacle.render(surface) for obstacle in self.obstacles if obstacle.active]

    def generate(self, difficulty):
        no_active_index = [index for index, obstacle in enumerate(self.obstacles) if not obstacle.active]
        if len(no_active_index) > 1:
            randIndex = no_active_index[random.randint(0, len(no_active_index) - 1)]
        else:
            randIndex = no_active_index[0]

        self.obstacles[randIndex].generate(difficulty)

    def getActives(self):
        return len([True for obstacle in self.obstacles if obstacle.active])

    def isCollision(self, sprite):
        for obstacle in self.obstacles:
            if obstacle.active:
                if sprite.isCollision(obstacle):
                    return True


class Tools:

    def convertToGray(surface):
        width, height = surface.get_size()
        pixels = pygame.PixelArray(surface)
        for x in range(width):
            for y in range(height):
                color       = pygame.Color(pixels[x,y])
                average     = (color.r + color.g + color.b) // 3
                pixels[x,y] = (average, average, average)
        return pixels.make_surface()




# -[ Main ]-
if __name__ == '__main__':
    ptabiste = Ptabiste()
    ptabiste.start()

