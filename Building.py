import pygame
import json
import time
from Floor import Floor
from Elevator import Elevator

with open("data.json") as data_:
    data = json.load(data_)

class Building:
    def __init__(self, num_floors, num_ele) -> None:
        self.__floors = [Floor(i) for i in range(num_floors)]
        self.__ele = [Elevator(i) for i in range(num_ele)]

    def build_floors(self, screen, height):
        for floor in self.__floors:
            floor.draw_floor(
                screen, height - data["space_down"] - data["height_floor"], len(self.__floors) - 1)
            height -= data["height_floor"]

    def build_ele(self, screen, height, x_pos=data["width_floor"] + data["space_left"] * 2):
        for elevator in self.__ele:
            elevator.draw_ele(screen, x_pos, height -
                              data["space_down"] - data["height_ele"])
            x_pos += data["width_ele"]
   
    def draw_building(self, screen):
        for elevator in self.__ele:# put it in class Elevator
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        for floor in self.__floors:# put it in class Floor
            screen.blit(floor.get_image(), floor.get_image_rect())
            font = pygame.font.Font(None, data["width_floor"] // 5)
            text = font.render(
                f"{floor.get_num()}", True, (255, 255, 255))
            screen.blit(text, (data["width_floor"] * 0.73, floor.get_image_rect().centery - 4))
            if floor.get_floor_status("ele_on_way"):
                timer = floor.get_timer() - (time.monotonic_ns() - floor.start_time) / 10**9
                if timer >= 0:
                    font = pygame.font.Font(None, data["width_floor"] // 4)
                    text = font.render(
                        f"{int(timer // 1):02}:{int((timer % 1) * 100):02}", True, (0, 0, 0))
                    screen.blit(text, (20, floor.get_image_rect().centery - 7))
                elif floor.get_floor_status("ele_on_way").get_ele_status("doors open"):
                    if (time.monotonic_ns() - floor.get_floor_status("ele_on_way").get_ele_status("doors open")) / 10**9 < 2:
                        font = pygame.font.Font(None, data["width_floor"] // 9)
                        text = font.render("doors open!", True, (70, 143, 34))
                        screen.blit(text, (20, floor.get_image_rect().centery))
                        # floor.set_floor_status("ele_on_floor", True)
                    else:
                        floor.get_floor_status("ele_on_way").set_ele_status("standing", True)
                        floor.set_floor_status("ele_on_way", False)

    def optimal_ele(self, floor: Floor):
        min = float("inf"), None
        for elevator in self.__ele:
            ele_missions = elevator.tasks_time(floor.get_num())
            if ele_missions < min[0]: min = ele_missions, elevator
        min[1].insert_task((floor.get_image_rect().centery, floor.get_num()))
        floor.start_time = time.monotonic_ns()
        floor.set_timer(min[0])
        floor.set_floor_status("ele_on_way", min[1])
        print((min[1].get_num(), min[0]))


    def move(self, screen, click_pos, new_click):
        if new_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx <= click_pos[0] <= floor.get_image_rect().centerx + data["width_floor"
                    ] * 1.3 and floor.get_image_rect().centery - data["width_floor"] // 20 <= click_pos[1] <= floor.get_image_rect().centery + data["width_floor"] // 20:
                    if not floor.get_floor_status("ele_on_way") and not floor.get_floor_status("ele_on_floor"):
                        self.optimal_ele(floor)
                        # time.sleep(3)
        screen.fill((255, 255, 255))
        for elevator in self.__ele:
            elevator.move()
        self.draw_building(screen)

