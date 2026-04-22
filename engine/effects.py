import pygame
from level.const import *

class PostProcess:
    def __init__(self, game):
        self.game = game
        self.flash_timer = 0
        self.flash_duration = 30 
        self.flash_surface = pygame.Surface((WIDTH, HEIGHT))
        self.flash_surface.fill(WHITE)

    def trigger_sonar_flash(self):
        self.flash_timer = self.flash_duration

    def update(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1

    def draw(self):
        if self.flash_timer > 0:
            alpha = (self.flash_timer / self.flash_duration) * 255
            self.flash_surface.set_alpha(alpha)
            self.game.screen.blit(self.flash_surface, (0, 0))
