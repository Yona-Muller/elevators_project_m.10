import pygame
import json
import time
from floor import Floor
from elevator import Elevator

with open("data.json") as data_:
    data = json.load(data_)

class Building:
    def __init__(self, num_of_floors, num_of_elevators, canvas) -> None:
        self.__floors = [Floor(i) for i in range(num_of_floors)]
        self.__ele = [Elevator(i) for i in range(num_of_elevators)]
        # new attribute to offset drawing on world surface
        self.x_offset = 0

    def build_floors(self, screen, height, x_offset=0):
        for floor in self.__floors:
            # apply x_offset to floor drawing
            floor.draw_floor(screen, height - data["space_down"] - data["height_floor"], len(self.__floors) - 1, x_offset)
            height -= data["height_floor"]

    def build_ele(self, screen, height, x_pos=None, x_offset=0):
        if x_pos is None:
            x_pos = data["width_floor"] + data["space_left"] * 2
        for elevator in self.__ele:
            elevator.draw_ele(screen, x_pos + x_offset, height - data["space_down"] - data["height_ele"])
            x_pos += data["width_ele"]
   
    def draw_building(self, screen):
        # draw elevators
        for elevator in self.__ele:
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        # draw floors and timers
        for floor in self.__floors:
            floor.draw_floor2(screen)
            # existing timer code unchanged
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
        # unchanged
        min = float("inf"), None
        for elevator in self.__ele:
            ele_missions = elevator.tasks_time(floor.get_num())
            if ele_missions < min[0]: min = ele_missions, elevator
        min[1].insert_task((floor.get_image_rect().centery, floor.get_num()))
        floor.start_time = time.monotonic_ns()
        floor.set_timer(min[0])
        floor.set_ele_on_way(min[1])

    def update(self, screen, click_pos, new_click, x_offset=0):
        # handle input
        if new_click:
            for floor in self.__floors:
                rect = floor.get_image_rect()
                # adjust click bounds by x_offset
                if rect.centerx + data["width_floor"] * 0.1 + x_offset <= click_pos[0] <= rect.centerx + data["width_floor"] * 0.3 + x_offset \
                   and rect.centery - data["height_floor"] // 5 <= click_pos[1] <= rect.centery + data["height_floor"] // 3:
                    if not floor.get_ele_on_way():
                        floor.set_image(pygame.transform.scale(pygame.image.load(data["image_floor_g"]), (data["width_floor"], data["height_floor"])))
                        self.optimal_ele(floor)
        # clear building area
        screen.fill((180, 232, 193))
        # move elevators
        for elevator in self.__ele:
            elevator.move()
        # draw entire building at offset
        # combine floors and elevators draw calls within draw_building
        self.draw_building(screen)