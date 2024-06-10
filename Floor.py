import pygame
import json

with open("data.json") as data_:
    data = json.load(data_)

black = (0, 0, 0)
white = (255, 255, 255)

class Floor:
    def __init__(self, num) -> None:
        self.__num = num
        self.__image = data["image_floor"]
        self.__image_rect = None
        self.__floor_status = {"ele_on_way": False, "ele_on_floor": False, "floor_emp": True}
        self.__timer = None

import json

with open("data.json") as data_:
    data = json.load(data_)

black = (0, 0, 0)
white = (255, 255, 255)

class Floor:
    def __init__(self, num) -> None:
        self.__num = num
        self.__image = data["image_floor"]
        self.__image_rect = None
        self.__floor_status = {"ele_on_way": False, "ele_on_floor": False, "floor_emp": True}
        self.__timer = None

    def get_image_rect(self):
        return self.__image_rect
    
    def get_floor_status(self):
        return self.__floor_status
        
    def set_floor_status(self, key):
        self.__floor_status[key] = True if self.__floor_status[key] == False else False

    def draw_floor(self, screen, height, num_floors):
        img = pygame.image.load(self.__image)
        self.__image = pygame.transform.scale(img, (data["width_floor"], data["height_floor"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (data["space_left"], height)
        screen.blit(self.__image, self.__image_rect)
        if num_floors != self.__num:
            pygame.draw.line(screen, black, [data["space_left"], height + data["black_space"
                            ] / 2], [data["space_left"] + data["width_floor"], height + data["black_space"] / 2], data["black_space"])
        font = pygame.font.Font(None, data["height_floor"] // 2)
        text = font.render(f"{self.__num}", True, white)
        screen.blit(text, (data["width_floor"] * 0.72, self.__image_rect.centery - 4))
    
    def get_floor_status(self):
        return self.__floor_status
        
    def set_floor_status(self, key):
        self.__floor_status[key] = True if self.__floor_status[key] == False else False

    def draw_floor(self, screen, height, num_floors):
        img = pygame.image.load(self.__image)
        self.__image = pygame.transform.scale(img, (data["width_floor"], data["height_floor"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (data["space_left"], height)
        screen.blit(self.__image, self.__image_rect)
        if num_floors != self.__num:
            pygame.draw.line(screen, black, [data["space_left"], height + data["black_space"
                            ] / 2], [data["space_left"] + data["width_floor"], height + data["black_space"] / 2], data["black_space"])
        font = pygame.font.Font(None, data["height_floor"] // 2)
        text = font.render(f"{self.__num}", True, white)
        screen.blit(text, (data["width_floor"] * 0.72, self.__image_rect.centery - 4))