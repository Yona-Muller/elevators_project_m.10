import pygame
import json
from collections import deque

with open("data.json") as data_:
    data = json.load(data_)


class Elevator:
    def __init__(self, num) -> None:
        self.__num = num
        self.__current_floor = 0
        self.__tasks_queue = deque([])
        self.__ele_status = {"standing": True,
                             "moving": False, "doors_open": False}

    def insert_task(self, task):
        self.__tasks_queue.append(task)

    def pop_task(self):
        return self.__tasks_queue.popleft()

    def tasks_time(self, floor):
        if self.__ele_status["standing"]:
            return abs(self.__current_floor - floor) * 0.5
        return abs(self.__current_floor - floor) * 0.5 if not self.__tasks_queue else abs(self.__tasks_queue[-1][0] - floor) * 0.5 + self.__tasks_queue[-1][1]

    def draw_ele(self, screen, width, height):
        image_elevator = data["image_ele"]
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(
            img, (data["width_ele"], data["height_ele"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (width, height)
        screen.blit(self.__image, self.__image_rect)
