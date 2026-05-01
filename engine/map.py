import pygame
import random
import math
from level.const import *
from engine.sprite_renderer import SpriteObject

class Map:
    def __init__(self, game):
        self.game = game
        self.world_map = {}
        self.visible_map = set()
        # Note: generate_new_map is called by game.new_game()

    def generate_new_map(self):
        self.rows = 10 + self.game.current_level * 2
        self.cols = 10 + self.game.current_level * 2
        
        grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        
        def add_frontier(y, x, frontier):
            for dy, dx in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.rows and 0 <= nx < self.cols and grid[ny][nx] == 1:
                    if (ny, nx) not in frontier:
                        frontier.append((ny, nx))

        start_y, start_x = 1, 1
        grid[start_y][start_x] = 0
        frontier = []
        add_frontier(start_y, start_x, frontier)

        while frontier:
            cy, cx = random.choice(frontier)
            frontier.remove((cy, cx))
            neighbors = []
            for dy, dx in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < self.rows and 0 <= nx < self.cols and grid[ny][nx] == 0:
                    neighbors.append((ny, nx))
            if neighbors:
                ny, nx = random.choice(neighbors)
                grid[cy][cx] = 0
                grid[cy + (ny - cy) // 2][cx + (nx - cx) // 2] = 0
                add_frontier(cy, cx, frontier)

        # Add some rooms to make it more interesting
        for _ in range(self.game.current_level + 2):
            rw, rh = random.randint(2, 3), random.randint(2, 3)
            rx, ry = random.randint(1, self.cols - rw - 1), random.randint(1, self.rows - rh - 1)
            for j in range(ry, ry + rh):
                for i in range(rx, rx + rw):
                    grid[j][i] = 0

        self.world_map = {}
        empty_tiles = []
        for j, row in enumerate(grid):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = (self.game.current_level % 4) + 1
                else:
                    empty_tiles.append((i, j))
        
        self.goal = empty_tiles[-1]
        self.visible_map = set()
        self.spawn_sprites(empty_tiles)

    def spawn_sprites(self, empty_tiles):
        self.game.sprite_renderer.sprites = []
        for _ in range(3):
            pos = random.choice(empty_tiles[5:-1])
            self.game.sprite_renderer.add_sprite(SpriteObject(self.game, path='assets/textures/item.png', pos=(pos[0] + 0.5, pos[1] + 0.5), scale=0.3, shift=0.5))
        for _ in range(self.game.current_level + 2):
            pos = random.choice(empty_tiles[5:-1])
            self.game.sprite_renderer.add_sprite(SpriteObject(self.game, path='assets/textures/enemy.png', pos=(pos[0] + 0.5, pos[1] + 0.5), scale=0.7, shift=0.27))

    def reveal_area(self, center, radius):
        cx, cy = center
        num_rays = 60
        step_angle = math.tau / num_rays
        for i in range(num_rays):
            angle = i * step_angle
            sin_a, cos_a = math.sin(angle), math.cos(angle)
            for dist in range(radius * 10):
                d = dist / 10
                x, y = int(cx + d * cos_a), int(cy + d * sin_a)
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    self.visible_map.add((x, y))
                    if (x, y) in self.world_map: break
                else: break

    def draw(self):
        if not getattr(self.game, 'show_map', False):
            return
            
        # Draw a full screen overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        
        # Calculate size to fit on screen
        size = min(WIDTH // self.cols, HEIGHT // self.rows) - 2
        offset_x = (WIDTH - self.cols * size) // 2
        offset_y = (HEIGHT - self.rows * size) // 2
        
        # Title
        try:
            font = pygame.font.Font('assets/fonts/orbitron.ttf', 40)
        except Exception:
            font = pygame.font.SysFont('consolas', 40, bold=True)
        title = font.render(f'SECTOR {self.game.current_level} MAP [TAB TO CLOSE]', True, 'cyan')
        self.game.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        # Map bounds
        bg_rect = pygame.Rect(offset_x, offset_y, self.cols * size, self.rows * size)
        pygame.draw.rect(self.game.screen, 'cyan', bg_rect, 2) # border

        for j in range(self.rows):
            for i in range(self.cols):
                if (i, j) in self.visible_map:
                    value = self.world_map.get((i, j))
                    if value:
                        color = (0, 150, 200) # Wall (cyan tech look)
                        pygame.draw.rect(self.game.screen, color, (offset_x + i * size, offset_y + j * size, size - 1, size - 1))
                    else:
                        color = (20, 40, 60) # Floor
                        pygame.draw.rect(self.game.screen, color, (offset_x + i * size, offset_y + j * size, size - 1, size - 1))
        
        # Draw goal
        if self.goal in self.visible_map:
            pygame.draw.circle(self.game.screen, 'gold', (offset_x + self.goal[0] * size + size//2, offset_y + self.goal[1] * size + size//2), size//3)

        # Draw player
        px, py = self.game.player.pos
        pygame.draw.circle(self.game.screen, 'green', (offset_x + px * size, offset_y + py * size), size//3)
        pygame.draw.line(self.game.screen, 'green', 
                         (offset_x + px * size, offset_y + py * size),
                         (offset_x + px * size + math.cos(self.game.player.angle) * size,
                          offset_y + py * size + math.sin(self.game.player.angle) * size), 3)
