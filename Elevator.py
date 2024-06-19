import pygame
import json
import time
from collections import deque

with open("data.json") as data_:
    data = json.load(data_)


class Elevator:
    def __init__(self, num) -> None:
        self.__num = num
        self.__current_floor = 0
        self.__tasks_queue = deque([])
        self.__ele_status = {"standing": True,
                             "moving": False, "doors open": False}
        self.__time_task = None
        self.__start_time = None
        self.__image_rect = None
        self.__image = None
        self.__time_left = None
        self.__time_tasks = 0

    def get_image(self):
        return self.__image

    def get_image_rect(self):
        return self.__image_rect

    def get_num(self):
        return self.__num

    def get_ele_status(self, key):
        return self.__ele_status[key]

    def set_ele_status(self, key, value):
        self.__ele_status[key] = value

    def ding(self):
        sound_file = data["ding"]
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def insert_task(self, task):
        if not self.__tasks_queue:
            self.__time_tasks += abs(task[1] - self.__current_floor) * 0.5 + 2
        else:
            self.__time_tasks += abs(task[1] - self.__tasks_queue[-1][1]) * 0.5 + 2
        self.__tasks_queue.append(task)

    def pop_task(self):
        self.__time_tasks -= abs(self.__current_floor - self.__tasks_queue[0][1]) * 0.5 + 2
        self.__time_task = abs(self.__current_floor - self.__tasks_queue[0][1]) * 0.5
        self.__current_floor = self.__tasks_queue[0][1]
        self.__ele_status["standing"] = False
        self.__start_time = time.monotonic_ns()
        return self.__tasks_queue.popleft()

    def tasks_time(self, floor):
        if self.__ele_status["standing"]:
            return abs(self.__current_floor - floor) * 0.5
        if not self.__tasks_queue:
            if self.__ele_status["doors open"]:
                return abs(self.__current_floor - floor) * 0.5 + 2 - (time.monotonic_ns() - self.__ele_status["doors open"])//10**9 + self.__time_left
            else:
                return abs(self.__current_floor - floor) * 0.5 + 2 + self.__time_left
        else:
            if self.__ele_status["doors open"]:
                return abs(self.__tasks_queue[-1][1] - floor) * 0.5 + 2 - (time.monotonic_ns() - self.__ele_status["doors open"])//10**9 + self.__time_tasks + self.__time_left
            else:
                return abs(self.__tasks_queue[-1][1] - floor) * 0.5 + 2 + self.__time_tasks + self.__time_left

    def move(self):
        if self.__ele_status["standing"] and self.__tasks_queue:
            self.__ele_status["moving"] = self.pop_task()
        if self.__ele_status["moving"]:
            correct_time = time.monotonic_ns()
            time_passed = (correct_time - self.__start_time)/ 10**9
            self.__time_left = self.__time_task - time_passed
            if self.__image_rect.centery - self.__ele_status["moving"][0] > 0:
                self.__image_rect.centery = self.__ele_status["moving"][0] + (
                    self.__time_left * data["height_floor"] * 2)
            else:
                self.__image_rect.centery = self.__ele_status["moving"][0] - (
                    self.__time_left * data["height_floor"] * 2)
            if self.__ele_status["moving"][0] - 1 <= self.__image_rect.centery <= self.__ele_status["moving"][0] + 1:
                self.ding()
                self.__ele_status["moving"] = False
                self.__ele_status["doors open"] = time.monotonic_ns()

    def draw_ele(self, screen, width, height):
        image_elevator = data["image_ele"]
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(
            img, (data["width_ele"], data["height_ele"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (width, height)
        screen.blit(self.__image, self.__image_rect)
