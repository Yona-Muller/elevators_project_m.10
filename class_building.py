import pygame
from class_floor import Floor
from class_elevator import Elevator

white = (255, 255, 255)
black = (0, 0, 0)
space_left_side = 10
speed = 1 / 75


class Building:
    def __init__(self, num_floors, num_elevators) -> None:
        self.__floors = [Floor(i) for i in range(num_floors + 1)]
        self.__elevators = [Elevator(i) for i in range(num_elevators)]

    def build_floors(self, screen, width, height):
        for floor in self.__floors:
            floor.image_floor(screen, height - 100)
            height -= 87
        pygame.draw.line(
            screen, white, [space_left_side, height - 16.5], [310, height - 16.5], 7)

    def build_elevators(self, screen, height, a=330):
        for elevator in self.__elevators:
            elevator.image_elevator(screen, a, height - 100)
            a += 75

    def move(self, screen, click_position):
        # senter_image =
        for floor in self.__floors:
            if floor.get_image_rect().center[0] - 15 <= click_position[0] <= floor.get_image_rect().center[
                0] + 15 and floor.get_image_rect().center[1] - 15 <= click_position[1] <= floor.get_image_rect().center[1] + 15:
                screen.fill(white)
                dy = floor.get_image_rect().center[1] - self.__elevators[0].get_image_rect().center[1] + 7 
                # Move the image gradually towards the target position
                if dy != 0:
                    dy *= speed
                    self.__elevators[0].get_image_rect().centery += dy
                else:
                    # If the image is close to the target position, snap it to the target
                    self.__elevators[0].get_image_rect().center = self.__elevators[0].get_image_rect().center
                    target_position = None
                    return

                for elevator in self.__elevators:
                    screen.blit(elevator.get_image(), elevator.get_image_rect())
                for floor in self.__floors:
                    screen.blit(floor.get_image(), floor.get_image_rect())
                for i in range(len(self.__floors) - 1):
                    pygame.draw.line(screen, black, [space_left_side, self.__floors[i].get_image_rect().top - 4],
                                    [space_left_side + self.__floors[i].width_floor, self.__floors[i].get_image_rect().top - 4], 7)
                

        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)
