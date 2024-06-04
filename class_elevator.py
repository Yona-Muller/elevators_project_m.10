import pygame
from collections import deque


class Elevator:
    def __init__(self, num_elevator) -> None:
        self.__num_elevator = num_elevator
        self.__image = None
        self.__image_rect = None
        self.__elevator_floor = 0
        self.__tasks_queue = deque([])
        self.__time_tasks = 0
        self.__elevator_moving = False
        self.__moving_to = None
        self.__moving_to_floor = None

    def get_num_elevator(self):
        return self.__num_elevator

    def get_image(self):
        return self.__image

    def get_image_rect(self):
        return self.__image_rect

    def set_image_rect(self, item):
        self.__image_rect = item

    def get_elevator_floor(self):
        return self.__elevator_floor
    
    def set_elevator_floor(self, now_floor):
        self.__elevator_floor = now_floor

    def get_lest_task(self):
        return self.__tasks_queue[-1]

    def get_time_tasks(self):
        return self.__time_tasks
    
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

    def moving(self):
        return self.__elevator_moving

    def insert_task(self, task):
        if self.no_tasks:
            self.__time_tasks += abs(self.__elevator_floor - task) * 0.5
        else:
            self.__time_tasks += abs(self.__tasks_queue[-1] - task) * 0.5
        self.__tasks_queue.append(task)

    def pop_task(self):
        self.__time_tasks -= abs(self.__elevator_floor - self.__tasks_queue[0]) * 0.5
        return self.__tasks_queue.popleft()

    def image_elevator(self, screen, elevator_loc_width, elevator_loc_height):
        image_elevator = "elv.png"
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(img, (82, 82))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (elevator_loc_width, elevator_loc_height)
        screen.blit(self.__image, self.__image_rect)
        pygame.display.flip()
