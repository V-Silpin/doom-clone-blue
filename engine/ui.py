import pygame
import math
from level.const import *

NEON_RED = (255, 50, 50)
DARK_RED = (100, 0, 0)
NEON_GLOW = (200, 20, 20)

class UI:
    def __init__(self, game):
        self.game = game
        # Load custom futuristic font
        try:
            self.font = pygame.font.Font('assets/fonts/orbitron.ttf', 30)
            self.menu_font = pygame.font.Font('assets/fonts/orbitron.ttf', 60)
        except Exception:
            self.font = pygame.font.SysFont('arial', 30, bold=True)
            self.menu_font = pygame.font.SysFont('arial', 60, bold=True)
        self.weapon_texture = self.load_weapon()
        self.hud_panel = self.load_hud_panel()

    def load_weapon(self):
        try:
            img = pygame.image.load('assets/textures/weapon.png').convert_alpha()
            return pygame.transform.scale(img, (512, 512))
        except:
            return pygame.Surface((512, 512))

    def load_hud_panel(self):
        try:
            img = pygame.image.load('assets/textures/hud_panel.png').convert_alpha()
            return pygame.transform.scale(img, (WIDTH, 150))
        except:
            surf = pygame.Surface((WIDTH, 150))
            surf.fill(BLACK)
            return surf

    def draw_neon_text(self, text, font, color, pos, glow_color=NEON_GLOW, glow_radius=2, center=False):
        surf_text = font.render(text, True, color)
        
        if center:
            pos = (pos[0] - surf_text.get_width() // 2, pos[1] - surf_text.get_height() // 2)

        # Glow effect
        for dx in range(-glow_radius, glow_radius + 1):
            for dy in range(-glow_radius, glow_radius + 1):
                if dx == 0 and dy == 0: continue
                glow_surf = font.render(text, True, glow_color)
                glow_surf.set_alpha(100)
                self.game.screen.blit(glow_surf, (pos[0] + dx * 2, pos[1] + dy * 2))
                
        self.game.screen.blit(surf_text, pos)

    def draw_weapon(self):
        # Weapon bobbing
        bob_offset = 0
        if any(pygame.key.get_pressed()[k] for k in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)):
            bob_offset = math.sin(pygame.time.get_ticks() * 0.01) * 5
        
        # Recoil
        recoil_offset = 0
        if getattr(self.game.player, 'shot', False):
            recoil_offset = 30 # Simple kickback
            
        self.game.screen.blit(self.weapon_texture, (WIDTH // 2 - 256, HEIGHT - 512 + bob_offset + recoil_offset))

    def draw_crosshair(self):
        center = (WIDTH // 2, HEIGHT // 2)
        # Tron neon red crosshair
        pygame.draw.circle(self.game.screen, DARK_RED, center, 10, 2)
        pygame.draw.circle(self.game.screen, NEON_RED, center, 10, 1)
        
        # Center dot
        pygame.draw.circle(self.game.screen, NEON_RED, center, 2)
        
        # Outer brackets
        offset = 15
        length = 8
        pygame.draw.line(self.game.screen, NEON_RED, (center[0] - offset, center[1]), (center[0] - offset - length, center[1]), 2)
        pygame.draw.line(self.game.screen, NEON_RED, (center[0] + offset, center[1]), (center[0] + offset + length, center[1]), 2)
        pygame.draw.line(self.game.screen, NEON_RED, (center[0], center[1] - offset), (center[0], center[1] - offset - length), 2)
        pygame.draw.line(self.game.screen, NEON_RED, (center[0], center[1] + offset), (center[0], center[1] + offset + length), 2)

    def draw_hud(self):
        # The new glossy panel
        hud_height = 150
        panel_y = HEIGHT - hud_height
        self.game.screen.blit(self.hud_panel, (0, panel_y))
        
        # HP Display
        hp_text = f'HP: {int(self.game.player.health)}'
        self.draw_neon_text(hp_text, self.menu_font, NEON_RED, (150, panel_y + 50))
        
        # Ammo Display
        ammo_count = self.game.player.inventory.get("ammo", 0)
        ammo_text = f'AMMO: {ammo_count}'
        self.draw_neon_text(ammo_text, self.menu_font, NEON_RED, (WIDTH // 2 - 100, panel_y + 50))
        
        # Sonar Info
        self.draw_neon_text(f'SONAR: {self.game.player.inventory.get("sonar", 0)}', self.menu_font, NEON_RED, (WIDTH - 350, panel_y + 50))

    def draw_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        
        # Grid background for Tron feel
        for x in range(0, WIDTH, 100):
            pygame.draw.line(self.game.screen, (20, 0, 0), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 100):
            pygame.draw.line(self.game.screen, (20, 0, 0), (0, y), (WIDTH, y), 1)
            
        self.draw_neon_text('DOOM CLONE: NEON PROTOCOL', self.menu_font, NEON_RED, (WIDTH // 2, HEIGHT // 3), center=True)
        
        # Pulsing effect using get_ticks()
        pulse_time = pygame.time.get_ticks()
        alpha_pulse = (math.sin(pulse_time * 0.005) + 1) / 2 # 0 to 1
        pulse_color = (
            max(0, int(NEON_RED[0] * alpha_pulse)), 
            max(0, int(NEON_RED[1] * alpha_pulse)), 
            max(0, int(NEON_RED[2] * alpha_pulse))
        )
        
        self.draw_neon_text('>> PRESS ENTER TO INITIALIZE <<', self.font, pulse_color, (WIDTH // 2, HEIGHT // 2), glow_color=DARK_RED, center=True)

    def draw_win(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        
        # Grid background
        for x in range(0, WIDTH, 100):
            pygame.draw.line(self.game.screen, (20, 0, 0), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 100):
            pygame.draw.line(self.game.screen, (20, 0, 0), (0, y), (WIDTH, y), 1)
            
        self.draw_neon_text('SYSTEM OVERRIDE COMPLETE', self.menu_font, NEON_RED, (WIDTH // 2, HEIGHT // 3), center=True)
        self.draw_neon_text('ALL SECTORS CLEARED', self.font, WHITE, (WIDTH // 2, HEIGHT // 3 + 60), center=True)
        
        pulse_time = pygame.time.get_ticks()
        alpha_pulse = (math.sin(pulse_time * 0.005) + 1) / 2
        pulse_color = (
            max(0, int(NEON_RED[0] * alpha_pulse)), 
            max(0, int(NEON_RED[1] * alpha_pulse)), 
            max(0, int(NEON_RED[2] * alpha_pulse))
        )
        
        self.draw_neon_text('>> PRESS ENTER TO REBOOT <<', self.font, pulse_color, (WIDTH // 2, HEIGHT // 2 + 50), glow_color=DARK_RED, center=True)
