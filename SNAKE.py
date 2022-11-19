import pygame
import random
import math
from datetime import datetime, date, time

WIDTH = 1000
HEIGHT = 540
FPS = 30
CELL_SIZE = 35
NUMBER_OF_CELLS = 14
STEP = CELL_SIZE - 1
OFFSET_X = (WIDTH - NUMBER_OF_CELLS * CELL_SIZE) / 2
OFFSET_Y = (HEIGHT - NUMBER_OF_CELLS * CELL_SIZE) / 2 + 10
PLAYER_SIZE = (CELL_SIZE / 5) * 4
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
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()

def append_result(crash_score, crash_time):
    h = datetime.utcnow()
    g = h.strftime("%Y.%m.%d %H:%M:%S") 
    b = open('snake_results.txt', 'a')
    b.write(' ' + str(crash_score) + ' | ' + str(crash_time) + ' | ' + str(g) + '\n')
    b.close()

def key_score(number_1):
    print(number_1)
    a = number_1.split(' | ', maxsplit=1)
    b = int(a[0])
    return b

def read_results():
    b = open('snake_results.txt', 'r')
    a = b.readlines()
    b.close()
    a = sorted(a, key=key_score)
    a.reverse()
    return a
    
def circle (x, y, radius):
    a = cell_to_pixels((x, y))
    pygame.draw.circle(screen, (186, 19, 13), (int(a[0]), int(a[1])), int(radius))

apple_count = 0

def big_circle(x, y, radius):
    a = cell_to_pixels((x, y))
    pygame.draw.circle(screen, (133, 214, 62), (int(a[0]), int(a[1])), int(radius))

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
    pygame.draw.rect(screen, (126, 86, 222), (pos[0] - PLAYER_SIZE/3, pos[1] - PLAYER_SIZE/3, PLAYER_SIZE, PLAYER_SIZE))

snake = []
snake.append(player_pos)

def draw_snake():
    for pos in snake:
        pos = cell_to_pixels(pos)
        pygame.draw.rect(screen, (128, 128, 255), (pos[0] - PLAYER_SIZE/2, pos[1] - PLAYER_SIZE/2, PLAYER_SIZE, PLAYER_SIZE))

apple_x = random.randint(0, NUMBER_OF_CELLS - 1)
apple_y = random.randint(0, NUMBER_OF_CELLS - 1)

def draw_apple():
    circle(apple_x, apple_y, PLAYER_SIZE / 2 - 5)

def draw_big_apple():
    big_circle(apple_x, apple_y, CELL_SIZE / 2)

def draw_time_score(time, vvvvvvvv):
    time = round(time)
    str_time = 'TIME: ' + str(time) + '          ' + 'SCORE: ' + str(vvvvvvvv)
    fontObj = pygame.font.Font('freesansbold.ttf', 30)
    textSurfaceObj = fontObj.render(str_time, True, (56, 54, 45), (244, 255, 236))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WIDTH / 2, 17)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()

def table(w, h, stroki):
    x = WIDTH // 3 - 100 // 3 - 5
    y = HEIGHT / 2 - 25
    for i in range(4):
        pygame.draw.line(screen, (0,0,0), [x, y + h * i], [x + w[0] + w[1] + w[2] + 5, y + h * i], 2)
        w_offset = 0
    pygame.draw.line(screen, (0,0,0), [x + w_offset, y], [x + w_offset, y + h * 3], 2)
    pygame.draw.line(screen, (0,0,0), [x + w[0], y], [x + w[0], y + h * 3], 2)
    pygame.draw.line(screen, (0,0,0), [x + w[0] + w[1], y], [x + w[0] + w[1], y + h * 3], 2)
    pygame.draw.line(screen, (0,0,0), [x + w[0] + w[1] + w[2] + 5, y], [x + w[0] + w[1] + w[2] + 5, y + h * 3], 2)

speed_x = 0
speed_y = 0
f_count = 0
snake_crash = False
pobeda = ''
count = 0
time = -1
five_count = 0
# Цикл игры

