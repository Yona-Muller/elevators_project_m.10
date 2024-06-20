import pygame
import json
import time
from Floor import Floor
from Elevator import Elevator

with open("data.json") as data_:
    data = json.load(data_)

class Building:
    """
    Initializes the building with the number of floors and elevators.

    Args:
    - num_floors (int): Number of floors in the building.
    - num_ele (int): Number of elevators in the building.
    """
    def __init__(self, num_floors, num_ele) -> None:
        self.__floors = [Floor(i) for i in range(num_floors)]
        self.__ele = [Elevator(i) for i in range(num_ele)]

    def build_floors(self, screen, height):
        """
        Constructs the floors of the building on the screen.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        - height (int): Initial height position to start drawing the floors.
        """
        for floor in self.__floors:
            floor.draw_floor(
                screen, height - data["space_down"] - data["height_floor"], len(self.__floors) - 1)
            height -= data["height_floor"]

    def build_ele(self, screen, height, x_pos=data["width_floor"] + data["space_left"] * 2):
        """
        Constructs the elevators of the building on the screen.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        - height (int): height position to drawing the elevators.
        - x_pos (int): Initial x-position to start drawing the first elevator.
        """
        for elevator in self.__ele:
            elevator.draw_ele(screen, x_pos, height - data["space_down"] - data["height_ele"])
            x_pos += data["width_ele"]
   
    def draw_building(self, screen):
        """
        Updates and draws the state of the building on the screen(with the timer in the right color of the button).

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        """
        for elevator in self.__ele:# put it in class Elevator
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        for floor in self.__floors:# put it in class Floor
            floor.draw_floor2(screen)
            if floor.get_ele_on_way():
                timer = floor.get_timer() - (time.monotonic_ns() - floor.start_time) / 10**9
                if timer >= 0:
                    font = pygame.font.Font(None, data["width_floor"] // 4)
                    text = font.render(
                        f"{int(timer // 1):02}:{int((timer % 1) * 100):02}", True, (0, 0, 0))
                    screen.blit(text, (20, floor.get_image_rect().centery - 7))
                elif floor.get_ele_on_way().get_ele_status("doors open"):
                    floor.set_image(pygame.transform.scale(pygame.image.load(data["image_floor"]), (data["width_floor"], data["height_floor"])))
                    if (time.monotonic_ns() - floor.get_ele_on_way().get_ele_status("doors open")) / 10**9 < 2:
                        font = pygame.font.Font(None, data["width_floor"] // 9)
                        text = font.render("doors open!", True, (70, 143, 34))
                        screen.blit(text, (20, floor.get_image_rect().centery))
                    else:
                        floor.get_ele_on_way().set_ele_status("standing", True)
                        floor.get_ele_on_way().set_ele_status("doors open", False)
                        floor.set_ele_on_way(False)

    def optimal_ele(self, floor: Floor):
        """
        Determines the optimal elevator to handle a request from a specific floor.

        Args:
        - floor (Floor): The floor object representing the floor requesting the elevator.
        """
        min = float("inf"), None
        for elevator in self.__ele:
            ele_missions = elevator.tasks_time(floor.get_num())
            if ele_missions < min[0]: min = ele_missions, elevator
        min[1].insert_task((floor.get_image_rect().centery, floor.get_num()))
        floor.start_time = time.monotonic_ns()
        floor.set_timer(min[0])
        floor.set_ele_on_way(min[1])


    def move(self, screen, click_pos, new_click):
        """
        Handles user input for interacting with the building (clicking on floors to request elevators),
        updates elevator movement, and redraws the building on the screen.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        - click_pos (tuple): Position of the mouse click on the screen.
        - new_click (bool): Flag indicating whether there is a new mouse click.
        """
        if new_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx + data["width_floor"] * 0.1 <= click_pos[0] <= floor.get_image_rect().centerx + data["width_floor"
                    ] * 0.3 and floor.get_image_rect().centery - data["height_floor"] // 5 <= click_pos[1] <= floor.get_image_rect().centery + data["height_floor"] // 3:
                    if not floor.get_ele_on_way():
                        floor.set_image(pygame.transform.scale(pygame.image.load(data["image_floor_g"]), (data["width_floor"], data["height_floor"])))
                        self.optimal_ele(floor)
        screen.fill((180, 232, 193))
        for elevator in self.__ele:
            elevator.move()
        self.draw_building(screen)

