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

width = 400 + num_elevators * 100
height = 120 + num_floors * 90
color = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
# height_floor = height
# floors = []
# for i in range(num_floors):
#     floor = Floor(i)
#     # floor.set_floor_num()
#     floor.image_floor(screen, height - 100)
#     height_floor -= 89


pygame.display.set_caption("abc")
screen.fill(color)
pygame.display.flip()

biul = Building(num_floors, num_elevators)
biul.build_floors(screen, height)
biul.build_elevators(screen, height)

# yona = Elevator()
# yona1 = Floor()
# # yona1.image_floor(screen, height - 100)
# yona.image_elevator(screen, 335, height - 100)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