running = True
while running:
    clock.tick(FPS)
    screen.fill((120, 188, 188)) #цвет проигрышного окна
    if time >= 0:
        time += 1
    w2max = 0
    if snake_crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                snake_crash = False
                apple_count = 0
                time = -1
                snake = [(0,0)]
                player_pos = (0,0)
                speed_x = 0
                speed_y = 0

        pobeda = 'GAME OVER'
        str_count = 'SCORE:' + ' ' + str(apple_count + apple_count // 5)
        if time_1 < 0:
            time_1 = 0
        str_time = 'TIME:' + ' ' + str(time_1)
        sort_results = read_results()
        
        fontObj = pygame.font.Font('freesansbold.ttf', 30)
        textSurfaceObj_1 = fontObj.render(pobeda, True, (255, 194, 241), (120, 188, 188))
        textSurfaceObj_2 = fontObj.render(str_count, True, (211, 67, 255), (120, 188, 188))
        textSurfaceObj_3 = fontObj.render(str_time, True, (211, 67, 255), (120, 188, 188))
        textSurfaceObj_4 = fontObj.render('RECORDS TABLE', True, (211, 67, 255), (120, 188, 188))
        textRectObj_1 = textSurfaceObj_1.get_rect()
        textRectObj_2 = textSurfaceObj_2.get_rect()
        textRectObj_3 = textSurfaceObj_3.get_rect()
        textRectObj_4 = textSurfaceObj_4.get_rect()
        textRectObj_1.center = (WIDTH / 2, HEIGHT / 2 - 200)
        textRectObj_2.center = (WIDTH / 2, HEIGHT / 2 - 150)
        textRectObj_3.center = (WIDTH / 2, HEIGHT / 2 - 100)
        textRectObj_4.center = (WIDTH / 2, HEIGHT / 2 - 50)
        screen.blit(textSurfaceObj_1, textRectObj_1)
        screen.blit(textSurfaceObj_2, textRectObj_2)
        screen.blit(textSurfaceObj_3, textRectObj_3) 
        screen.blit(textSurfaceObj_4, textRectObj_4)     

        for i in range(0, min(len(sort_results),3)):
            a = sort_results[i]
            a = a[0:-1]
            split_a = a.split('|')
            fontObj = pygame.font.Font('freesansbold.ttf', 30)
            h = 50
            for j in range(len(split_a)):
                textSurfaceObj = fontObj.render(split_a[j], True, (0, 0, 0), (120, 188, 188))
                textRectObj = textSurfaceObj.get_rect()
                w = textSurfaceObj.get_rect().w
                if w2max <= w:
                    w2max = w
                textRectObj.midleft = (WIDTH // 3 - 100 // 3 + 75 * j, HEIGHT / 2 + 50 * i)
                screen.blit(textSurfaceObj, textRectObj)     
        w = [75,75, w2max]
        table(w, h, 3)
        pygame.display.flip()                                                                                  #здесь был цикл с выводои резов
        continue
    
    
    
    
    f_count = f_count + 1
    player_move = False
    if f_count >= 7:
        f_count = 0
        player_move = True
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x = -1
                speed_y = 0
            elif event.key == pygame.K_RIGHT:
                speed_x = 1
                speed_y = 0
            elif event.key == pygame.K_UP:
                speed_y = -1 
                speed_x = 0
            elif event.key == pygame.K_DOWN:
                speed_y = 1
                speed_x = 0
    
    if player_move:
        if (speed_x != 0 or speed_y != 0) and time == -1: 
            time = 0
        player_pos = (player_pos[0] + speed_x, player_pos[1] + speed_y)            
        if player_pos[0] < 0:
            player_pos = (0, player_pos[1])
            snake_crash = True
        elif player_pos[0] >= NUMBER_OF_CELLS:
            player_pos = (NUMBER_OF_CELLS - 1, player_pos[1])
            snake_crash = True
        elif player_pos[1] < 0:
            player_pos = (player_pos[0], 0)
            snake_crash = True
        elif player_pos[1] >= NUMBER_OF_CELLS:
            player_pos = (player_pos[0], NUMBER_OF_CELLS - 1)
            snake_crash = True

        if player_pos in snake and (speed_x != 0 or speed_y != 0):
            snake_crash = True
            
        if player_pos[0] == apple_x and player_pos[1] == apple_y:
            apple_x = random.randint(0, NUMBER_OF_CELLS - 1)
            apple_y = random.randint(0, NUMBER_OF_CELLS - 1)
            apple_count += 1

            snake.append(player_pos)
            print(apple_count + apple_count // 5)

        if not snake_crash:
            for i in range(len(snake) - 1):
                snake[i] = snake[i + 1]
            snake[len(snake) - 1] = player_pos
            time_1 = time // 30
        else:
           append_result(apple_count + apple_count // 5, time_1)  


    # Рендеринг
    screen.fill((244, 255, 236))
    draw_field()
    draw_snake()
    draw_player()
    if (apple_count + 1) % 5 != 0 or apple_count == 0:
        draw_apple()
    else:
        draw_big_apple()
    draw_time_score(time / 30, apple_count + apple_count // 5)
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()






