import pygame
from class_floor import Floor
from class_elevator import Elevator
import json
import time

with open("data.json") as data_:
    data = json.load(data_)


white = (255, 255, 255)
black = (0, 0, 0)
color = (0, 0, 0)
speed = 3


class Building:
    def __init__(self, num_floors, num_elevators) -> None:
        self.__floors = [Floor(i) for i in range(num_floors)]
        self.__elevators = [Elevator(i) for i in range(num_elevators)]

    # def set_timer(self, target_floor):
    #     self.__floors[self.get_moving_to_floor()].set_timer(
    #             abs(self.get_moving_to_floor() - self.get_current_floor()) * 0.5)

    def build_floors(self, screen, width, height):
        for floor in self.__floors:
            floor.draw_floor(screen, height -
                             data["space_down"] - data["height_floor"])
            height -= data["height_floor"]
        pygame.draw.line(screen, white, [data["space_left"], height - data["black_space"]], [
                         data["space_left"] + data["width_floor"], height - data["black_space"]], data["black_space"])

    def build_elevators(self, screen, height, x=data["space_left"] * 2 + data["width_floor"]):
        for elevator in self.__elevators:
            elevator.draw_elevator(screen, x, height -
                                   data["space_down"] - data["height_ele"])
            x += data["width_ele"]

    def optimal_elevator(self, target_floor: Floor):
        min = float("inf"), -1
        for elevator in self.__elevators:
            if not elevator.no_tasks():
                time_tasks_elevator = elevator.get_lest_task(
                )[1] + abs(elevator.get_lest_task()[0] - target_floor.get_floor_num()) * 0.5 if not elevator.get_elevator_moving() else elevator.get_lest_task(
                )[1] + abs(elevator.get_lest_task()[0] - target_floor.get_floor_num()) * 0.5 + self.__floors[elevator.get_moving_to_floor()].get_timer()
                if time_tasks_elevator < min[0]:
                    min = time_tasks_elevator, elevator.get_num_elevator()
            else:
                time_tasks_elevator = abs(
                    elevator.get_current_floor() - target_floor.get_floor_num()) * 0.5 if not elevator.get_elevator_moving() else abs(elevator.get_moving_to_floor() - target_floor.get_floor_num()) * 0.5 + self.__floors[elevator.get_moving_to_floor()].get_timer()
                if time_tasks_elevator < min[0]:
                    min = time_tasks_elevator, elevator.get_num_elevator()
        self.__elevators[min[1]].insert_task(target_floor.get_floor_num())
        self.__elevators[min[1]].time_start = time.monotonic_ns()
        target_floor.set_timer(self.__elevators[min[1]].get_lest_task()[1] - 2)
        target_floor.set_elevator_com(self.__elevators[min[1]])
        self.__elevators[min[1]].set_dist_ele_to_floor(target_floor.get_image_rect(
        ).centery - self.__elevators[min[1]].get_image_rect().centery)

    def drawing_floors_and_elevators(self, screen):
        for elevator in self.__elevators:
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        for floor in self.__floors:
            screen.blit(floor.get_image(), floor.get_image_rect())
            font = pygame.font.Font(None, data["width_floor"] // 5)
            text = font.render(
                f"{floor.get_floor_num()}", True, (255, 255, 255))
            screen.blit(text, (data["width_floor"] * 0.73, floor.get_image_rect().centery - 4))

            if floor.get_timer() and not floor.get_elevator_com().get_doors_open():
                font = pygame.font.Font(None, data["width_floor"] // 4)
                text = font.render(
                    f"{int(floor.get_timer() // 1):02}:{int((floor.get_timer() % 1) * 100):02}", True, floor.get_elevator_com().get_color_timer())
                screen.blit(text, (20, floor.get_image_rect().centery - 7))
                floor.set_timer(floor.get_timer() - (1 / 40))
                

            elif floor.get_elevator_com() and floor.get_elevator_com().get_doors_open():
                font = pygame.font.Font(None, data["width_floor"] // 8)
                text = font.render("doors open", True, (70, 143, 34))
                screen.blit(text, (20, floor.get_image_rect().centery))
                floor.get_elevator_com().set_doors_open(
                    floor.get_elevator_com().get_doors_open() - 1/40)
                # if floor.get_elevator_com().get_doors_open() < 0.2: floor.set_elevator_com(None)

        for i in range(len(self.__floors) - 1):
            pygame.draw.line(screen, black, [data["space_left"], self.__floors[i].get_image_rect().top + data["black_space"] / 2],
                             [data["space_left"] + data["width_floor"], self.__floors[i].get_image_rect().top + data["black_space"] / 2], data["black_space"])

    def move(self, screen, click_position, new_click):
        if new_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx + 20 <= click_position[0] <= floor.get_image_rect(
                ).centerx + 45 and floor.get_image_rect().centery - 15 <= click_position[1] <= floor.get_image_rect().centery + 15:
                    self.optimal_elevator(floor)
                    floor.set_image(pygame.transform.scale(
                        pygame.image.load(data["image_floor_g"]), (data["width_floor"], data["height_floor"])))
        # screen.fill(white)
        for elevator in self.__elevators:
            elevator.move_ele()
            if elevator.get_doors_open():
                self.__floors[elevator.get_moving_to_floor()].set_image(pygame.transform.scale(
                    pygame.image.load(data["image_floor"]), (data["width_floor"], data["height_floor"])))
            if elevator.get_moving_to_floor() and self.__floors[elevator.get_moving_to_floor()].get_timer() and self.__floors[elevator.get_moving_to_floor()].get_timer() <= 0:
                self.__floors[elevator.get_moving_to_floor()].set_timer(None)
        self.drawing_floors_and_elevators(screen)
        # if not is_door_open: return True
