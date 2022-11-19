import pygame
import random
import math
import os
from Game_math import Point

def is_inside_circle(x, y, circle_center, circle_r):
    dist = math.sqrt((circle_center[0] - x) ** 2 + (circle_center[1] - y) ** 2)
    if dist > circle_r:
        return False
    else:
        return True

def clamp(x, xmin = None, xmax = None):
    if xmin is not None and x < xmin:
        x = xmin

    if xmax is not None and x > xmax:
        x = xmax

    return x
         
class Falling_things():
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, picture, game_level, cannon_level):
        self.__cannon_force = cannon_level
        self.__game_level = game_level
        self.__screen_height = SCREEN_HEIGHT
        self.__screen_width = SCREEN_WIDTH
        self.__down_speed = 0
        self.__side_speed = random.uniform(-2, 2)
        file = os.path.join(os.getcwd(), "resources", "stone.png" )
        print("file ", file)
        self.__image = pygame.image.load(file)
        print("loaded ", file)
        #self.__image = pygame.image.load(picture)
        self.__scale_image = pygame.transform.scale(self.__image, (int(self.__image.get_width() // 6), int(self.__image.get_height() // 6)))
        self.__rect = self.__scale_image.get_rect(center = [random.randint(50, self.__screen_width - 50),  -50])
        self.__pos = Point(self.__rect.centerx, self.__rect.centery)
        self.__rotate_angle = 1
        self.__rotate_angle_for_1_frame = 1
        self.__cir_circle_r = int(self.__rect.height / 2)
        self.__one_bullet_force = 1 * self.__cannon_force
        #для цифры
        self.txt_number = random.randint(30, 45) * self.__game_level
        self.__font_size = 40
        self.__txt_color_delta_red = 0
        self.__txt_color_delta_green = int(170 / (self.txt_number / self.__one_bullet_force))
        self.__txt_color_delta_blue = int(255 / (self.txt_number / self.__one_bullet_force))
        self.__txt_color_index_red = 255
        self.__txt_color_index_green = 255
        self.__txt_color_index_blue = 255
        print("font ")

        self.__fontobj = pygame.font.Font(r'.\resources\18547.ttf', self.__font_size)
        print("font 1")
        self.__txt_color = (self.__txt_color_index_red, self.__txt_color_index_green, self.__txt_color_index_blue)
        self.__txt_image = self.__fontobj.render(str(self.txt_number), True, self.__txt_color)
        self.__txt_rect = self.__txt_image.get_rect()
        while self.__txt_rect.width >= self.__cir_circle_r * 2:
            self.__font_size -= 1
            self.__fontobj = pygame.font.SysFont('bodoniblack', self.__font_size)
            self.__txt_image = self.__fontobj.render(str(self.txt_number), True, self.__txt_color)
            self.__txt_rect = self.__txt_image.get_rect()
        self.__effect_state = 0
        
    def get_rect(self):
        return self.__rect

    def move(self, dt):
        a = random.randint(150, 300)
        dV = a * dt
        self.__down_speed += dV
        if self.__pos.y + self.__cir_circle_r >= self.__screen_height:
            self.__pos.y = self.__screen_height - self.__cir_circle_r
            self.__down_speed *= -0.90
            self.__rotate_angle_for_1_frame *= -1

        if self.__pos.x + self.__cir_circle_r >= self.__screen_width or self.__pos.x - self.__cir_circle_r <= 0:
            self.__side_speed *= -1
            self.__rotate_angle_for_1_frame *= -1

        self.__pos += Point(self.__side_speed, self.__down_speed * dt)        
        self.__rect.center = (self.__pos.x, self.__pos.y)
        self.__txt_rect.center = (self.__pos.x, self.__pos.y)

    def __clamp_zero(self, x):
        if x < 0:
            x = 0

        return x

    def hit(self):
        self.__txt_color_index_red = self.__clamp_zero(self.__txt_color_index_red - self.__txt_color_delta_red)
        self.__txt_color_index_green = self.__clamp_zero(self.__txt_color_index_green - self.__txt_color_delta_green)
        self.__txt_color_index_blue = self.__clamp_zero(self.__txt_color_index_blue - self.__txt_color_delta_blue)
        self.__txt_color = (self.__txt_color_index_red, self.__txt_color_index_green, self.__txt_color_index_blue) 
        self.txt_number -= self.__one_bullet_force
        self.txt_number = clamp(self.txt_number, xmin = 0)
        self.__update_image_for_number()
        self.__start_effect()

    def check_cross_bullet_and_thing(self, bullet):
        bullet_param = bullet.get_position()
        return is_inside_circle(bullet_param[0], bullet_param[1], self.__rect.center, self.__cir_circle_r) 

    def update(self):
        self.__update_rotation()
        self.__update_image_for_number()
        self.__update_effects()

    def draw(self, screen):
        rotated_image, rotated_n = self.__make_rotated_image()
        screen.blit(rotated_image, rotated_image.get_rect(center = self.__rect.center))
        screen.blit(rotated_n, rotated_n.get_rect(center = self.__rect.center))

    def __reduce_image(self, reduce_index):
        self.__scale_image = pygame.transform.scale(self.__image, (int(self.__image.get_width() // reduce_index), int(self.__image.get_height() // reduce_index)))
        self.__rect = self.__scale_image.get_rect(center = [self.__pos.x,  self.__pos.y])

    def __increase_image(self):
        self.__scale_image = pygame.transform.scale(self.__image, (int(self.__image.get_width() // 6), int(self.__image.get_height() // 6)))
        self.__rect = self.__scale_image.get_rect(center = [self.__pos.x,  self.__pos.y])

    def __update_rotation(self):
        self.__rotate_angle += self.__rotate_angle_for_1_frame
        self.__rotate_angle %= 360

    def __update_effects(self):
        if self.__effect_state <= 0:
            return
        self.__increase_image()
        self.__effect_state -=1

    def __start_effect(self):
        self.__effect_state = 2
        self.__reduce_image(6.5)

    def __make_rotated_image(self):
        return pygame.transform.rotate(self.__scale_image, self.__rotate_angle), pygame.transform.rotate(self.__txt_image, self.__rotate_angle)

    def __update_image_for_number(self):
        self.__txt_image = self.__fontobj.render(str(self.txt_number), True, self.__txt_color)
        self.__txt_rect = self.__txt_image.get_rect()