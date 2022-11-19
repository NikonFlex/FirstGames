import pygame
import random
from enum import Enum

'''class Direction(Enum):
    top = 1
    down = 2
    left = 3
    right = 4'''
    
WIDTH = 600
HEIGHT = 600
FPS = 30
NUMBER_OF_CELLS = 10
CELL_SIZE = 50
OFFSET_X = (WIDTH - NUMBER_OF_CELLS * CELL_SIZE) // 2
OFFSET_Y = (HEIGHT - NUMBER_OF_CELLS * CELL_SIZE) // 2

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
random.seed(100)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def pixel_to_cell(pixel_x:int, pixel_y:int):
    x_cell = (pixel_x - OFFSET_X) // NUMBER_OF_CELLS
    y_cell = (pixel_y - OFFSET_Y) // NUMBER_OF_CELLS
    return [x_cell, y_cell]

def cell_to_pixel(cell_x:int, cell_y:int, get_centre = False):
    #выдает самый левый и самый верхний пиксель
    x_pixel = OFFSET_X + cell_x * CELL_SIZE - cell_x
    y_pixel = OFFSET_Y + cell_y * CELL_SIZE - cell_y
    if get_centre:
        x_pixel -= CELL_SIZE // 2
        y_pixel -= CELL_SIZE // 2
    return Point(x_pixel, y_pixel)

def draw_field():
    for i in range(NUMBER_OF_CELLS):
        for j in range(NUMBER_OF_CELLS):
            step = CELL_SIZE - 1
            pygame.draw.rect(screen, (0, 0, 0), (OFFSET_X + step * j, OFFSET_Y + step * i, CELL_SIZE, CELL_SIZE), 1)

def check_game_over(snake_pieces_list, snake_course):
    current_head_pos = snake_pieces_list[-1]

    if snake_course == 'left':
        head_next_pos = [current_head_pos[0] - 1, current_head_pos[1]]
    
    elif snake_course == 'up':
        head_next_pos = [current_head_pos[0], current_head_pos[1] - 1]
    
    elif snake_course == 'down':
        head_next_pos = [current_head_pos[0], current_head_pos[1] + 1]

    elif snake_course == 'right':
        head_next_pos = [current_head_pos[0] + 1, current_head_pos[1]]

    if head_next_pos in snake_pieces_list:
        return True
    
    else:
        return False

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_pos(self):
        return [self.__x, self.__y]

class Rect:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def change_pos(self, new_x, new_y):
        self.__x = new_x
        self.__y = new_y

    def get_pos(self):
        return [self.__x, self.__y]

class Apple:
    def __init__(self, snake_pos):
        self.__size = CELL_SIZE // 2 - CELL_SIZE // 5
        while True:
            self.__cell = Rect(random.randint(0, 9), random.randint(0, 9))
            if self.__cell.get_pos() in snake_pos:
                self.__cell = Rect(random.randint(0, 9), random.randint(0, 9))
            else:
                break
            
    def get_pos(self):
        return self.__cell.get_pos()

    def draw(self):
        pos = self.__cell.get_pos()
        apple_pos_in_pixels = cell_to_pixel(pos[0], pos[1], True).get_pos()
        circle_r = self.__size
        color_index = 120
        color_step = color_index // self.__size
        circle_color = (255, color_index, color_index)
        while circle_r > 0:
            circle_r -= 1
            pygame.draw.circle(screen, circle_color, (OFFSET_X + apple_pos_in_pixels[0], OFFSET_Y + apple_pos_in_pixels[1]), circle_r)
            color_index -= color_step
            circle_color = (255, color_index, color_index)

class Head:
    def __init__(self):
        self.__cell = Rect(0, 0)
        self.__player_course = ''

    def get_pos(self):
        pos = self.__cell.get_pos()
        return [pos[0], pos[1]]

    def get_rect_pos(self):
        return self.__cell

    def get_course(self):
        return self.__player_course

    def change_pos(self):
        pos = self.__cell.get_pos()
        if self.__player_course == 'left':
            self.__cell.change_pos(pos[0] - 1, pos[1])

        elif self.__player_course == 'right':
            self.__cell.change_pos(pos[0] + 1, pos[1])

        elif self.__player_course == 'up':
            self.__cell.change_pos(pos[0], pos[1] - 1)

        elif self.__player_course == 'down':
            self.__cell.change_pos(pos[0], pos[1] + 1)

    def change_course(self, new_course:str):
        self.__player_course = new_course

    def check_apple_eating(self, apple:Apple):
        player_pos = self.__cell.get_pos()
        apple_pos = apple.get_pos()
        if player_pos[0] == apple_pos[0] and player_pos[1] == apple_pos[1]:
            return True
        else:
            return False

