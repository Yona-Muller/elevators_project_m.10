import pygame
import json
from Building import Building

with open("data.json") as data_:
    data = json.load(data_)

white = (255, 255, 255)

pygame.init()


class Game:
    """
    Represents the main game class for managing the elevator game.

    Attributes:
    - __num_floors (int): Number of floors in the building.
    - __num_ele (int): Number of elevators in the building.
    - __width (int): Width of the game screen.
    - __height (int): Height of the game screen.
    - __screen (pygame.Surface): Pygame surface for rendering the game.
    - __click_position (tuple): Last mouse click position on the screen.
    - __new_click (bool): Flag indicating a new mouse click.
    - __fullscreen (bool): Flag indicating fullscreen mode.
    """

    def __init__(self, num_floors, num_ele) -> None:
        """
        Initializes the Game instance with number of floors and elevators.

        Args:
        - num_floors (int): Number of floors in the building.
        - num_ele (int): Number of elevators in the building.
        """
        self.__num_floors = num_floors
        self.__num_ele = num_ele
        self.__width = data["space_left"] * 2 + \
            data["width_floor"] + num_ele * data["width_ele"]
        self.__height = data["space_down"] * \
            2 + num_floors * data["height_floor"]
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__click_position = None
        self.__new_click = False
        self.__fullscreen = False

    def boot_screen(self):
        """
        Sets up the initial game screen with building layout and starts the game loop.
        """
        pygame.display.set_caption("elevators game")
        self.__screen.fill(white)
        building = Building(self.__num_floors, self.__num_ele)
        building.build_floors(self.__screen, self.__height)
        building.build_ele(self.__screen, self.__height)
        self.screen_run(building)

    def screen_run(self, building: Building):
        """
        Main game loop that handles events, updates building state, and redraws the screen.

        Args:
        - building (Building): Instance of the Building class representing the game environment.
        """
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # Toggle fullscreen mode when 'F' key is pressed
                        self.__fullscreen = not self.__fullscreen
                        if self.__fullscreen:
                            pygame.display.set_mode(
                                (self.__width, self.__height), pygame.FULLSCREEN)
                        else:
                            pygame.display.set_mode(
                                (self.__width, self.__height))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__click_position = event.pos
                    self.__new_click = True
            building.move(self.__screen, self.__click_position,
                          self.__new_click)
            self.__new_click = False
            pygame.display.flip()


game = Game(17, 5)
game.boot_screen()
