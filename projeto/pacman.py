import pygame
import sys
import random
import math

# Inicialização
pygame.init()
WIDTH, HEIGHT = 400, 280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Simples")

# Cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 100, 150)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Labirinto (0=vazio, 1=parede)
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,0,1],
    [1,0,1,0,0,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

CELL_SIZE = WIDTH // len(maze[0])

# Lista de bolinhas
dots = [(x, y) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x]==0]

# Pac-Man
pac_x, pac_y = 1, 1  # posição em células
dir_x, dir_y = 0, 0
mouth_angle = 0
mouth_dir = 1

# Fantasmas
ghost_colors = [RED, PINK, CYAN, ORANGE]
ghost_positions = [(8,5), (8,1), (1,5), (5,3)]  # em células

clock = pygame.time.Clock()
running = True
game_over = False
game_won = False

def draw_text(text, color):
    font = pygame.font.SysFont(None, 48)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(render, rect)

while running:
    screen.fill(BLACK)

    # Desenhar labirinto e bolinhas
    for y,row in enumerate(maze):
        for x,cell in enumerate(row):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell==1:
                pygame.draw.rect(screen, BLUE, rect)
            elif (x,y) in dots:
                pygame.draw.circle(screen, WHITE, rect.center, 4)

    # Animar boca
    mouth_angle += mouth_dir * 0.1
    if mouth_angle > 0.25*math.pi or mouth_angle < 0:
        mouth_dir *= -1

    # Desenhar Pac-Man
    pac_px, pac_py = pac_x*CELL_SIZE+CELL_SIZE//2, pac_y*CELL_SIZE+CELL_SIZE//2
    pygame.draw.circle(screen, YELLOW, (pac_px, pac_py), CELL_SIZE//2)
    pygame.draw.polygon(screen, BLACK, [
        (pac_px, pac_py),
        (pac_px + CELL_SIZE//2*math.cos(mouth_angle), pac_py - CELL_SIZE//2*math.sin(mouth_angle)),
        (pac_px + CELL_SIZE//2*math.cos(-mouth_angle), pac_py - CELL_SIZE//2*math.sin(-mouth_angle))
    ])

    # Desenhar fantasmas
    for i,(gx,gy) in enumerate(ghost_positions):
        gpx, gpy = gx*CELL_SIZE+CELL_SIZE//2, gy*CELL_SIZE+CELL_SIZE//2
        pygame.draw.circle(screen, ghost_colors[i], (gpx,gpy), CELL_SIZE//2)

    # Checar vitória
    if not dots and not game_won and not game_over:
        game_won = True

    if game_won:
        draw_text("Você venceu!", WHITE)

    if game_over:
        draw_text("Game Over!", RED)

    pygame.display.flip()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not (game_over or game_won):
            if event.key == pygame.K_LEFT and maze[pac_y][pac_x-1]==0: dir_x, dir_y = -1, 0
            elif event.key == pygame.K_RIGHT and maze[pac_y][pac_x+1]==0: dir_x, dir_y = 1, 0
            elif event.key == pygame.K_UP and maze[pac_y-1][pac_x]==0: dir_x, dir_y = 0, -1
            elif event.key == pygame.K_DOWN and maze[pac_y+1][pac_x]==0: dir_x, dir_y = 0, 1

    # Movimento Pac-Man
    if not (game_over or game_won):
        next_x, next_y = pac_x+dir_x, pac_y+dir_y
        if maze[next_y][next_x]==0:
            pac_x, pac_y = next_x, next_y

        # Comer bolinha
        if (pac_x,pac_y) in dots:
            dots.remove((pac_x,pac_y))

        # Movimento fantasmas (grade)
        for i,(gx,gy) in enumerate(ghost_positions):
            valid_dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            valid_dirs = [(dx,dy) for dx,dy in valid_dirs if maze[gy+dy][gx+dx]==0]
            if valid_dirs:
                dx, dy = random.choice(valid_dirs)
                ghost_positions[i] = (gx + dx, gy + dy)

        # Colisão com fantasmas
        if (pac_x,pac_y) in ghost_positions:
            game_over = True

    clock.tick(5)

pygame.quit()
sys.exit()
