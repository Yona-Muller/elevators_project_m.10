import pygame
from class_floor import Floor
from class_elevator import Elevator

class Building:
    def __init__(self, num_floors, num_elevators) -> None:
        self.__floors = [Floor(i) for i in range(num_floors + 1)]
        self.__elevators = [Elevator(i) for i in range(num_elevators)]
        print(self.__floors)

    def build_floors(self, screen, height):
        for floor in self.__floors:
            floor.image_floor(screen, height - 100)
            height -= 87  

    def build_elevators(self, screen, height, a = 330):
        for elevator in self.__elevators:
            elevator.image_elevator(screen, a, height - 100)
            a += 75
