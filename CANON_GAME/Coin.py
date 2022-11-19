import pygame
import random

class Coin:
    def __init__(self, falling_thing_x, falling_thing_y, Game_screen, Game_screen_width, Game_screen_height):
        self.n_bounce = 0
        self.move = True
        self.__x = falling_thing_x
        self.__y = falling_thing_y
        self.__screen = Game_screen
        self.__screen_width = Game_screen_width
        self.__screen_height = Game_screen_height
        self.__coin_cir_r = 13
        self.__down_speed = 0
        self.__side_speed = random.uniform(-2, 2)
        self.__coin_color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def draw_coin(self):
        pygame.draw.circle(self.__screen, self.__coin_color, (int(self.__x), int(self.__y)), self.__coin_cir_r)

    def get_coin_position_and_size(self):
        return (self.__x - self.__coin_cir_r / 2, self.__y - self.__coin_cir_r / 2), self.__coin_cir_r

    def coin_update(self, dt):
        if self.n_bounce == 4:
            self.move = False
            
        if self.move:
            a = random.randint(150, 300)
            dV = a * dt
            self.__down_speed += dV
            if self.__y + self.__coin_cir_r >= self.__screen_height:
                self.__y = self.__screen_height - self.__coin_cir_r
                self.__down_speed *= -0.3
                self.n_bounce += 1

            if self.__x + self.__coin_cir_r >= self.__screen_width or self.__x - self.__coin_cir_r <= 0:
                self.__side_speed *= -1
                
            self.__x, self.__y = self.__x + self.__side_speed, self.__y + self.__down_speed * dt