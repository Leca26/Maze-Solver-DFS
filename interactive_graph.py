import pygame
from random import choice
from pygame import mixer
from collections import defaultdict, deque

#defining screen variables
RES = WIDTH, HEIGHT = 1000, 800
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

#initialize pygame
pygame.init()
pygame.mixer.init()
WOW = pygame.mixer.Sound("WOW.mp3")
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
FPS = 30

#defining algorithms
def DFS_path(graph, start, end):
    '''Takes in a graph, start, and end node, and returns the shortest path between the two nodes if it exists through DFS'''
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        cell = path[-1]
        
        if cell == end:
            return path
        
        if cell not in visited:
            visited.add(cell)
            for neighbor in graph[cell]:
                if neighbor not in visited:
                    stack.append(path + [neighbor])
    return []

def BFS_path(graph, start, end):
    '''Takes in a graph, start, and end node, and returns the shortest path between the two nodes if it exists through BFS'''
    queue = deque([[start]])
    visited = set()
    
    while queue:
        path = queue.popleft()
        cell = path[-1]

        if cell == end:
            return path 
        
        if cell not in visited:
            visited.add(cell)
            for neighbor in graph[cell]:
                if neighbor not in visited:
                    queue.append(path + [neighbor])
    
    return []

#Creating cell class
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.visited = False

    def draw(self):
        '''Draws the tile outlines if they are explored and with corresponding existing walls'''
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(screen, (0, 90, 100), (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(screen, (0, 90, 100), (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(screen, (0, 90, 100), (x, y), (x, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(screen, (0, 90, 100), (x, y + TILE), (x + TILE, y + TILE), 3)

    def draw_current_cell(self):
        '''Draws in the inner square of each cell'''
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, (0, 255, 0), (x + 2, y + 2, TILE - 2, TILE - 2))

    def check_cell(self, x, y):
        '''checks to see if the cell is within the bounds, else returns None'''
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return None
        return grid_cells[x + y * cols]

    def check_neighbors(self):
        '''Checks to see if the neighbouring cells exist and creates a list of neighbouring nodes'''
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

    def __str__(self):
        return f"{self.x},{self.y}"

def remove_walls(current, next_cell):
    '''Looks between two cells and checks to see if there is a wall between the two cells. Updates .walls accordingly'''
    dx = current.x - next_cell.x
    dy = current.y - next_cell.y

    if dx == 1:
        current.walls['left'] = False
        next_cell.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next_cell.walls['left'] = False
    elif dy == 1:
        current.walls['top'] = False
        next_cell.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next_cell.walls['top'] = False

#variables
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
graph = defaultdict(list)
dodathing = False
final_path = []
takeinput = True
flag = True

#Game loop
while flag:
    screen.fill("white")
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    
    next_cell = choice(current_cell.check_neighbors()) if current_cell.check_neighbors() else None
    if next_cell:
        stack.append(current_cell)
        next_cell.visited = True
        remove_walls(current_cell, next_cell)

        if not current_cell.walls['top'] and next_cell == current_cell.check_cell(current_cell.x, current_cell.y - 1):
            graph[str(current_cell)].append(str(next_cell))
            graph[str(next_cell)].append(str(current_cell))
        if not current_cell.walls['right'] and next_cell == current_cell.check_cell(current_cell.x + 1, current_cell.y):
            graph[str(current_cell)].append(str(next_cell))
            graph[str(next_cell)].append(str(current_cell))
        if not current_cell.walls['bottom'] and next_cell == current_cell.check_cell(current_cell.x, current_cell.y + 1):
            graph[str(current_cell)].append(str(next_cell))
            graph[str(next_cell)].append(str(current_cell))
        if not current_cell.walls['left'] and next_cell == current_cell.check_cell(current_cell.x - 1, current_cell.y):
            graph[str(current_cell)].append(str(next_cell))
            graph[str(next_cell)].append(str(current_cell))

        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    #input loop
    key = pygame.key.get_pressed()
    if current_cell.x == 0 and current_cell.y == 0:
    #DFS run
        if key[pygame.K_d] and takeinput:
            takeinput = False
            start, end = str(grid_cells[0]), str(grid_cells[-1])
            path = DFS_path(graph, start, end)
            
            path_boxes = []
            for pos in path:
                x, y = map(int, pos.split(","))
                path_boxes.append((x * TILE + 2, y * TILE + 2, TILE - 5, TILE - 5))
            #OW.play()
            dodathing = True
            
    #BFS run
        elif key[pygame.K_b]:
            takeinput = False
            start, end = str(grid_cells[0]), str(grid_cells[-1])
            path = BFS_path(graph, start, end)
            
            path_boxes = []
            for pos in path:
                x, y = map(int, pos.split(","))
                path_boxes.append((x * TILE + 2, y * TILE + 2, TILE - 5, TILE - 5))
            WOW.play()
            dodathing = True
    #resets path
        elif key[pygame.K_r]:
            dodathing = False
            takeinput = True
            final_path = []
            path_boxes = []

    #prints path
    if dodathing:
        for i in final_path:
            pygame.draw.rect(screen, (0, 255, 0), i)
    
        if path_boxes:
            box = path_boxes.pop()
            pygame.draw.rect(screen, (255, 255, 255), box)
            final_path.append(box)
    
#quitter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()