#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class StartScreen: 
    """ Classe de l'écran de démarage pour le jeu Ptabiste
    """

    """ Constantes de configuration du prototype """
    CONFIG = {
            'ResolutionWidth'  : 1920,
            'ResolutionHeight' : 1080,
            'DisplayFlags'     : pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME,
            'Music'            : 'resources/Musique/happy.mp3',
            'ImageFond'        : 'resources/Fond/sunrise.png',
            'ScrollingSpeed'   : 2,
            'FondY'            : -400,
            'Titre'            : 'resources/Titre/Ptabiste.png'
            }

    OPTION = {
            'Music' : False
            }

    def __init__(self):
        self._running       = False
        self._screen        = None
        self.width          = self.CONFIG['ResolutionWidth']
        self.height         = self.CONFIG['ResolutionHeight']
        self.size           = self.width, self.height
        self.offscreen      = pygame.Surface(self.size)
        self.next           = ''

    def start(self):
        self._load_resources()
        if self._init() == False:
            self._quit()

        while( self._running ):
            for event in pygame.event.get():
                self._on_event(event)
            self._logic()
            self._render()
        self._cleanup()
        return self.next


    # Private
    def _load_resources(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.CONFIG['Music'])

    def _init(self):
        pygame.init()
        self._screen  = pygame.display.set_mode(self.size, self.CONFIG['DisplayFlags'])
        self._running = True
        self._clock   = pygame.time.Clock()
        self._joystickInitialisation()

        if self.OPTION['Music']:
            pygame.mixer.music.play(-1)

        self.fond     = Fond()

        self.titre    = Titre() 

        self._renderOffscreen()
        self._fadeIn()


    def _on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._quit()
            elif event.key:
                self._play()
        if event.type == pygame.JOYBUTTONDOWN:
            self._play()
        if event.type == pygame.QUIT:
            self._quit()

    def _logic(self):
        self.fond.update()
        self.titre.update()

    def _render(self):
        self._renderOffscreen()
        self._screen.blit(self.offscreen, (0,0))

        self._clock.tick(30)

        pygame.display.flip()

    def _renderOffscreen(self):
        self.offscreen.fill([0,0,0])
        self.fond.render(self.offscreen)
        self.titre.render(self.offscreen)


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
        if not self.next == 'GAME':
            self._joystickCleanup()
            pygame.quit()

    def _quit(self):
        self.next = 'EXIT'
        self._running = False

    def _play(self):
        self._fadeOut()
        self.next = 'GAME'
        self._running = False

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

    def __init__(self, flip=True):
        self.image          = pygame.image.load(StartScreen.CONFIG['ImageFond']).convert()
        if flip:
            self.imageClone = pygame.transform.flip(self.image, True, False)
        else:
            self.imageClone = self.image
        self.position       = Position(0,StartScreen.CONFIG['FondY'])
        self.positionClone  = Position(self.image.get_width(),StartScreen.CONFIG['FondY'])
        self.scrollingSpeed = StartScreen.CONFIG['ScrollingSpeed']
        self.InitialScrollingSpeed = self.scrollingSpeed

    def update(self):
        self.scrollingSpeed = self.InitialScrollingSpeed
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
        surface.blit(self.imageClone, self.positionClone.get())

class Titre:
    def __init__(self):
        imagePath                  = StartScreen.CONFIG['Titre']
        self.image                 = pygame.transform.rotozoom(pygame.image.load(imagePath), 0, 3).convert_alpha()
        self.rect                  = self.image.get_rect()
        self.rect.centerx          = StartScreen.CONFIG['ResolutionWidth'] // 2
        self.rect.centery          = StartScreen.CONFIG['ResolutionHeight'] // 2

        self.text                  = 'Appuyer sur un bouton'
        self.textColor             = pygame.Color(255, 255, 255, 255)
        self.fontSize              = 60
        self.font                  = None
        if pygame.font.get_init():
            self.font              = pygame.font.Font(pygame.font.get_default_font(),self.fontSize)
        else:
            raise Exception('pygame.font not initialized')
        self.textSurface      = self.font.render(self.text, True, self.textColor)
        self.rectText         = self.textSurface.get_rect()
        self.rectText.top     = self.rect.bottom + 100
        self.rectText.centerx = self.rect.centerx

        self._vitesseVariation = 2
        self._variation = -1

    def update(self):
        try:
            self.textColor.a += (self._vitesseVariation * self._variation)
        except ValueError:
            tmp_value = self.textColor.a + (self._vitesseVariation * self._variation)

            if tmp_value > 255:
                self._variation = -1
                self.textColor.a = 255

            if tmp_value < 0:
                self._variation = 1
                self.textColor.a = 0

        self.textColor.r = self.textColor.a
        self.textColor.g = self.textColor.a
        self.textColor.b = self.textColor.a

        self.textSurface = self.font.render(self.text, True, self.textColor).convert_alpha()

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        surface.blit(self.textSurface,(self.rectText.x, self.rectText.y))

# -[ Main ]-
if __name__ == '__main__':
    startScreen = StartScreen()
    startScreen.start()
