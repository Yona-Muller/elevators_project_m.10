import pygame
from class_elevator import Elevator
from class_floor import Floor
from class_building import Building


num_floors = int(input("choose the number of floors: "))
while not 0 < num_floors <= 100:
    num_floors = int(input("choose a number of floors between 1 in 100: "))
num_elevators = int(input("choose the number of elevators: "))
while not 0 < num_elevators <= 15:
    num_floors = int(input("choose a number of elevators between 1 in 15: "))


pygame.init()

width = 310 + num_elevators * 100
height = 120 + num_floors * 90
white = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
move_x = 5
move_y = 5


pygame.display.set_caption("elevators game")
screen.fill(white)
pygame.display.flip()

building = Building(num_floors, num_elevators)
building.build_floors(screen, width, height)
building.build_elevators(screen, height)


target_position = None
click_position = None

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_position = event.pos
            # Left mouse button clicked

    if click_position:
        building.move(screen, click_position)
