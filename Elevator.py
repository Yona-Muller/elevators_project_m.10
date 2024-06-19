import pygame
import json
import time
from collections import deque

with open("data.json") as data_:
    data = json.load(data_)


class Elevator:
    """
    Represents an elevator object with various functionalities.

    Attributes:
    - __num (int): Identifier number of the elevator.
    - __current_floor (int): Current floor where the elevator is located.
    - __tasks_queue (deque): Queue of tasks (floor destinations) for the elevator.
    - __ele_status (dict): Dictionary to track the status of the elevator (standing, moving, doors open).
    - __time_task (float): Time required for the current task (movement between floors).
    - __start_time (float): Time when the current task started.
    - __image_rect (pygame.Rect): Rectangle defining the position and size of the elevator's image on the screen.
    - __image (pygame.Surface): Image of the elevator.
    - __time_left (float): Remaining time for the current task.
    - __time_tasks (float): Total time spent on all tasks.
    """

    def __init__(self, num) -> None:
        """
        Initializes an elevator with its identifier number and default attributes.

        Args:
        - num (int): Identifier number of the elevator.
        """
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
        """
        Returns the image of the elevator.

        Returns:
        - pygame.Surface: Image of the elevator.
        """
        return self.__image

    def get_image_rect(self):
        """
        Returns the rectangle defining the position and size of the elevator's image.

        Returns:
        - pygame.Rect: Rectangle defining the position and size of the elevator's image.
        """
        return self.__image_rect

    def get_num(self):
        """
        Returns the identifier number of the elevator.

        Returns:
        - int: Identifier number of the elevator.
        """
        return self.__num

    def get_ele_status(self, key):
        """
        Returns the value of a specific status key from the elevator's status dictionary.

        Args:
        - key (str): Key of the status to retrieve.

        Returns:
        - bool: Value of the specified status key.
        """
        return self.__ele_status[key]

    def set_ele_status(self, key, value):
        """
        Sets the value of a specific status key in the elevator's status dictionary.

        Args:
        - key (str): Key of the status to set.
        - value (bool): Value to set for the specified status key.
        """
        self.__ele_status[key] = value

    def ding(self):
        """
        Plays a ding sound to indicate the elevator has reached a floor.
        """
        sound_file = data["ding"]
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def insert_task(self, task):
        """
        Inserts a new task (floor destination) into the elevator's task queue.

        Args:
        - task (tuple): Tuple containing (elevator center, floor number) to be added to the task queue.
        """
        if not self.__tasks_queue:
            self.__time_tasks += abs(task[1] - self.__current_floor) * 0.5 + 2
        else:
            self.__time_tasks += abs(task[1] - self.__tasks_queue[-1][1]) * 0.5 + 2
        self.__tasks_queue.append(task)

    def pop_task(self):
        """
        Removes and returns the next task (floor destination) from the elevator's task queue.

        Returns:
        - tuple: Tuple containing (elevator center, floor number) of the next task.
        """
        self.__time_tasks -= abs(self.__current_floor - self.__tasks_queue[0][1]) * 0.5 + 2
        self.__time_task = abs(self.__current_floor - self.__tasks_queue[0][1]) * 0.5
        self.__current_floor = self.__tasks_queue[0][1]
        self.__ele_status["standing"] = False
        self.__start_time = time.monotonic_ns()
        return self.__tasks_queue.popleft()

    def tasks_time(self, floor):
        """
        Calculates the time required for the elevator to reach a specific floor.

        Args:
        - floor (int): Floor number to calculate the time to reach.

        Returns:
        - float: Time in seconds required for the elevator to reach the specified floor.
        """
        if self.__ele_status["standing"]:
            return abs(self.__current_floor - floor) * 0.5
        if not self.__tasks_queue:
            if self.__ele_status["doors open"]:
                return abs(self.__current_floor - floor) * 0.5 + 2 - (time.monotonic_ns() - self.__ele_status["doors open"])/10**9 + self.__time_left
            else:
                return abs(self.__current_floor - floor) * 0.5 + 2 + self.__time_left
        else:
            if self.__ele_status["doors open"]:
                return abs(self.__tasks_queue[-1][1] - floor) * 0.5 + 2 - (time.monotonic_ns() - self.__ele_status["doors open"])/10**9 + self.__time_tasks + self.__time_left
            else:
                return abs(self.__tasks_queue[-1][1] - floor) * 0.5 + 2 + self.__time_tasks + self.__time_left

    def move(self):
        """
        Moves the elevator based on its current tasks and status.
        """
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
        """
        Draws the elevator on the screen at a specific position.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        - width (int): X-coordinate position to draw the elevator.
        - height (int): Y-coordinate position to draw the elevator.
        """
        image_elevator = data["image_ele"]
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(
            img, (data["width_ele"], data["height_ele"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (width, height)
        screen.blit(self.__image, self.__image_rect)
