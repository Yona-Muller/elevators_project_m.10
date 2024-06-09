import pygame
from collections import deque
import json

with open("data.json") as data_:
    data = json.load(data_)

class Elevator:
    def __init__(self, num_elevator) -> None:
        self.__num_elevator = num_elevator
        self.__image = None
        self.__image_rect = None
        self.__current_floor = 0
        self.__tasks_queue = deque([])
        self.__time_tasks = 0
        self.__elevator_moving = False
        self.__moving_to = None
        self.__moving_to_floor = None
        self.__is_door_open = False
        self.__color_timer = (0, 0, 0) #if self.__is_door_open else (0, 255, 0)

    def get_num_elevator(self):
        return self.__num_elevator

    def get_image(self):
        return self.__image

    def get_image_rect(self):
        return self.__image_rect

    def set_image_rect(self, item):
        self.__image_rect = item

    def get_current_floor(self):
        return self.__current_floor
    
    def set_current_floor(self, now_floor):
        self.__current_floor = now_floor

    def get_lest_task(self):
        return self.__tasks_queue[-1]

    def get_time_tasks(self):
        return self.__time_tasks
    
    def get_is_door_open(self):
        return self.__is_door_open
    
    def set_is_door_open(self):
        if self.__is_door_open:
            self.__is_door_open = False
            self.__color_timer = (0, 0, 0)
        else:
            self.__is_door_open = True
            self.__color_timer = (70, 143, 34)
    
    def get_color_timer(self):
        return self.__color_timer

    def no_tasks(self):
        return True if len(self.__tasks_queue) == 0 else False
    
    def stop_or_start_moving(self):
        if not self.__elevator_moving:
            self.__elevator_moving = True

        else:
            self.__elevator_moving = False

    def set_moving_to(self, dist):
        self.__moving_to = dist

    def get_moving_to(self):
        return self.__moving_to
    
    def get_moving_to_floor(self):
        return self.__moving_to_floor
    
    def set_moving_to_floor(self, num_floor):
        self.__moving_to_floor = num_floor

    def get_elevator_moving(self):
        return self.__elevator_moving

    def moving(self):
        return self.__elevator_moving

    def insert_task(self, task):
        if self.no_tasks:
            self.__time_tasks += abs(self.__current_floor + 1 - task) * 0.5 + 2
        else:
            self.__time_tasks += abs(self.__tasks_queue[-1] + 1 - task) * 0.5 + 2
        self.__tasks_queue.append(task)

    def pop_task(self):
        self.__time_tasks -= abs(self.__current_floor + 1 - self.__tasks_queue[0]) * 0.5
        return self.__tasks_queue.popleft()
    
    def move_ele(self):
        if not self.__elevator_moving and not self.no_tasks():
            self.__moving_to_floor = self.pop_task()
            self.__floors[self.get_moving_to_floor()].set_timer(
                abs(self.get_moving_to_floor() - self.get_current_floor()) * 0.5)
            self.stop_or_start_moving()
            self.set_moving_to(self.__floors[self.get_moving_to_floor()].get_image_rect(
            ).centery - self.get_image_rect().centery)
        if self.moving() and self.get_moving_to() > data["speed"]:
            self.get_image_rect().centery += data["speed"]
            self.set_moving_to(self.get_moving_to() - data["speed"])
        if self.moving() and self.get_moving_to() < data["speed"]:
            self.get_image_rect().centery -= data["speed"]
            self.set_moving_to(self.get_moving_to() + data["speed"])
        if self.moving() and data["speed"] + 2 >= self.get_moving_to() >= -data["speed"] - 2:
            if not self.get_is_door_open():
                sound_file = data["ding"]
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                self.__floors[self.get_moving_to_floor()].set_timer(2)
                self.set_is_door_open()
                self.__floors[self.get_moving_to_floor()].set_image(pygame.transform.scale(
                    pygame.image.load(data["image_floor"]), (data["width_floor"], data["height_floor"])))
            elif self.__floors[self.get_moving_to_floor()].get_timer() <= 0:
                self.stop_or_start_moving()
                self.set_current_floor(self.get_moving_to_floor())
                self.__floors[self.get_moving_to_floor()
                                ].set_timer(None)
                self.set_moving_to_floor(None)
                self.set_is_door_open()

    def draw_elevator(self, screen, elevator_loc_width, elevator_loc_height):
        image_elevator = data["image_ele"]
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(img, (data["width_ele"], data["height_ele"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (elevator_loc_width, elevator_loc_height)
        screen.blit(self.__image, self.__image_rect)
        pygame.display.flip()
