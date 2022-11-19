import pygame
import random
from math import sqrt

WIDTH = 600
HEIGHT = 600
FPS = 60
CELL_SIZE = 50
OBSTACLE_SIZE = 75

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

class Obstacle():
    def __init__(self, size, speed, offset_from_down, echelon):
        self.size = size
        self.speed = speed 
        self.offset_from_down = offset_from_down
        self.offset = 0 - size
        self.echelon = echelon
    def move(self, time):
        self.offset += self.speed * time
    def speed_up(self):
        if self.speed < 15: 
            self.speed += 1

def draw_rect(offset):
    player_up = HEIGHT - CELL_SIZE - offset
    if player_up < 0:
        player_up = 0
        offset = HEIGHT - CELL_SIZE 
    pygame.draw.rect(screen, (120, 188, 188), (WIDTH / 2 - CELL_SIZE / 2, HEIGHT - CELL_SIZE - offset, CELL_SIZE, CELL_SIZE))

def draw_obstacle(obst, color):
    pygame.draw.rect(screen, color, (WIDTH - obst.size - obst.offset, HEIGHT - obst.offset_from_down - obst.size, obst.size, obst.size))

def cross_test(obst, offset):
    right = WIDTH / 2 + CELL_SIZE / 2
    left = WIDTH / 2 - CELL_SIZE / 2
    down = offset
    up = offset + CELL_SIZE
    obstacle_right = WIDTH - obst.offset
    obstacle_left =  WIDTH - (obst.offset + obst.size)
    obstacle_up = obst.size + obst.offset_from_down
    obstacle_down = obst.offset_from_down
    if (down > obstacle_up or obstacle_down > up):
        return False
    elif (obstacle_right < left or obstacle_left > right):
        return False
    else:
        return True

def kasanie_test(offset):
    if offset >= HEIGHT - CELL_SIZE:
        kasanie = True
    else:
        kasanie = False
    return kasanie

offset = 0
speed = 0 
move = False
a = 2500
obstacles = []
for i in range(0, 3):
    echelon = (HEIGHT - 2 * OBSTACLE_SIZE) / 3 * i + OBSTACLE_SIZE
    offset_from_down = echelon + random.randint(0 - int(OBSTACLE_SIZE / 2), int(OBSTACLE_SIZE / 2))
    obst = Obstacle(random.randint(50, OBSTACLE_SIZE),\
         random.randint(1,30) / 10, offset_from_down, echelon)
    obstacles.append(obst)
    print(echelon)
color = BLACK
color_test = False
kasanie = False
fragments_count = 0
seconds_count = 0

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    fragments_count += 1
    if fragments_count % 60 == 0:
        seconds_count += 1
        if seconds_count % 5 == 0:
            for obst in obstacles:
                obst.speed_up()
    for obst in obstacles: 
        if obst.offset >= WIDTH + obst.size:
            offset_from_down = obst.echelon + random.randint(0 - HEIGHT / 10, HEIGHT / 10)
            o = Obstacle(random.randint(50, OBSTACLE_SIZE),\
                random.randint(1,30) / 10,  offset_from_down, obst.echelon)
            obstacles.append(o)
            obstacles.remove(obst)
            
    for obst in obstacles:
        obst.move(FPS / 60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                move = True
                speed = 1200           #5 пикслелей в секунду
                
    if move:
        offset += speed / FPS
        speed -= a / FPS
    
    if kasanie_test(offset) == True:
        speed = -90
        offset += speed / FPS
        speed -= a / FPS

    if offset <= 0:
        offset = 0
        move = False
    
    screen.fill(WHITE)
    draw_rect(offset)
    for obst in obstacles:
        if cross_test(obst, offset) == True:
            color = RED
        else:
            color = BLACK
        draw_obstacle(obst, color)
    pygame.display.flip()

pygame.quit()
