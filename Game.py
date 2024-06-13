import pygame
import json
from Building import Building

with open("data.json") as data_:
    data = json.load(data_)

white = (255, 255, 255)

pygame.init()

class Game:
    def __init__(self, num_floors, num_ele) -> None:
        self.__num_floors = num_floors
        self.__num_ele = num_ele
        self.__width = data["space_left"] * 2 + data["width_floor"] + num_ele * data["width_ele"]
        self.__height = data["space_down"] * 2 + num_floors * data["height_floor"]
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__click_position = None
        self.__new_click = False

    def boot_screen(self):
        pygame.display.set_caption("elevators game")
        self.__screen.fill(white)
        building = Building(self.__num_floors, self.__num_ele)
        building.build_floors(self.__screen, self.__height)
        building.build_ele(self.__screen, self.__height)
        self.screen_run(building)

    def screen_run(self, building: Building):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__click_position = event.pos
                    self.__new_click = True
            building.move(self.__screen, self.__click_position, self.__new_click)
            self.__new_click = False
            pygame.display.flip()

game = Game(20, 5)
game.boot_screen()