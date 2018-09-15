#! /usr/bin/env python3
# encoding: utf-8

import pygame
from pygame.locals import *
from importlib import reload

#from games.colorFlood import Game
#from games.untangle import Game
#from motherload import Game
import motherload

class Launcher:

    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        self._running = True
        self._clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Motherload')
        self._display_surf = pygame.display.set_mode(
                (self.windowWidth, self.windowHeight),
                pygame.HWSURFACE)
        self._running = True

        self.loadGame()

    def loadGame(self):
        try:
            reload(motherload)
            self.game = motherload.Game((self.windowWidth, self.windowHeight))
        except Exception as e:
            print (e)
            raise

    def event(self, event):
        if event.type == QUIT:
            self._running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False

            if event.key == pygame.K_F5:
                self.loadGame()

        self.game.gameEvent(event)

    def loop(self):
        self.game.gameLoop()

        if self.game.getRunningState() == False:
            self._running = False

    def draw(self):
        self._display_surf.fill((0,0,0))
        self.game.draw(self._display_surf)
        pygame.display.flip()
        # print (self._clock.get_fps())

    def exit(self):
        pygame.quit()

    def run(self):
        try:
            while( self._running ):
                for event in pygame.event.get():
                    self.event(event)

                self.loop()
                self.draw()

                self._clock.tick(30)
        except KeyboardInterrupt:
            self._running = False
        self.exit()

if __name__ == "__main__" :
    print ('\nAll graphics are from https://itch.io/game-assets \n'\
    'See the source to find the links.\n'\
    'Thanks to original authors\n')
    theApp = Launcher()
    theApp.run()
