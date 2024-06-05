import pygame
from class_floor import Floor
from class_elevator import Elevator
import json

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

    def build_floors(self, screen, width, height):
        for floor in self.__floors:
            floor.draw_floor(screen, height - data["space_down"] - data["height_floor"])
            height -= data["height_floor"]
        pygame.draw.line(screen, white, [data["space_left"], height - data["black_space"]], [310, height - data["black_space"]], data["black_space"])

    def build_elevators(self, screen, height, x=data["space_left"] * 2 + data["width_floor"]):
        for elevator in self.__elevators:
            elevator.draw_elevator(screen, x, height - data["space_down"] - data["height_ele"])
            x += data["width_ele"]

    def optimal_elevator(self, target_floor: Floor):
        min = float("inf"), -1
        for elevator in self.__elevators:
            if not elevator.no_tasks():
                time_staks_elevator = elevator.get_time_tasks(
                ) + abs(elevator.get_lest_task() - target_floor.get_floor_num()) if not elevator.get_elevator_moving() else elevator.get_time_tasks(
                ) + abs(elevator.get_lest_task() - target_floor.get_floor_num()) + self.__floors[elevator.get_moving_to_floor()].get_timer()
                if time_staks_elevator < min[0]:
                    min = time_staks_elevator, elevator.get_num_elevator()
            else:
                time_staks_elevator = abs(
                    elevator.get_current_floor() - target_floor.get_floor_num()) * 0.5 if not elevator.get_elevator_moving() else abs(
                    elevator.get_current_floor() - target_floor.get_floor_num()) * 0.5 + self.__floors[elevator.get_moving_to_floor()].get_timer()
                if time_staks_elevator < min[0]:
                    min = time_staks_elevator, elevator.get_num_elevator()
        self.__elevators[min[1]].insert_task(target_floor.get_floor_num())
        if not elevator.no_tasks():
            target_floor.set_timer(abs(target_floor.get_floor_num() - elevator.get_lest_task()) * 0.5 + self.__elevators[min[1]].get_time_tasks())
        else:
            target_floor.set_timer(abs(target_floor.get_floor_num() - elevator.get_current_floor()) * 0.5)
        target_floor.set_elevator_com(self.__elevators[min[1]])

    def drawing_floors_and_elevators(self, screen):
        for elevator in self.__elevators:
            screen.blit(elevator.get_image(), elevator.get_image_rect())
        for floor in self.__floors:
            screen.blit(floor.get_image(), floor.get_image_rect())
            font = pygame.font.Font(None, 30)
            text = font.render(
                f"{floor.get_floor_num()}", True, (255, 255, 255))
            screen.blit(text, (data["width_floor"] * 0.73, floor.get_image_rect().centery - 4))

            if floor.get_timer():
                font = pygame.font.Font(None, 40)
                text = font.render(
                    f"{int(floor.get_timer() // 1):02}:{int((floor.get_timer() % 1) * 100):02}", True, floor.get_elevator_com().get_color_timer())
                screen.blit(text, (20, floor.get_image_rect().centery - 7))
                floor.set_timer(floor.get_timer() - (1 / 40))

        for i in range(len(self.__floors) - 1):
            pygame.draw.line(screen, black, [data["space_left"], self.__floors[i].get_image_rect().top + data["black_space"] / 2],
                             [data["space_left"] + data["width_floor"], self.__floors[i].get_image_rect().top + data["black_space"] / 2], data["black_space"])


    
    def move(self, screen, click_position, new_click):
        if new_click:
            for floor in self.__floors:
                if floor.get_image_rect().centerx + 20 <= click_position[0] <= floor.get_image_rect(
                ).centerx + 45 and floor.get_image_rect().centery - 15 <= click_position[1] <= floor.get_image_rect().centery + 15:
                    self.optimal_elevator(floor)
        screen.fill(white)
        for elevator in self.__elevators:
            if not elevator.moving() and not elevator.no_tasks():
                elevator.set_moving_to_floor(elevator.pop_task())
                self.__floors[elevator.get_moving_to_floor()].set_timer(abs(elevator.get_moving_to_floor() - elevator.get_current_floor()) * 0.5)
                elevator.stop_or_start_moving()
                elevator.set_moving_to(self.__floors[elevator.get_moving_to_floor()].get_image_rect(
                ).centery - elevator.get_image_rect().centery)
            if elevator.moving() and elevator.get_moving_to() > speed:
                elevator.get_image_rect().centery += speed
                elevator.set_moving_to(elevator.get_moving_to() - speed)
            if elevator.moving() and elevator.get_moving_to() < speed:
                elevator.get_image_rect().centery -= speed
                elevator.set_moving_to(elevator.get_moving_to() + speed)
            if elevator.moving() and speed  + 2 >= elevator.get_moving_to() >= -speed - 2:
                if not elevator.get_is_door_open():
                    sound_file = data["ding"]
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play()
                    self.__floors[elevator.get_moving_to_floor()].set_timer(2)
                    elevator.set_is_door_open()
                elif self.__floors[elevator.get_moving_to_floor()].get_timer() <= 0:
                    elevator.stop_or_start_moving()
                    elevator.set_current_floor(elevator.get_moving_to_floor())
                    self.__floors[elevator.get_moving_to_floor()].set_timer(None)
                    elevator.set_moving_to_floor(None)
                    elevator.set_is_door_open()
        self.drawing_floors_and_elevators(screen)
        # if not is_door_open: return True

