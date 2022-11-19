import pygame
import random
from Game_math import Rectangle, Point
import typing

cannon_surf = pygame.image.load(r'.\resources\cannon.png')
wheel_surf = pygame.image.load(r'.\resources\new_wheel.png')

wheel_scale = pygame.transform.scale(wheel_surf, (int(wheel_surf.get_width() // 3), int(wheel_surf.get_height() // 3)))
cannon_scale = pygame.transform.scale(cannon_surf, (int(cannon_surf.get_width() // 3), int(cannon_surf.get_height() // 3)))

class Cannon:
    def __init__(self, x, Game_width, Game_height, screen):
        self.__x = x
        #cоздание объектов
        self.cannon_rect = cannon_scale.get_rect(midbottom = (self.__x, 0))
        self.__wheel_offset = int(self.cannon_rect.width / 4)
        self.__game_width = Game_width
        self.__game_height = Game_height
        self.__game_screen = screen

        #постановка пушки и колес на правильную высоту
        cannon_midbottom_y = self.__game_height - wheel_scale.get_height() / 2
        self.cannon_rect = cannon_scale.get_rect(midbottom = (self.__x, cannon_midbottom_y))
        self.left_wheel = Wheel(self.__x - self.__wheel_offset, 0, self.__game_height, self.__game_screen)
        self.right_wheel = Wheel(self.__x + self.__wheel_offset, 0, self.__game_height, self.__game_screen)
        self.__hits_counter = 0
    
    def draw_cannon(self):
        self.__game_screen.blit(cannon_scale, self.cannon_rect)   
        self.left_wheel.draw_wheel()
        self.right_wheel.draw_wheel()                       

    def add_hit(self, cannon_level):
        self.__hits_counter += 1 * cannon_level

    def get_n_hits(self):
        return self.__hits_counter

    def get_position(self):
        return self.__x
    
    def move(self, offset):
        self.__set_cannon_position(self.get_position() + offset)

    def clamp_pos_by_window(self):
        if self.cannon_rect.left < 2:
            self.__set_cannon_position(2 + self.cannon_rect.width // 2)
        if self.cannon_rect.right > self.__game_width - 2:
            self.__set_cannon_position(self.__game_width - 2 - self.cannon_rect.width // 2)

    def get_rects_under_cannon(self):
        #нижняя часть пушки
        down_rect_x = self.cannon_rect.left
        down_rect_y = self.cannon_rect.bottom - self.cannon_rect.height // 4
        down_rect_width = self.cannon_rect.width
        down_rect_height = self.cannon_rect.height // 4
        down_rect = Rectangle(down_rect_x, down_rect_y, down_rect_width, down_rect_height)
        #верхняя часть пушки
        top_rect_x = self.cannon_rect.left + self.cannon_rect.width // 6
        top_rect_y = self.cannon_rect.top
        top_rect_width = self.cannon_rect.width // 6 * 4
        top_rect_height = self.cannon_rect.height - down_rect_height
        top_rect = Rectangle(top_rect_x, top_rect_y, top_rect_width, top_rect_height)
        return [top_rect, down_rect]

    def draw_fire_while_shoot(self, scale_fire):
        fire_rect = scale_fire.get_rect(midbottom = (self.__x, self.cannon_rect.top))
        self.__game_screen.blit(scale_fire, fire_rect)

    def shooting(self, bullets_list):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if len(bullets_list) == 0:   
                bullets_list.append(Bullet(self.__game_screen, Point(self.cannon_rect.centerx, self.cannon_rect.top)))
            elif bullets_list[-1].get_position()[1] + 30 <= self.cannon_rect.top:
                bullets_list.append(Bullet(self.__game_screen, Point(self.cannon_rect.centerx, self.cannon_rect.top)))
            return True     

        else:
            return False

    def __set_cannon_position(self, shift_from_left_edge):
        self.__x = shift_from_left_edge 
        self.cannon_rect.midbottom = [self.__x, self.cannon_rect.bottom]
        self.left_wheel.set_wheel_position(self.__x - self.__wheel_offset)
        self.right_wheel.set_wheel_position(self.__x + self.__wheel_offset)    

class Wheel(pygame.sprite.Sprite):
    def __init__(self, x, angle, Game_height, screen):
        super().__init__()
        self.__x = x
        self.__game_height = Game_height
        self.__game_screen = screen
        self.wheel_rect = wheel_scale.get_rect(midbottom = (self.__x, self.__game_height))
        self.angle_rotate = angle
        
    def set_wheel_position(self, x):
        self.__x = x
        self.wheel_rect.centerx = self.__x

    def rotate_by(self, angle):
        self.angle_rotate += angle
        self.angle_rotate %= 360
    
    def draw_wheel(self):
        rotated_wheel = self.__wheels_rotation()
        self.__game_screen.blit(rotated_wheel[0], rotated_wheel[1])
      
    def __wheels_rotation(self):
        rot_image = pygame.transform.rotate(wheel_scale, self.angle_rotate)
        rot_rect = rot_image.get_rect(center = self.wheel_rect.center)
        return (rot_image, rot_rect)


class Bullet:
    def __init__(self, screen, pos:Point):
        self.__x = pos.x
        self.__y = pos.y        
        self.width = 4
        self.height = 10
        self.__game_screen = screen

    def draw_bullet(self):
        pygame.draw.rect(self.__game_screen, (67, 67, 67), (self.__x - self.width // 2, self.__y, self.width, self.height))

    def move(self, speed):
        self.__y -= speed
 
    def get_position(self):
        return (self.__x, self.__y)