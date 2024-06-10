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

    def optimal_ele(self, floor: Floor):
        min = float("inf"), None
        for elevator in self.__ele:
            ele_missions = elevator.tasks_time(floor)
            if ele_missions < min[0]: min = ele_missions, elevator
        min[1].insert_task((floor, min[0]))
        floor.start_time(time.monotonic_ns())
        floor.set_timer(min[0])
        floor.set_floor_status("ele_on_way", min[1])


    def move(self, screen, click_pos, new_click):
        if new_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx + data["width_floor"] // 3 <= click_pos[0] <= floor.get_image_rect().centerx + data["width_floor"
                    ] * 1.3 and floor.get_image_rect().centery - data["width_floor"] // 4 <= click_pos[1] <= floor.get_image_rect().centery + data["width_floor"] // 4:
                    if not floor.get_floor_status()["ele_on_way"] and not floor.get_floor_status()["ele_on_floor"]:
                        self.optimal_ele(floor)
        

a = time.monotonic_ns() // 10 ** 8
