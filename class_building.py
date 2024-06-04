import pygame
from class_floor import Floor
from class_elevator import Elevator
import json

with open("data.json") as data_:
    data = json.load(data_)


white = (255, 255, 255)
black = (0, 0, 0)
space_left_side = 10
speed = 3


class Building:
    def __init__(self, num_floors, num_elevators) -> None:
        self.__floors = [Floor(i) for i in range(num_floors)]
        self.__elevators = [Elevator(i) for i in range(num_elevators)]

    def build_floors(self, screen, width, height):
        for floor in self.__floors:
            floor.image_floor(screen, height - data["space_down"])
            height -= data["height_floor"]
        pygame.draw.line(screen, white, [space_left_side, height], [310, height], 7)

    def build_elevators(self, screen, height, x=data["space_left"] * 2 + data["width_floor"]):
        for elevator in self.__elevators:
            elevator.image_elevator(screen, x, height - data["space_down"])
            x += data["width_ele"]

    def optimal_elevator(self, target_floor: Floor):
        min = float("inf"), -1
        for elevator in self.__elevators:
            if not elevator.no_tasks():
                time_staks_elevator = elevator.get_time_tasks(
                ) + abs(elevator.get_lest_task() - target_floor.get_floor_num())
                if time_staks_elevator < min[0]:
                    min = time_staks_elevator, elevator.get_num_elevator()
            else:
                time_staks_elevator = abs(
                    elevator.get_elevator_floor() - target_floor.get_floor_num()) * 0.5
                if time_staks_elevator < min[0]:
                    min = time_staks_elevator, elevator.get_num_elevator()
        self.__elevators[min[1]].insert_task(target_floor.get_floor_num())

    def drawing_floors_and_elevators(self, screen):
        for elevator in self.__elevators:
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        for floor in self.__floors:
            screen.blit(floor.get_image(), floor.get_image_rect())
            if floor.get_timer():
                font = pygame.font.Font(None, 40)
                text = font.render(
                    f"{int(floor.get_timer() // 1)}:{int((floor.get_timer() % 1) * 100)}", True, (0, 0, 0))
                screen.blit(text, (30, floor.get_image_rect().centery))
        for i in range(len(self.__floors) - 1):
            pygame.draw.line(screen, black, [space_left_side, self.__floors[i].get_image_rect().top + data["black_space"] / 2],
                             [space_left_side + data["width_floor"], self.__floors[i].get_image_rect().top + data["black_space"] / 2], data["black_space"])


    def move(self, screen, click_position, now_click):
        if now_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx - 15 <= click_position[0] <= floor.get_image_rect(
                ).centerx + 15 and floor.get_image_rect().centery - 15 <= click_position[1] <= floor.get_image_rect().centery + 15:
                    self.optimal_elevator(floor)
        screen.fill(white)
        # seconds = 0
        # minutes = (seconds / 60) % 60
        # seconds %= 60
        for elevator in self.__elevators:
            if not elevator.moving() and not elevator.no_tasks():
                elevator.set_moving_to_floor(elevator.pop_task())
                self.__floors[elevator.get_moving_to_floor()].set_timer(abs(elevator.get_moving_to_floor() - elevator.get_elevator_floor()) * 0.5)
                elevator.stop_or_start_moving()
                elevator.set_moving_to(self.__floors[elevator.get_moving_to_floor()].get_image_rect(
                ).centery - elevator.get_image_rect().centery)
            if elevator.moving() and elevator.get_moving_to() > speed:
                elevator.get_image_rect().centery += speed
                elevator.set_moving_to(elevator.get_moving_to() - speed)
                self.__floors[elevator.get_moving_to_floor()].set_timer(self.__floors[elevator.get_moving_to_floor()].get_timer() - (1 / 40))
            if elevator.moving() and elevator.get_moving_to() < speed:
                elevator.get_image_rect().centery -= speed
                elevator.set_moving_to(elevator.get_moving_to() + speed)
                self.__floors[elevator.get_moving_to_floor()].set_timer(self.__floors[elevator.get_moving_to_floor()].get_timer() - (1 / 40))
            if elevator.moving() and speed  + 2>= elevator.get_moving_to() >= -speed - 2:
                sound_file = "ding.mp3"
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                elevator.stop_or_start_moving()
                elevator.set_elevator_floor(elevator.get_moving_to_floor())
                # self.__floors[elevator.get_moving_to_floor()].set_timer(None)
        self.drawing_floors_and_elevators(screen)

        # https://youtu.be/KseiSR0MCTI
