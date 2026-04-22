#from graph_node import Graph as Vertex
import pygame
from random import randint
from random import choice
from const import map
from const import dim
from const import color

class Spark():
    def __init__(self):
        self.screen = pygame.display.set_mode((dim.WIDTH, dim.HEIGHT))

    def add_frontier_cells(grid, y, x, frontier):
        for dy, dx in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            ny, nx = y + dy, x + dx
            if (
                0 <= ny < dim.ROWS and
                0 <= nx < dim.COLS and
                grid[ny][nx] == 1 and
                (ny, nx) not in frontier
            ):
                frontier.append((ny, nx))

    def draw_grid(self, grid, current=None):
        self.screen.fill(color.WHITE)
        for row in range(dim.ROWS):
            for col in range(dim.COLS):
                if grid[row][col]:
                    color = color.WHITE
                else:
                    pygame.draw.rect(self.screen, color, (col * dim.CELL_SIZE, row * dim.CELL_SIZE, dim.CELL_SIZE, dim.CELL_SIZE))

        if current:
            y, x = current
            pygame.draw.rect(self.screen, color.GREEN, (col * dim.CELL_SIZE, row * dim.CELL_SIZE, dim.CELL_SIZE, dim.CELL_SIZE))

        pygame.display.flip()
    def prim(self):
        grid = [[map.WALL for _ in range(dim.COLS)] for _ in range(dim.ROWS)]

        start_y, start_x = randint(0, dim.ROWS-1), randint(0, dim.COLS-1)
        grid[start_y][start_x] = False

        frontier = []
        self.add_frontier_cells(grid, start_y, start_x, frontier)
        self.draw_grid(grid, (start_y, start_x))

        while frontier:
            for  event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
            current = choice(frontier)
            frontier.remove(current)
            y, x = current

            neighbors = []
            for dy, dx in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < dim.ROWS and 0 <= nx < dim.COLS and grid[ny][nx] == 0:
                    neighbors.append((ny, nx))
            
            if neighbors:
                ny, nx = choice(neighbors)
                grid[y][x] = 0
                grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                self.add_frontier_cells(grid, y, x, frontier)

            self.draw_grid(grid, (y, x))

        return grid