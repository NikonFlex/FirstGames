import pygame
import random
import math
import falling_things
import game_windows
import Coin
from Cannon import Wheel, Bullet, Cannon
from Game_math import Rectangle, Point
import Game_progress
from Draw_permanent_states import Draw_permanent_states

WIDTH = 500
HEIGHT = 630
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GROND_HEIGHT = 30
IMPROVMENT_COST_K = 3.5
COIN_K = 4
MAX_FALLING_THINGS_IN_LEVEL = 10

# Создаем игру и окно
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CANNON")
clock = pygame.time.Clock()

#загрузка картинок
ground_surf = pygame.image.load(r'.\resources\ground.png')
background_surf = pygame.image.load(r'.\resources\background.png')
fire_surf_1 = pygame.image.load(r'.\resources\fire_for_shoot.png')
fire_surf_2 = pygame.image.load(r'.\resources\fire_for_shoot_2.png')

ground_scale = pygame.transform.scale(ground_surf, (int(ground_surf.get_width() // 1), int(ground_surf.get_height() // 1)))
background_scale = pygame.transform.scale(background_surf, (int(background_surf.get_width() // 1), int(background_surf.get_height() // 1)))
fire_scale_1 = pygame.transform.scale(fire_surf_1, (int(fire_surf_1.get_width() // 14), int(fire_surf_1.get_height() // 21)))
fire_scale_2 = pygame.transform.scale(fire_surf_2, (int(fire_surf_2.get_width() // 14), int(fire_surf_2.get_height() // 19)))

def draw_background(ground_height):
    background_rect = background_scale.get_rect(topleft = (0, 0))
    ground_rect = ground_scale.get_rect(topleft = (0, HEIGHT - ground_height))
    screen.blit(background_scale, background_rect)
    screen.blit(ground_scale, ground_rect)
    
def calc_wheel_rotation_angle(distance, radius):
    length_of_circle = 2 * math.pi * radius
    dist_per_angle = length_of_circle / 360
    return -(distance / dist_per_angle)

#debug_
def draw_rects_under_cannon(cannon):
    down_rect_x = cannon.cannon_rect.left
    down_rect_y = cannon.cannon_rect.bottom - cannon.cannon_rect.height // 4
    down_rect_height = cannon.cannon_rect.height // 4
    pygame.draw.rect(screen, GREEN, (down_rect_x, down_rect_y, cannon.cannon_rect.width, down_rect_height))
    top_rect_x = cannon.cannon_rect.left + cannon.cannon_rect.width // 6
    top_rect_y = cannon.cannon_rect.top
    top_rect_width = cannon.cannon_rect.width // 6 * 4
    top_rect_height = cannon.cannon_rect.height - down_rect_height
    pygame.draw.rect(screen, GREEN, (top_rect_x, top_rect_y, top_rect_width, top_rect_height)) 

def check_rects_intersection(rect_1, rect_2):
    if rect_1.x + rect_1.width < rect_2.x or rect_2.x + rect_2.width < rect_1.x:
       return False
    if rect_1.y + rect_1.height < rect_2.y or rect_2.y + rect_2.height < rect_1.y:
        return False

    return True

def get_min_n_of_things(things_list):
    min_n = 38456
    for thing in things_list:
        if thing.txt_number < min_n:
            min_n = thing.txt_number

    return min_n

def spawn_new_falling_thing(game_state):
    min_f_th_n = get_min_n_of_things(game_state.things_list)
    if min_f_th_n <= 10 and len(game_state.things_list) == 1:
        game_state.things_list.append(falling_things.Falling_things(WIDTH, HEIGHT - GROND_HEIGHT, r'.\resources\stone.png', game_state.game_progress.game_level, game_state.game_progress.cannon_level))
        return True
    else:
        return False
    
def spawn_new_coin(coins_list, falling_thing):
    coins_list.append(Coin.Coin(falling_thing.get_rect().x, falling_thing.get_rect().y, screen, WIDTH, HEIGHT - GROND_HEIGHT))


def collect_coin(coins_list, cannon_obj, number_of_coins):
    top_cannon_rect, bottom_cannon_rect = cannon_obj.get_rects_under_cannon()
    for coin in coins_list:
        # coin.get_rectangle()
        coin_pos, coin_size = coin.get_coin_position_and_size()
        coin_rect = Rectangle(coin_pos[0], coin_pos[1], coin_size, coin_size)
        if check_rects_intersection(coin_rect, top_cannon_rect) or check_rects_intersection(coin_rect, bottom_cannon_rect):
            coins_list.remove(coin)
            number_of_coins += 1 * COIN_K
    return number_of_coins

def check_cannon_and_falling_thing_intersection(things_list):
    cannon_rects_list = cannon.get_rects_under_cannon()
    for cannon_rect in cannon_rects_list:
        for thing in things_list:
            rects_intercection = check_rects_intersection(Rectangle.from_pygame_rect(thing.get_rect()), cannon_rect)
            if rects_intercection:
                return True
            else:
                return False

def bullets_list_update(bullets_list):
    if len(bullets_list) != 0:
        if bullets_list[0].get_position()[1] <= 0:
            bullets_list.remove(bullets_list[0])

def restart_game(game_state):
    game_state.game_finished = False
    game_state.finish_window = None
    game_state.things_list = []
    game_state.things_list.append(falling_things.Falling_things(WIDTH, HEIGHT - GROND_HEIGHT, r'.\resources\stone.png', game_state.game_progress.game_level, game_state.game_progress.cannon_level))
    game_state.coins_list = []
    game_state.bullets_list = []
    game_state.game_mode = True

def check_finish_window_events(finish_window, game_state, mouse_pos, click_event):
    if click_event and finish_window.the_mouse_intercect_the_button(mouse_pos) and game_state.game_progress.coins_n >= game_state.cannon_upgrade_cost:
        game_state.game_progress.cannon_level += 1
        game_state.game_progress.coins_n -= game_state.cannon_upgrade_cost
        game_state.cannon_upgrade_cost = int(IMPROVMENT_COST_K * game_state.game_progress.cannon_level)
        finish_window.cannon_level = game_state.game_progress.cannon_level
        finish_window.upgrade_cost = game_state.cannon_upgrade_cost
    
class Game_state:
    def __init__(self, game_progress, bullets_list,\
                       things_list, game_started, game_finished, coins_list, game_mode):

        self.game_progress = game_progress
        self.cannon_upgrade_cost = int(IMPROVMENT_COST_K * self.game_progress.cannon_level)
        self.bullets_list = bullets_list
        self.things_list = things_list
        self.game_started = game_started
        self.game_finished = game_finished
        self.coins_list = coins_list
        self.game_mode = game_mode

game_progress = Game_progress.read_file_with_progress()
game_state = Game_state(game_progress, [], [], False, False, [], False)
cannon_level = game_progress.cannon_level
cannon = Cannon(WIDTH // 2, WIDTH, HEIGHT - GROND_HEIGHT, screen)
game_state.things_list.append(falling_things.Falling_things(WIDTH, HEIGHT - GROND_HEIGHT, r'.\resources\stone.png', game_state.game_progress.game_level, game_state.game_progress.cannon_level))
right_move = False
left_move = False
mouse_move = [0, 0]
cannon_move = False
cannon_top = cannon.cannon_rect.top
start_window = game_windows.Start_window(screen, WIDTH, HEIGHT, r'.\resources\Cannon_for_game_windows.png', FPS, cannon_level)
finish_window = None
FPS_counter = 0
n_of_coins_obj_for_draw = Draw_permanent_states(screen, WIDTH, HEIGHT, game_state.game_progress.game_level)
fire_drew_on_last_frame = False
press = False
click_event = False
falling_things_counter = 0
level_complete = False
level_raised = False
# Цикл игры
running = True
while running:
    if level_complete and not level_raised:
        game_state.game_progress.game_level += 1 
        n_of_coins_obj_for_draw.raise_game_level()
        level_raised = True

    if game_state.game_finished:
        falling_things_counter = 0

    if game_state.game_finished:
        check_finish_window_events(finish_window, game_state, pygame.mouse.get_pos(), click_event)

    click_event = False
    pygame.mouse.set_visible(not game_state.game_mode)
    FPS_counter += 1
    game_state.game_progress.coins_n = collect_coin(game_state.coins_list, cannon, game_state.game_progress.coins_n)
    if falling_things_counter < MAX_FALLING_THINGS_IN_LEVEL:
        if spawn_new_falling_thing(game_state): 
            falling_things_counter += 1

    if len(game_state.things_list) == 0:
        if falling_things_counter == 10:
            level_complete = True
        game_state.game_finished = True
        game_state.game_mode = False

    for thing in game_state.things_list:
        thing.update()

    if check_cannon_and_falling_thing_intersection(game_state.things_list):
        game_state.game_finished = True
        game_state.game_mode = False

    bullets_list_update(game_state.bullets_list)

    if cannon_move:
        cannon_move = False
        angle_for_rotate = calc_wheel_rotation_angle(mouse_move[0], cannon.left_wheel.wheel_rect.width / 2)
        cannon.left_wheel.rotate_by(angle_for_rotate)
        cannon.right_wheel.rotate_by(angle_for_rotate)

    cannon_is_shooting = cannon.shooting(game_state.bullets_list)

    for thing in game_state.things_list:
        if thing.txt_number <= 0:
            game_state.things_list.remove(thing)
            spawn_new_coin(game_state.coins_list, thing)

        for bullet in game_state.bullets_list:
            if (thing.check_cross_bullet_and_thing(bullet)):
                thing.hit()
                game_state.bullets_list.remove(bullet)
                cannon.add_hit(game_state.game_progress.cannon_level)

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            game_progress.write_game_progress() 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                game_progress.write_game_progress() 

            if event.key == pygame.K_SPACE:
                if not game_state.game_started:
                    game_state.game_started = True
                    game_state.game_mode = True

                if game_state.game_finished:
                    restart_game(game_state)
                    level_complete = False
                    level_raised = False
                    cannon.hits_counter = 0

        if not game_state.game_mode:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not press:
                    press = True
                    click_event = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    press = False

        if event.type == pygame.MOUSEMOTION:
            cannon_move = True
            if cannon.cannon_rect.left == 2:
                cannon_move = False
            if cannon.cannon_rect.right == WIDTH - 2:
                cannon_move = False

            mouse_move = pygame.mouse.get_rel()
            cannon.move(mouse_move[0]) 
            cannon.clamp_pos_by_window()
    # Рендеринг
    screen.fill(WHITE)
    if game_state.game_mode:
        draw_background(GROND_HEIGHT)
        for coin in game_state.coins_list:
            coin.draw_coin()
            coin.coin_update(1/FPS)
        #draw_rects_under_cannon(cannon)
        for bullet in game_state.bullets_list:
            bullet.move(7)
            bullet.draw_bullet() 

        cannon.draw_cannon()

        for thing in game_state.things_list:
            thing.move(1/FPS)
            thing.draw(screen)
        if cannon_is_shooting:
            if not fire_drew_on_last_frame:        
                cannon.draw_fire_while_shoot(fire_scale_1)
                fire_drew_on_last_frame = True

            else:
                fire_drew_on_last_frame = False
                cannon.draw_fire_while_shoot(fire_scale_2)
    else:
        if not game_state.game_started:
            start_window.draw_start_window()

        if game_state.game_finished:
            if finish_window is None:
                hits_counter = cannon.get_n_hits()
                finish_window = game_windows.Finish_window(screen, WIDTH, HEIGHT, hits_counter, FPS, cannon_level, int(cannon_level * IMPROVMENT_COST_K))
            finish_window.draw_finish_window(pygame.mouse.get_pos(), click_event, level_complete)

    n_of_coins_obj_for_draw.draw_permanent_states(game_state.game_progress.coins_n, FPS_counter)
    pygame.display.flip()

pygame.quit()