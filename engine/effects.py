import pygame
from level.const import *

class PostProcess:
    def __init__(self, game):
        self.game = game
        self.flash_timer = 0
        self.flash_duration = 30 
        self.flash_surface = pygame.Surface((WIDTH, HEIGHT))
        self.flash_surface.fill(WHITE)
        self.damage_surface = pygame.Surface((WIDTH, HEIGHT))
        self.damage_surface.fill((255, 0, 0))
        self.damage_timer = 0

    def trigger_sonar_flash(self):
        self.flash_timer = self.flash_duration

    def trigger_damage_flash(self):
        self.damage_timer = self.flash_duration

    def update(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.damage_timer > 0:
            self.damage_timer -= 1

    def draw(self):
        if self.flash_timer > 0:
            alpha = (self.flash_timer / self.flash_duration) * 255
            self.flash_surface.set_alpha(alpha)
            self.game.screen.blit(self.flash_surface, (0, 0))
        
        if self.damage_timer > 0:
            alpha = (self.damage_timer / self.flash_duration) * 150
            self.damage_surface.set_alpha(alpha)
            self.game.screen.blit(self.damage_surface, (0, 0))
