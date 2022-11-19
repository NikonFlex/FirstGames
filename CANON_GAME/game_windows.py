import pygame
from Game_math import Rectangle, Point

def color_txt_changer(color_index, color_change_delta, lighting, fogging):
        if lighting:
            if color_index + color_change_delta <= 255:
                color_index += color_change_delta
            else:
                lighting = False
                fogging  = True

        if fogging:
            if color_index - color_change_delta >= 10:
                color_index -= color_change_delta
            else:
                lighting = True
                fogging = False

        return color_index, lighting, fogging

class Start_window:
    def __init__(self, screen, screen_width, screen_height, image, FPS_index, cannon_level):
        self.__window_width = screen_width
        self.__window_height = screen_height
        self.__screen = screen
        self.cannon_level = cannon_level
        self.__image = pygame.image.load(image)
        self.__flashing_txt_color_index = 0
        self.__color_change_delta = int(255 / (FPS_index))
        self.__fogging = False
        self.__lighting = True 

    def draw_start_window(self):
        self.__draw_game_title()
        self.__draw_cannon_level_index()
        self.__draw_cannon_for_start_window()
        self.__draw_flashing_txt_for_start()
        

    def __draw_game_title(self):
        self.__fontobj = pygame.font.SysFont('Agency FB', 40)
        self.__txt_image_for_name = self.__fontobj.render('CANNON GAME', True, (0, 2, 2))
        self.__txt_rect_for_name = self.__txt_image_for_name.get_rect(center = (self.__window_width / 2, 50))
        self.__screen.blit(self.__txt_image_for_name, self.__txt_rect_for_name)

    def __draw_cannon_level_index(self):
        self.__txt_image_for_cannon_level = self.__fontobj.render('Cannon level: ' + str(self.cannon_level), True, (0, 2, 2))
        self.__txt_rect_for_cannon_level = self.__txt_image_for_cannon_level.get_rect(center = (self.__window_width / 2, 100))
        self.__screen.blit(self.__txt_image_for_cannon_level, self.__txt_rect_for_cannon_level)

    def __draw_cannon_for_start_window(self):
        self.__scale_image = pygame.transform.scale(self.__image, (int(self.__image.get_width() // 6), int(self.__image.get_height() // 6)))
        self.__image_rect = self.__scale_image.get_rect(center = (self.__window_width / 2, self.__window_height / 2 - 50))
        self.__screen.blit(self.__scale_image, self.__image_rect)

    def __draw_flashing_txt_for_start(self):
        txt = 'TAP TO START'
        self.__flashing_txt_color_index, self.__lighting, self.__fogging = color_txt_changer(self.__flashing_txt_color_index, self.__color_change_delta, self.__lighting, self.__fogging)
        self.__fontobj = pygame.font.SysFont('Agency FB', 40)
        self.__txt_image = self.__fontobj.render(txt, True, (self.__flashing_txt_color_index, self.__flashing_txt_color_index, self.__flashing_txt_color_index))
        self.__txt_rect_for_name = self.__txt_image.get_rect(center = (self.__window_width / 2, self.__window_height - 150))
        self.__screen.blit(self.__txt_image, self.__txt_rect_for_name)

class Finish_window:
    def __init__(self, __screen, screen_width, screen_height, score, FPS_index, cannon_level, upgrade_cost):
        self.__window_width = screen_width
        self.__window_height = screen_height
        self.__screen = __screen
        self.__score = score
        self.__flashing_txt_color_index = 0
        self.__color_change_delta = int(255 / (FPS_index))
        self.__fogging = False
        self.__lighting = True
        self.__fontobj = pygame.font.SysFont('Agency FB', 40)
        self.upgrade_cost = upgrade_cost
        self.cannon_level = cannon_level
        self.__button = Rectangle(self.__window_width / 2 - 65, self.__window_height / 2 - 25, 130, 50)
    
    def draw_finish_window(self, mouse_button_down, click_event, complete_level):
        #отрисовка заднего фона
        pygame.draw.rect(self.__screen, (255, 255, 255), (0, 0, self.__window_width, self.__window_height))
        if complete_level:
            self.__draw_complete_level()
        self.__draw_score()
        self.__draw_flashing_txt_for_finish_window()
        self.__draw_button_for_imrove_cannon(mouse_button_down, click_event)
        self.__draw_cannon_level()
        self.__draw_upgrade_cost()

    def __draw_complete_level(self):
        txt = 'level complete'
        txt_image = self.__fontobj.render(txt, True, (0, 0, 0))
        txt_rect_for_name = txt_image.get_rect(midtop = (self.__window_width / 2, 7))
        self.__screen.blit(txt_image, txt_rect_for_name)

    def __draw_score(self):
        txt = 'SCORE ' + str(self.__score)
        txt_image = self.__fontobj.render(txt, True, (0, 0, 0))
        txt_rect_for_name = txt_image.get_rect(center = (self.__window_width / 2, self.__window_height / 2 - 200))
        self.__screen.blit(txt_image, txt_rect_for_name)

    def __draw_cannon_level(self):
        txt = 'CANNON LEVEL: ' + str(self.cannon_level)
        txt_cannon_level_image = self.__fontobj.render(txt, True, (0, 0, 0))
        txt_rect_for_cannon_level = txt_cannon_level_image.get_rect(center = (self.__window_width / 2, self.__window_height / 2 - 100))
        self.__screen.blit(txt_cannon_level_image, txt_rect_for_cannon_level)

    def __draw_upgrade_cost(self):
        txt = 'UPGRADE PRICE: ' + str(self.upgrade_cost)
        txt_cannon_level_image = self.__fontobj.render(txt, True, (0, 0, 0))
        txt_rect_for_cannon_level = txt_cannon_level_image.get_rect(center = (self.__window_width / 2, self.__window_height / 2 - 150))
        self.__screen.blit(txt_cannon_level_image, txt_rect_for_cannon_level)

    def __draw_flashing_txt_for_finish_window(self):
        txt = 'TAP TO RESTART'
        self.__flashing_txt_color_index, self.__lighting, self.__fogging = color_txt_changer(self.__flashing_txt_color_index, self.__color_change_delta, self.__lighting, self.__fogging)
        txt_image = self.__fontobj.render(txt, True, (self.__flashing_txt_color_index, self.__flashing_txt_color_index, self.__flashing_txt_color_index))
        txt_rect_for_name = txt_image.get_rect(center = (self.__window_width / 2, self.__window_height - 100))
        self.__screen.blit(txt_image, txt_rect_for_name)

    def the_mouse_intercect_the_button(self, mouse_pos):
        if self.__button.x + self.__button.width < mouse_pos[0] or mouse_pos[0] < self.__button.x:
            return False
        if self.__button.y + self.__button.height < mouse_pos[1] or mouse_pos[1] < self.__button.y:
            return False
        return True
       
    def __draw_button_for_imrove_cannon(self, mouse_pos, click_event):
        pygame.draw.rect(self.__screen, (129, 129, 129), (self.__button.x, self.__button.y, self.__button.width, self.__button.height))
        fontobj = pygame.font.SysFont('Agency FB', 30)
        txt_image = fontobj.render('UPGRADE', True, (0, 0, 0))
        txt_rect = txt_image.get_rect(center = (self.__window_width / 2, self.__window_height / 2))
        self.__screen.blit(txt_image, txt_rect)

        
