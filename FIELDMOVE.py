import pygame
import random

WIDTH = 400
HEIGHT = 480
FPS = 60
PLAYER_SIZE = 40

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

def draw_player(player_x, player_y):
    pygame.draw.rect(screen, (255, 98, 0), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

def field_deacrease(thikness, field_x, field_y):
    pygame.draw.rect(screen, (153, 59, 230), (field_x, field_y, WIDTH, HEIGHT + thikness * 2), thikness)

def decor_rects(dec_rect_x, dec_rect_y, width, height):
    pygame.draw.rect(screen, (255, 98, 0), (dec_rect_x, dec_rect_y, width, height))

class Dec_rect():
    def __init__(self, dec_rect_x, dec_rect_y, width, height):
        self.dec_rect_x = dec_rect_x
        self.dec_rect_y = dec_rect_y
        self.width = width
        self.height = height

class Obstacle():
    def __init__(self, obst_x, obst_y, color):
        self.obst_x = obst_x
        self.obst_y = obst_y
        self.color = color
        self.width = random.randint(35, 60)
        self.height = random.randint(10, 15)
        self.speed_side_count = random.randint(3, 6)
        self.speed_vert_count = 0
        self.speed_side = 0
        self.speed_vert = 0

    def speed_vert_up(self):
        self.obst_y += self.speed_vert

    def speed_side_up(self):
        self.obst_x += self.speed_side
    
    def check_bound(self):
        up = False
        down = False
        right = False
        left = False
        if self.obst_x <= thikness / 2:
            left = False
            right = True
        elif self.obst_x >= WIDTH - thikness / 2 - self.width:
            left = True
            right = False
        if player_y <= max_offset_from_up:
            up = False
            down = True
        elif player_y >= max_offset_from_down:
            up = True
            down = False
        if player_y < max_offset_from_down and player_y > max_offset_from_up:
            up = False
            down = False
        if player_y == finish_y + finish_height:
            up = False
            down = False

        if left:
            self.speed_side = 0 - self.speed_side_count
        if right:
            self.speed_side = self.speed_side_count
        if up:
            self.speed_vert = -3
        elif down:
            self.speed_vert = 3
        else:
            self.speed_vert = 0 

def draw_obst(obst_x, obst_y, obst_width, obst_height, obst_color):
    pygame.draw.rect(screen, obst_color, (obst_x, obst_y, obst_width, obst_height))

def draw_finish(finish_x, finish_y, finish_height):
    n_of_lines = 3
    n_of_pillars = 21
    cell_size = WIDTH / n_of_pillars
    for i in range(n_of_lines):
        for j in range(n_of_pillars):
            if j % 2 == 0 and i % 2 == 0:
                color = BLACK
            elif j % 2 != 0 and i % 2 == 0:
                color = WHITE
            elif j % 2 == 0 and i % 2 != 0:
                color = WHITE
            elif j % 2 != 0 and i % 2 != 0:
                color = BLACK
            pygame.draw.rect(screen, color, (finish_x + cell_size * j, finish_y + cell_size * i, WIDTH, finish_height / n_of_lines))
    
def cross_test(obst_x, obst_y, width, height, player_x, player_y):
    left = obst_x
    right = obst_x + width
    up = obst_y
    down = obst_y + height
    player_left = player_x
    player_right = player_x + PLAYER_SIZE
    player_up = player_y
    player_down = player_y + PLAYER_SIZE
    if down < player_up or player_down < up:
        return False
    elif right < player_left or left > player_right:
        return False
    else:
        return True

def check_show_screen(y, height_of_obst):
    return y > -height_of_obst and y < HEIGHT
    
dec_rects_move = True
key_left = False
key_right = False
key_down = False
key_up = False
player_x = WIDTH / 2 - PLAYER_SIZE / 2
player_y = HEIGHT / 2 - PLAYER_SIZE / 2
speed_player_side = 0
speed_player_up = 0
kasanie = False
thikness = 15
field_x = 0
field_y = 0 - thikness
finish_x = 0
finish_y = -5000
max_offset_from_up = 60
max_offset_from_down = WIDTH - 60
move_forward = False
move_back = False
finish_height = 60
decor_rects_list = []
for i in range(100):
    dec_rect = Dec_rect(0, finish_y + 50 * 2 * i, thikness / 2 + 1, 50)
    decor_rects_list.append(dec_rect)
for i in range(100):
    dec_rect = Dec_rect(WIDTH - thikness / 2, finish_y + 50 * 2 * i, thikness / 2 + 1, 50)
    decor_rects_list.append(dec_rect)
dec_rect_speed = 0
obst_list = []
for i in range(100):
    if i % 2 != 0:
        obst = Obstacle(thikness / 2, finish_y + 100 + 75 * 2 * i, (153, 59, 230))
    elif i % 2 == 0:
        obst = Obstacle(WIDTH - thikness / 2, finish_y + 100 + 75 * 2 * i, (153, 59, 230))
    obst_list.append(obst)

# Цикл игры
running = True
while running:
    if finish_y + finish_height < player_y: 
        for obst in obst_list:
            obst.check_bound()
            obst.speed_side_up()
            if not kasanie and dec_rects_move:
                obst.speed_vert_up()

    player_x += speed_player_side
    player_y += speed_player_up

    for dec_rect in decor_rects_list:
        dec_rect.dec_rect_y += dec_rect_speed

    if player_x >= WIDTH - PLAYER_SIZE - thikness / 2:
        player_x = WIDTH - PLAYER_SIZE - thikness / 2
        kasanie = True
    if player_x <= thikness / 2:
        player_x = thikness / 2
        kasanie = True

    if player_y <= max_offset_from_up:
        player_y = max_offset_from_up
        dec_rect_speed = 3
        move_forward = True
        move_back = False
    
    if player_y >= max_offset_from_down:
        player_y = max_offset_from_down
        dec_rect_speed = -3
        move_forward = False
        move_back = True

    if not player_y <= max_offset_from_up and not player_y >= max_offset_from_down:
        dec_rect_speed = 0
        move_forward = False
        move_back = False
    
    if finish_y + finish_height >= player_y:
        move_forward = False
        dec_rect_speed = 0
        speed_player_side = 0
        speed_player_up = 0 
    
    if move_forward:
        finish_y += 3

    if move_back:
        finish_y -= 3

    if kasanie:
        speed_player_side = 0
        speed_player_up = 0
        dec_rect_speed = 0

    if not dec_rects_move:
        dec_rect_speed = 0

    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not kasanie:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed_player_side = -3
                    speed_player_up = 0
                    dec_rects_move = False
                elif event.key == pygame.K_RIGHT:
                    speed_player_side = 3
                    speed_player_up = 0
                    dec_rects_move = False
                elif event.key == pygame.K_UP:
                    speed_player_side = 0
                    speed_player_up = -3
                    dec_rects_move = True
                elif event.key == pygame.K_DOWN:
                    speed_player_side = 0
                    speed_player_up = 3
                    dec_rects_move = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_x = WIDTH / 2 - PLAYER_SIZE / 2
                player_y = HEIGHT / 2 - PLAYER_SIZE / 2
                kasanie = False
                speed_player_side = 0
                speed_player_up = 0
                finish_y = -1000
                decor_rects_list = []
                for i in range(30):
                    dec_rect = Dec_rect(0, finish_y + 50 * 2 * i, thikness / 2 + 1, 50)
                    decor_rects_list.append(dec_rect)
                for i in range(30):
                    dec_rect = Dec_rect(WIDTH - thikness / 2, finish_y + 50 * 2 * i, thikness / 2 + 1, 50)
                    decor_rects_list.append(dec_rect)
                dec_rect_speed = 0
                obst_list = []
                for i in range(30):
                    if i % 2 != 0:
                        obst = Obstacle(thikness / 2, finish_y + 100 + 75 * 2 * i, (153, 59, 230))
                    elif i % 2 == 0:
                        obst = Obstacle(WIDTH - thikness / 2, finish_y + 100 + 75 * 2 * i, (153, 59, 230))
                    obst_list.append(obst)
    # Обновление
    
    # Рендеринг
    screen.fill(WHITE)
    for obst in obst_list:
        if check_show_screen(obst.obst_y, obst.height):
            draw_obst(obst.obst_x, obst.obst_y, obst.width, obst.height, obst.color)
    
    draw_finish(finish_x, finish_y, finish_height)
    draw_player(player_x, player_y)
    field_deacrease(thikness, field_x, field_y)
    
    for dec_rect in decor_rects_list:
        if check_show_screen(dec_rect.dec_rect_y, dec_rect.height):
            decor_rects(dec_rect.dec_rect_x, dec_rect.dec_rect_y, dec_rect.width, dec_rect.height)
           
    for obst in obst_list:
        b = cross_test(obst.obst_x, obst.obst_y, obst.width, obst.height, player_x, player_y)
        if b:
            obst.color = RED
        else:
            obst.color = (153, 59, 230)

    pygame.display.flip()

pygame.quit()

