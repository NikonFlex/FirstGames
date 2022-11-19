import pygame
import random

WIDTH = 550
HEIGHT = 550
FPS = 60
CELL_SIZE = 50
PLAYER_SIZE = 50

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OBST_COLOR = (10, 0, 65)        
PLAYER_COLOR = (196, 255, 14)   
DEACRESE_FIELD_COLOR = (176, 230, 213)
RESULT_COLOR = (35, 46, 81)
TXT_COLOR = (10, 0, 65)   
CELL_SIZE = 45
PLAYER_SIZE = 45

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SQUARE BOUNDS")
clock = pygame.time.Clock()

def read_results():
    b = open('square_bound_results.txt', 'r')
    a = b.readlines()
    b.close()
    a = sorted(a, key=key_score)
    a.reverse()
    return a

def append_results(result):
    b = open('square_bound_results.txt', 'a')
    b.write(str(result) + '\n')
    b.close()

def key_score(number_1):
    a = number_1.split('/')
    b = int(a[0])
    return b

def draw_best_result(best_result):
    str_time = 'BEST ' + str(best_result) 
    font = pygame.font.SysFont("Agency FB", 45)
    label1 = font.render(str_time, 1, RESULT_COLOR)
    label1.set_alpha(100)
    textRectObj = label1.get_rect()
    textRectObj.center = (WIDTH / 2, HEIGHT / 2 + 20)
    screen.blit(label1, textRectObj)     

class Obstacle():
    def __init__(self, x, y, speed_x, speed_y, speed_count):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.speed_count = speed_count
        self.color = OBST_COLOR

    def update(self): # прибавлять скорость к позиции
        self.x += self.speed_x
        self.y += self.speed_y
    
    def check_rebound(self): # проверять касание со стенами и менять скорость
        up = False
        down = False
        left = False
        right = False
        if self.y >= HEIGHT - CELL_SIZE - thikness / 2:
            up = True
            down = False
        elif self.y <= thikness / 2:
            down = True
            up = False
        if self.x >= WIDTH - CELL_SIZE - thikness / 2:
            right = False
            left = True
        elif self.x <= thikness / 2:
            right = True
            left = False
        if down:
            self.speed_y = self.speed_count + 0.5
        if up:
            self.speed_y = 0 - self.speed_count - 0.5
        if left:
            self.speed_x = 0 - self.speed_count
        if right:
            self.speed_x = self.speed_count
     
def draw_rect(x,y, color_rect):
    pygame.draw.rect(screen, color_rect, (x, y, CELL_SIZE, CELL_SIZE))

def draw_player(player_x, player_y):
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

def deacrease_field(thikness):
    pygame.draw.rect(screen, DEACRESE_FIELD_COLOR, (0, 0, WIDTH, HEIGHT), thikness)

def cross_test(x, y, size_1, player_x, player_y, size_2):
    left = x
    right = x + size_1
    up = y
    down = y + size_1
    player_left = player_x
    player_right = player_x + size_2
    player_up = player_y
    player_down = player_y + size_2
    if down < player_up or player_down < up:
        return False
    elif right < player_left or left > player_right:
        return False
    else:
        return True

def draw_time(time):
    str_time = 'TIME ' + str(time) 
    font = pygame.font.SysFont("Agency FB", 45)
    label1 = font.render(str_time, 1, RESULT_COLOR)
    label1.set_alpha(100)
    textRectObj = label1.get_rect()
    textRectObj.center = (WIDTH / 2, HEIGHT / 2 - 20)
    screen.blit(label1, textRectObj)      

def time_and_errors_on_screen(time, record, error):
    str_time = 'time ' + str(time) + ' ('+ str(record) + ')'  
    str_error = 'bounds ' + str(error)
    font = pygame.font.SysFont("Agency FB", 20)     #рисование времени
    label1 = font.render(str_time, 1, BLACK)
    label1.set_alpha(100)
    textRectObj = label1.get_rect()
    textRectObj.center = (38, 8)
    screen.blit(label1, textRectObj)      
    font = pygame.font.SysFont("Agency FB", 20)     #рисование ошибок
    label1 = font.render(str_error, 1, (0,0,0))
    label1.set_alpha(100)
    textRectObj = label1.get_rect()
    textRectObj.center = (WIDTH - 30, 8)
    screen.blit(label1, textRectObj)  

