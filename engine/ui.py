import pygame
from level.const import *

class UI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.menu_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.weapon_texture = self.load_weapon()

    def load_weapon(self):
        try:
            img = pygame.image.load('assets/textures/weapon.png').convert_alpha()
            return pygame.transform.scale(img, (512, 512))
        except:
            return pygame.Surface((512, 512))

    def draw_weapon(self):
        self.game.screen.blit(self.weapon_texture, (WIDTH // 2 - 256, HEIGHT - 512))

    def draw_hud(self):
        health_text = self.font.render(f'HEALTH: {self.game.player.health}', True, RED)
        self.game.screen.blit(health_text, (20, HEIGHT - 50))
        level_text = self.font.render(f'LEVEL: {self.game.current_level}', True, WHITE)
        self.game.screen.blit(level_text, (WIDTH // 2 - 50, HEIGHT - 50))
        sonar_text = self.font.render(f'SONAR: {self.game.player.inventory["sonar"]}', True, CYAN)
        self.game.screen.blit(sonar_text, (WIDTH - 180, HEIGHT - 50))

    def draw_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        title_text = self.menu_font.render('DOOM CLONE BLUE', True, BLUE)
        self.game.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        start_text = self.font.render('PRESS ENTER TO START', True, WHITE)
        self.game.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    def draw_win(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        win_text = self.menu_font.render('YOU CONQUERED ALL LEVELS!', True, GREEN)
        self.game.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
        restart_text = self.font.render('PRESS ENTER TO REPLAY', True, WHITE)
        self.game.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
