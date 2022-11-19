import pygame
import random

def krest(screen, x, y, size):
    pygame.draw.line(screen, WHITE, [x - size, y - size], [x + size, y + size], 3)
    pygame.draw.line(screen, WHITE, [x - size, y + size], [x + size, y - size], 3)

def circle(screen, x, y, radius):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), radius, 1)

WIDTH = 540
HEIGHT = 540
FPS = 30
CELL_SIZE = 100
STEP = CELL_SIZE - 1
OFFSET_X = (WIDTH - 3 * CELL_SIZE) / 2
OFFSET_Y = (HEIGHT - 3 * CELL_SIZE) / 2
SIZE_ZNAKA = int((CELL_SIZE - (CELL_SIZE /5) * 2) / 2 + 2)

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

pos_kresta = []
mesta_kresta = []
pos_kruga = []
mesta_kruga = []

# Цикл игры
running = True
krest_win = False
circles_win = False
nichya = False

def show_finish_window():
    running = True
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    if krest_win:
        pobeda = 'КРЕСТИКИ ВЫИГРАЛИ'
    elif circles_win:
        pobeda = 'НОЛИКИ ВЫИГРАЛИ'
    elif nichya:
        pobeda = 'НИЧЬЯ'
    
    fontObj = pygame.font.Font('freesansbold.ttf', 30)
    textSurfaceObj = fontObj.render(pobeda, True, (255, 255, 255), (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()
    return running

def check_user_input():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.button, event.pos)
            print((event.pos[0] - OFFSET_X) // CELL_SIZE, (event.pos[1] - OFFSET_Y) // CELL_SIZE)
            ppos = int((event.pos[0] - OFFSET_X) // CELL_SIZE), int((event.pos[1] - OFFSET_Y) // CELL_SIZE)
            print(ppos in mesta_kresta, ppos in mesta_kruga)
            if not ppos in mesta_kresta and not ppos in mesta_kruga:
                if ppos[0] >= 0 and ppos[0] < 3 and ppos[1] >= 0 and ppos[1] < 3:
                    mesta_kruga.append(ppos)
                    added = False
                    for i in range(1000):
                        a = random.randint(0,2)
                        b = random.randint(0,2)
                        ppos = a, b
                        if not ppos in mesta_kruga and not ppos in mesta_kresta:
                            mesta_kresta.append(ppos)
                            break
            
    return running                  

def drawing(circles_win, krest_win):
    screen.fill(BLACK)
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (OFFSET_X + (i * STEP), OFFSET_Y + (j * STEP), CELL_SIZE, CELL_SIZE), 1)
            
    for pos in mesta_kresta:
       krest(screen, OFFSET_X + (pos[0] * STEP) + CELL_SIZE / 2, OFFSET_Y + (pos[1] * STEP) + CELL_SIZE / 2, SIZE_ZNAKA) 
    for pos in mesta_kruga:
       circle(screen, OFFSET_X + (pos[0] * STEP) + CELL_SIZE / 2, OFFSET_Y + (pos[1] * STEP) + CELL_SIZE / 2, SIZE_ZNAKA) 
    
    pygame.display.flip()

def check_winner():
    krest_win = False
    circles_win = False
    nichya = False
    for i in range(3):
        if (0,i) in mesta_kresta and (1,i) in mesta_kresta and (2,i) in mesta_kresta:
            krest_win = True
        elif (i,0) in mesta_kresta and (i,1) in mesta_kresta and (i,2) in mesta_kresta:
            krest_win = True
        elif (0,i) in mesta_kruga and (1,i) in mesta_kruga and (2,i) in mesta_kruga:
            circles_win = True
        elif (i,0) in mesta_kruga and (i,1) in mesta_kruga and (i,2) in mesta_kruga:
            circles_win = True
    
    if (0,0) in mesta_kresta and (1,1) in mesta_kresta and (2,2) in mesta_kresta:
        krest_win = True
    elif (2,0) in mesta_kresta and (1,1) in mesta_kresta and (0,2) in mesta_kresta:
        krest_win = True
    elif (0,0) in mesta_kruga and (1,1) in mesta_kruga and (2,2) in mesta_kruga:
        circles_win = True
    elif (2,0) in mesta_kruga and (1,1) in mesta_kruga and (0,2) in mesta_kruga:
        circles_win = True
    
    if not circles_win and not krest_win and (len(mesta_kresta) + len(mesta_kruga)) == 9:
        nichya = True
    return krest_win, circles_win, nichya



while running:
    clock.tick(FPS)
    if krest_win or circles_win or nichya:
        running = show_finish_window()
        continue

    running = check_user_input()

    krest_win, circles_win, nichya = check_winner()
    
    drawing(circles_win, krest_win)

pygame.quit()