def spawn_obst(obst_list):
    for obst in obst_list:
        obst.x = random.randint(thikness // 2, WIDTH - CELL_SIZE - thikness // 2)
        obst.y = random.randint(thikness // 2, HEIGHT - CELL_SIZE - thikness // 2)

def cross_obsts(obst_list):
    obsts_cross = False
    n_of_obst = len(obst_list)
    for i in range(n_of_obst):
        for j in range(n_of_obst):
            if i != j:
                cross = cross_test(obst_list[i].x, obst_list[i].y, CELL_SIZE, obst_list[j].x, obst_list[j].y, CELL_SIZE)
                if cross:
                    obsts_cross = True
    if obsts_cross:
        return True
    else:
        return False

def cross_obst_and_player(obst_list, player_x, player_y):
    obst_and_player_cross = False
    for obst in obst_list:
        player_cross_obst = cross_test(obst.x, obst.y, CELL_SIZE, player_x, player_y, PLAYER_SIZE)
        if player_cross_obst:
            obst_and_player_cross = True
    if obst_and_player_cross:
        return True
    else:
        return False

def record_count():
    all_sorted_results = read_results()
    best_result = all_sorted_results[0]
    best_result = key_score(best_result)
    return best_result

thikness = 35
x = WIDTH - CELL_SIZE - thikness // 2
y = thikness // 2
down = True
up = False
right = False
left = True
speed_side = 0
speed_down = 0 
color_rect = BLACK
color_screen = WHITE
speed_player_side = 0
speed_player_up = 0
speed_count = 3
fps_count = 0
time = 0
player_x = WIDTH / 2 - PLAYER_SIZE / 2
player_y = HEIGHT / 2 - PLAYER_SIZE / 2
kasanie_right = False
kasanie_left = False
kasanie_up = False
kasanie_down = False
cross = False
cross_count = 0   
result = 0
in_touch = False
obst_list = []
obst_1 = Obstacle(x, y, speed_side, speed_down, speed_count)
obst_list.append(obst_1)
obst_2 = Obstacle(thikness // 2, random.randint(180, HEIGHT - thikness // 2 - CELL_SIZE), -speed_side, 3, speed_count)
obst_list.append(obst_2)
thikness_up = True
thikness_down = False
append_result = False
game_start = False


# Цикл игры
running = True
while running:
    fps_count += 1
    if fps_count % 15 == 0 and time >= 15:
        if thikness_up:
            thikness += 1
            if thikness > 150:
                thikness_down = True
                thikness_up = False
        elif thikness_down:
            thikness -= 1
            if thikness <= 35:
                thikness_down = False
                thikness_up = True
    if fps_count % 60 == 0:
        if cross_count < 10 and game_start:
            time += 1
        if time % 2 == 0:
            for obst in obst_list:
                if obst.speed_count <= 5:
                    obst.speed_count += 1/5
            
    if cross_count < 10 and game_start:
        for obst in obst_list:
            obst.update()
            obst.check_rebound()          

    player_x += speed_player_side
    player_y += speed_player_up
    
    if player_x >= WIDTH - PLAYER_SIZE - thikness / 2:
        player_x = WIDTH - PLAYER_SIZE - thikness / 2
        kasanie_right = True
    if player_x <= thikness / 2:
        player_x = thikness / 2
        kasanie_left = True
    if player_y <= thikness / 2:
        player_y = thikness / 2
        kasanie_up = True
    if player_y >= HEIGHT - PLAYER_SIZE - thikness / 2:
        player_y = HEIGHT - PLAYER_SIZE - thikness / 2
        kasanie_down = True

    if cross_count >= 10:
        speed_player_side = 0
        speed_player_up = 0
        thikness_down = False
        thikness_up = False

    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if cross_count < 10:
                if event.key == pygame.K_LEFT:
                    speed_player_side = -5
                    speed_player_up = 0
                    game_start = True
                elif event.key == pygame.K_RIGHT:
                    speed_player_side = 5
                    speed_player_up = 0
                    game_start = True
                elif event.key == pygame.K_UP:
                    speed_player_side = 0
                    speed_player_up = -5
                    game_start = True
                elif event.key == pygame.K_DOWN:
                    speed_player_side = 0
                    speed_player_up = 5
                    game_start = True
            if event.key == pygame.K_SPACE:   
                player_x = WIDTH / 2 - PLAYER_SIZE / 2
                player_y = HEIGHT / 2 - PLAYER_SIZE / 2
                spawn_obst(obst_list)
                things_cross = False
                player_cross_obst = cross_obst_and_player(obst_list, player_x, player_y)
                obst_and_obst_cross = cross_obsts(obst_list)
                if player_cross_obst or obst_and_obst_cross:
                    things_cross = True
                while things_cross:
                    things_cross = False
                    spawn_obst(obst_list)
                    player_cross_obst = cross_obst_and_player(obst_list, player_x, player_y)
                    obst_and_obst_cross = cross_obsts(obst_list)
                    if player_cross_obst or obst_and_obst_cross:
                        things_cross = True

                speed_player_side = 0
                speed_player_up = 0
                kasanie_right = False
                kasanie_left = False
                kasanie_up = False
                kasanie_down = False    
                for obst in obst_list:
                    obst.speed_count = 3
                cross = False
                time = 0
                cross_count = 0
                thikness = 35
                thikness_up = True
                thikness_down = False
                game_start = False

    if kasanie_right:
        speed_player_side = 0
        speed_player_up = 0
        player_x = WIDTH - PLAYER_SIZE - thikness / 2
    if kasanie_left:
        speed_player_side = 0
        speed_player_up = 0
        player_x = thikness / 2
    if kasanie_up:
        speed_player_side = 0
        speed_player_up = 0
        player_y = thikness / 2
    if kasanie_down:
        speed_player_side = 0
        speed_player_up = 0
        player_y = HEIGHT - PLAYER_SIZE - thikness / 2

    # Обновление
    
    # Рендеринг
    
    screen.fill(color_screen)
    cross_bool = False
    for obst in obst_list:
        n = cross_test(obst.x, obst.y, CELL_SIZE, player_x, player_y, PLAYER_SIZE)
        if n:
            cross_bool = True
            obst.color = (228, 17, 77)
        else:
            obst.color = OBST_COLOR
    if cross_bool:
        if not in_touch:    # факт пересечения
            result = time
            in_touch = True
            if cross_count < 10:
                cross_count += 1
    else:
        in_touch = False
   
    for obst in obst_list:
        draw_rect(obst.x, obst.y, obst.color)
    draw_player(player_x, player_y)
    deacrease_field(thikness)
    if cross_count == 10:    
        draw_time(result)
        time_and_errors_on_screen(result, record_count(), cross_count)
        if not append_result:
            append_results(result)
            all_sorted_results = read_results()
            best_result = all_sorted_results[0]
            best_result = key_score(best_result)
            append_result = True
        draw_best_result(best_result)
    else:
        time_and_errors_on_screen(time, record_count(), cross_count)
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()