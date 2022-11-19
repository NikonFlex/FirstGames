import pygame
import random

WIDTH = 540
HEIGHT = 540
FPS = 30
CELL_SIZE = 50
NUMBER_OF_CELLS = 8
STEP = CELL_SIZE - 1
OFFSET_X = (WIDTH - NUMBER_OF_CELLS * CELL_SIZE) / 2
OFFSET_Y = (HEIGHT - NUMBER_OF_CELLS * CELL_SIZE) / 2
PLAYER_SIZE = (CELL_SIZE / 5) * 3
OFFSET_OF_PLAYER = (CELL_SIZE - PLAYER_SIZE) / 2

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def circle(screen, x, y, radius):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), radius, 1)

def cell_to_pixels(pos):
    return CELL_SIZE / 2 + OFFSET_X + (pos[0] * CELL_SIZE), CELL_SIZE / 2 + OFFSET_Y + (pos[1] * CELL_SIZE)

def pixel_to_cell(pos):
    return int((pos[0] - OFFSET_X) // CELL_SIZE), int((pos[1] - OFFSET_Y) // CELL_SIZE)

def draw_field():
    for i in range(NUMBER_OF_CELLS):
        for j in range(NUMBER_OF_CELLS):
            pos = cell_to_pixels((i,j))
            pygame.draw.rect(screen, (210, 210, 210), (pos[0] - CELL_SIZE / 2, pos[1] - CELL_SIZE / 2, CELL_SIZE + 1 ,CELL_SIZE + 1), 1)

player_pos = (0,0)

def draw_player():
    pos = cell_to_pixels(player_pos)
    pygame.draw.rect(screen, (0, 0, 0), (pos[0] - PLAYER_SIZE/2, pos[1] - PLAYER_SIZE/2, PLAYER_SIZE, PLAYER_SIZE))

speed_x = 0
speed_y = 0
f_count = 0


# Цикл игры
running = True
while running:
    clock.tick(FPS)
    f_count = f_count + 1
    player_move = False
    if f_count >= 20:
        f_count = 0
        player_move = True
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x = -1
                speed_y = 0
            elif event.key == pygame.K_RIGHT:
                speed_x = +1
                speed_y = 0
            elif event.key == pygame.K_UP:
                speed_y = -1 
                speed_x = 0
            elif event.key == pygame.K_DOWN:
                speed_y = 1
                speed_x = 0
    if player_move:
        player_pos = (player_pos[0] + speed_x, player_pos[1] + speed_y)            

    if player_pos[0] < 0:
        player_pos = (0, player_pos[1])
    elif player_pos[0] >= NUMBER_OF_CELLS:
        player_pos = (NUMBER_OF_CELLS - 1, player_pos[1])
    elif player_pos[1] < 0:
        player_pos = (player_pos[0], 0)
    elif player_pos[1] >= NUMBER_OF_CELLS:
        player_pos = (player_pos[0], NUMBER_OF_CELLS - 1)
    
    # Рендеринг
    screen.fill(WHITE)
    draw_field()
    draw_player()
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()