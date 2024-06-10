import pygame
from class_building import Building
import json


with open("data.json") as data_:
    data = json.load(data_)

num_floors = int(input("choose the number of floors: "))
while not 0 < num_floors <= 100:
    num_floors = int(input("choose a number of floors between 1 in 100: "))
num_elevators = int(input("choose the number of elevators: "))
while not 0 < num_elevators <= 15:
    num_elevators = int(
        input("choose a number of elevators between 1 in 15: "))
    
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode(
            (game.__width, game.__height), pygame.FULLSCREEN)
        game.__screen.fill((255, 255, 255))
        building = Building(num_floors, num_elevators)
        building.build_floors(game.__screen, game.__width, game.__height)
        building.build_elevators(game.__screen, game.__height)
    else:
        pygame.display.set_mode((game.__width, game.__height))
        game.__screen.fill((255, 255, 255))
        building = Building(num_floors, num_elevators)
        building.build_floors(game.__screen, game.__width, game.__height)
        building.build_elevators(game.__screen, game.__height)  

pygame.init()


class Game:
    def __init__(self) -> None:
        self.__width = data["space_left"] * 2 + \
            data["width_floor"] + num_elevators * data["width_ele"]
        self.__height = data["space_down"] * \
            2 + num_floors * data["height_floor"]
        self.__white = (255, 255, 255)
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__target_position = None
        self.__click_position = None
        self.__fullscreen = False

    def boot_screen(self):
        pygame.display.set_caption("elevators game")
        self.__screen.fill(self.__white)
        # pygame.display.flip()

        building = Building(num_floors, num_elevators)
        building.build_floors(self.__screen, self.__width, self.__height)
        building.build_elevators(self.__screen, self.__height)
        self.screen_run(building)

    

    def screen_run(self, building):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # Toggle fullscreen mode when 'F' key is pressed
                        toggle_fullscreen()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__click_position = event.pos
                    new_click = True

            if self.__click_position:
                finished = building.move(
                    self.__screen, self.__click_position, new_click)
                new_click = False
                # if finished: is_door_open = False
                pygame.display.flip()

                # Cap the frame rate
                pygame.time.Clock().tick(60)


game = Game()
game.boot_screen()
