import pygame
import json

with open("data.json") as data_:
    data = json.load(data_)

black = (0, 0, 0)


class Floor:
    def __init__(self, floor_num=None) -> None:
        self.__floor_num = floor_num
        self.__image = None
        self.__image_rect = None
        self.__timer = None
        self.__elevator_com = None

    def get_image(self):
        return self.__image
    
    def set_image(self, new_image):
        self.__image = new_image

    def get_image_rect(self):
        return self.__image_rect

    def get_floor_num(self) -> int:
        return self.__floor_num

    def get_timer(self):
        return self.__timer

    def set_timer(self, seconds):
        self.__timer = seconds

    def get_elevator_com(self):
        return self.__elevator_com
    
    def set_elevator_com(self, ele):
        self.__elevator_com = ele

    def draw_floor(self, screen, floor_locat):
        self.__image_floor = data["image_floor"]
        img = pygame.image.load(self.__image_floor)
        self.__image = pygame.transform.scale(
            img, (data["width_floor"], data["height_floor"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (data["space_left"], floor_locat)
        screen.blit(self.__image, self.__image_rect)
        pygame.draw.line(screen, black, [
                         data["space_left"], floor_locat + data["black_space"] / 2], [data["space_left"] + data["width_floor"], floor_locat + data["black_space"] / 2], data["black_space"])
        pygame.display.flip()
        font = pygame.font.Font(None, 30)
        text = font.render(
            f"{self.__floor_num}", True, (255, 255, 255))
        screen.blit(text, (data["width_floor"] * 0.72, self.__image_rect.centery - 4))

    def __str__(self) -> str:
        return f'{self.__floor_num}'
