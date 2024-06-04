import pygame
from class_building import Building
import json


with open("data.json") as data_:
    data = json.load(data_)

num_floors = int(input("choose the number of floors: "))
while not 0 < num_floors <= 100:
    num_floors = int(input("choose a number of floors between 1 in 100: "))
num_elevators = int(input("choose the number of elevators: "))
while not 0 < num_elevators <= 15:
    num_elevators = int(input("choose a number of elevators between 1 in 15: "))


pygame.init()

width = data["space_left"] * 2 + data["width_floor"] + num_elevators * data["width_ele"]
height = data["height_ele"] * 2 + (num_floors - 1) * data["height_floor"]
white = (255, 255, 255)
screen = pygame.display.set_mode((width, height))


pygame.display.set_caption("elevators game")
screen.fill(white)
pygame.display.flip()

building = Building(num_floors, num_elevators)
building.build_floors(screen, width, height)
building.build_elevators(screen, height)


target_position = None
click_position = None
fullscreen = False

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        screen.fill(white)
        building = Building(num_floors, num_elevators)
        building.build_floors(screen, width, height)
        building.build_elevators(screen, height)
    else:
        pygame.display.set_mode((width, height))
        screen.fill(white)
        building = Building(num_floors, num_elevators)
        building.build_floors(screen, width, height)
        building.build_elevators(screen, height)
        

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Toggle fullscreen mode when 'F' key is pressed
                toggle_fullscreen()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_position = event.pos
            now_click = True

    if click_position:
        finished = building.move(screen, click_position, now_click)
        now_click = False
        if finished: click_position = None
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)