class Snake:
    def __init__(self, head_pos):
        self.__snake_pieces_list = [head_pos]
        self.__side = CELL_SIZE - CELL_SIZE // 5
        self.__offset = (CELL_SIZE - self.__side) // 2
        
    def snake_change_pos(self, new_pos):
        self.__snake_pieces_list.append(new_pos) 
        del self.__snake_pieces_list[0]
        
    def growing(self, eating_place):
        self.__snake_pieces_list.insert(0, eating_place)

    def get_pieces_list(self):
        return self.__snake_pieces_list

    def draw(self):
        piece_green_index = 255
        color_step = 255 // len(self.__snake_pieces_list)
        for piece in self.__snake_pieces_list:
            piece_color = (0, piece_green_index, 0)
            piece_green_index -= color_step
            piece_pos_in_pixels = cell_to_pixel(piece[0], piece[1]).get_pos()
            pygame.draw.rect(screen, piece_color, (self.__offset + piece_pos_in_pixels[0], self.__offset + piece_pos_in_pixels[1], self.__side, self.__side))

class Brain():
    def __init__(self, player_course:str, player_cell:Rect, snake:Snake):
        self.__player_course = player_course
        self.__player_cell = player_cell
        self.__snake = snake

    def change_pos(self, new_pos:list):
        self.__player_cell.change_pos(new_pos[0], new_pos[1])

    def __check_itself_cross_on_next_step(self):
        if self.__player_course == 'left':
            head_next_pos = [self.__player_cell.get_pos()[0] - 1, self.__player_cell.get_pos()[1]]
        
        elif self.__player_course == 'up':
            head_next_pos = [self.__player_cell.get_pos()[0], self.__player_cell.get_pos()[1] - 1]
        
        elif self.__player_course == 'down':
            head_next_pos = [self.__player_cell.get_pos()[0], self.__player_cell.get_pos()[1] + 1]

        elif self.__player_course == 'right':
            head_next_pos = [self.__player_cell.get_pos()[0] + 1, self.__player_cell.get_pos()[1]]

        if head_next_pos in self.__snake.get_pieces_list():
            return True
        
        else:
            return False

    def __check_crash_on_next_move(self):
        pos = self.__player_cell.get_pos()
        if pos[0] >= NUMBER_OF_CELLS - 1 or pos[1] >= NUMBER_OF_CELLS - 1:
            return True

        elif pos[0] <= 0 or pos[1] <= 0:
            return True 

        elif self.__check_itself_cross_on_next_step():
            return True

        else:
            return False

    def __move_to_apple(self, apple_pos:list):
        apple_x = apple_pos[0]
        apple_y = apple_pos[1]
        player_pos = self.__player_cell.get_pos()
        player_x = player_pos[0]
        player_y = player_pos[1]
        if player_x < apple_x:
            self.__player_course = 'right'
        elif player_x > apple_x:
            self.__player_course = 'left'
        else:
            if player_y < apple_y:
                self.__player_course = 'down'
            elif player_y > apple_y:
                self.__player_course = 'up'

    def __get_new_course_without_crash_in_walls(self, pos):
        last_player_course = self.__player_course
        new_player_course = last_player_course
        if pos[0] >= NUMBER_OF_CELLS - 1 and last_player_course == 'right':
            if pos[1] <= 0:
                new_player_course = 'down'
            else:
                new_player_course = 'up'
                
        elif pos[0] <= 0 and  last_player_course == 'left':
            if pos[1] <= 0:
                new_player_course = 'down'
            else:
                new_player_course = 'up' 

        elif pos[1] >= NUMBER_OF_CELLS - 1 and last_player_course == 'down':
            if pos[0] <= 0:
                new_player_course = 'right'
            else:
                new_player_course = 'left'

        elif pos[1] <= 0 and last_player_course == 'up':
            if pos[0] <= 0:
                new_player_course = 'right'
            else:
                new_player_course = 'left'

        return new_player_course

    def __check_visibility_for_x_move(self):
        head_pos = self.__player_cell.get_pos()
        snake_pieces_list = self.__snake.get_pieces_list()
        visible_cells_counter_for_up = 0
        visible_cells_counter_for_down = 0
        up_visibility = True
        down_visibility = True
        y = head_pos[1] - 1
        while y >= 0:
            if [head_pos[0], y] in snake_pieces_list:
                up_visibility = False
                break
            else:
                visible_cells_counter_for_up += 1
                y -= 1

        y = head_pos[1] + 1
        while y <= 9:
            if [head_pos[0], y] in snake_pieces_list:
                down_visibility = False
                break
            else:
                visible_cells_counter_for_down += 1
                y += 1

        return up_visibility, visible_cells_counter_for_up, down_visibility, visible_cells_counter_for_down

    def __check_visibility_for_y_move(self):
        head_pos = self.__player_cell.get_pos()
        snake_pieces_list = self.__snake.get_pieces_list()
        visible_cells_counter_for_left = 0
        visible_cells_counter_for_right = 0
        left_visibility = True
        right_visibility = True
        x = head_pos[0] - 1
        while x >= 0:
            if [x, head_pos[1]] in snake_pieces_list:
                left_visibility = False
                break
            else:
                visible_cells_counter_for_left += 1
                x -= 1

        x = head_pos[0] + 1
        while x <= 9:
            if [x, head_pos[1]] in snake_pieces_list:
                right_visibility = False
                break
            else:
                visible_cells_counter_for_right += 1
                x += 1 

        return left_visibility, visible_cells_counter_for_left, right_visibility, visible_cells_counter_for_right

    def __get_best_course_for_y_move(self):
        left_visibility, visible_cells_counter_for_left, right_visibility, visible_cells_counter_for_right = self.__check_visibility_for_y_move()
        best_course = ''

        if right_visibility and left_visibility:
            if visible_cells_counter_for_right >= visible_cells_counter_for_left:
                best_course = 'right'

            else:
                best_course = 'left'

        elif right_visibility:
            best_course = 'right'

        elif left_visibility:
            best_course = 'left'

        else:
            if visible_cells_counter_for_right >= visible_cells_counter_for_left:
                best_course = 'right'

            else:
                best_course = 'left'

        return best_course

    def __get_best_course_for_x_move(self):
        up_visibility, visible_cells_counter_for_up, down_visibility, visible_cells_counter_for_down = self.__check_visibility_for_x_move()
        best_course = ''

        if down_visibility and up_visibility:
            if visible_cells_counter_for_down >= visible_cells_counter_for_up:
                best_course = 'down'

            else:
                best_course = 'up'

        elif down_visibility:
            best_course = 'down'

        elif up_visibility:
            best_course = 'up'

        else:
            if visible_cells_counter_for_down >= visible_cells_counter_for_up:
                best_course = 'down'

            else:
                best_course = 'up'

        return best_course

    def __get_best_course_with_wall_visibility(self):
        best_course = ''

        if self.__player_course == 'right' or self.__player_course == 'left':
            best_course = self.__get_best_course_for_x_move()
             
        elif self.__player_course == 'up' or self.__player_course == 'down':
            best_course = self.__get_best_course_for_y_move()

        return best_course

    def get_new_course(self, apple:Apple):
        self.__move_to_apple(apple.get_pos())
        pos = self.__player_cell.get_pos()
        if self.__check_crash_on_next_move():
            if self.__check_itself_cross_on_next_step():
                self.__player_course = self.__get_best_course_with_wall_visibility()
            self.__player_course = self.__get_new_course_without_crash_in_walls(pos)
            
        return self.__player_course

    def check_reversal(self, last_course, new_course):
        if last_course == 'left' and new_course == 'right':
            return True

        elif last_course == 'right' and new_course == 'left':
            return True

        elif last_course == 'up' and new_course == 'down':
            return True

        elif last_course == 'down' and new_course == 'up':
            return True

        else:
            return False



player = Head()
snake = Snake(player.get_pos())
player.change_course('right')   
brain = Brain(player.get_course(), player.get_rect_pos(), snake)
apple_list = []
for i in range(1):
    apple_list.append(Apple(snake.get_pieces_list()))

fps_counter = 0

# Цикл игры
running = True
while running:
    fps_counter += 1
    if len(apple_list) == 0:
        apple_list.append(Apple(snake.get_pieces_list()))
        
    apple_for_eating = apple_list[0]
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    draw_field()
    player.change_course(brain.get_new_course(apple_for_eating))
    if check_game_over(snake.get_pieces_list(), player.get_course()):
        running = False

    eating = player.check_apple_eating(apple_for_eating)
    if eating:
        apple_list.remove(apple_for_eating)
        snake.growing(apple_for_eating.get_pos())

    if fps_counter % 3 == 0:
        player.change_pos()
        brain.change_pos(player.get_pos())
        snake.snake_change_pos(player.get_pos())

    snake.draw()
    for apple in apple_list:
        apple.draw()

    pygame.display.flip()

pygame.quit()