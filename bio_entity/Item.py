import pygame
from level.const import *

class Item:
    def __init__(self, game, pos, type='sonar'):
        self.game = game
        self.x, self.y = pos
        self.type = type
        self.picked_up = False

    def update(self):
        dist = ((self.game.player.x - self.x)**2 + (self.game.player.y - self.y)**2)**0.5
        if dist < 0.5:
            self.game.player.inventory[self.type] += 1
            self.picked_up = True

    def draw(self):
        size = 8
        pygame.draw.circle(self.game.screen, 'cyan', (self.x * size, self.y * size), 3)
