import pygame
import math
from level.const import *

class SpriteObject:
    def __init__(self, game, path='assets/textures/enemy.png', pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image_path = path
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 0, 0))
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.health = 100
        self.alive = True
        self.is_enemy = 'enemy' in path

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        image = pygame.transform.scale(self.image, (int(proj_width), int(proj_height)))
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        if 0 < self.screen_x < WIDTH:
            ray_idx = int(self.screen_x // SCALE)
            if 0 <= ray_idx < len(self.game.raycasting.ray_casting_result):
                wall_depth = self.game.raycasting.ray_casting_result[ray_idx][0]
                if self.dist < wall_depth:
                    self.game.screen.blit(image, pos)

    def get_sprite(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        self.dx, self.dy, self.theta = dx, dy, math.atan2(dy, dx)
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0): delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_WIDTH // SCALE + delta_rays) * SCALE
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        self.run_logic()

    def run_logic(self):
        if self.alive and self.is_enemy:
            # Simple chase logic
            dx, dy = self.player.x - self.x, self.player.y - self.y
            dist = math.hypot(dx, dy)
            if 1.0 < dist < 10.0: # Chase if in range
                speed = 0.001 * self.game.delta_time
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed
            
            if dist < 0.6: # Attack range
                self.player.health -= 0.1 * self.game.delta_time
                self.game.effects.trigger_damage_flash()
                if self.player.health <= 0:
                    self.game.state = 0 # Return to menu on death
        
        elif self.alive and not self.is_enemy:
            # Item pickup logic
            dx, dy = self.player.x - self.x, self.player.y - self.y
            dist = math.hypot(dx, dy)
            if dist < 0.5:
                self.alive = False
                if 'item' in self.image_path: # Assuming path is stored
                    self.player.inventory['sonar'] += 1

class SpriteRenderer:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def update(self):
        self.sprites.sort(key=lambda s: s.dist, reverse=True)
        for sprite in self.sprites:
            if sprite.alive:
                sprite.update()
