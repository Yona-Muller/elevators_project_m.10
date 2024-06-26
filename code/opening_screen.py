import pygame
import json
import os
from Game import set_screen_position
from Game import Game


with open("../data.json") as data_:
    data = json.load(data_)

# Initialize Pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
pygame.init()

# Set up the screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Input Example")

# Set up fonts
font = pygame.font.Font(None, 45)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the input areas
input_rect1 = pygame.Rect(610, 975, 70, 40)
input_rect2 = pygame.Rect(1469, 975, 70, 40)
play_rect = pygame.Rect(800, 930, 300, 100)
# Main loop
num_floors = ''
num_elevators = ''
active_input = None  # To keep track of which input area is active


image_floor = "../resources/images/aaa.png"
img = pygame.image.load(image_floor)
image = pygame.transform.scale(
    img, (screen_width, screen_height))
image_rect = image.get_rect()
image_rect.topleft = (0, 0)

run = True
while run:
    screen.blit(image, image_rect)
    
    # Render the current text for input area 1
    text_surface1 = font.render(num_floors, True, BLACK)
    screen.blit(text_surface1, (input_rect1.x + 25, input_rect1.y + 5))
    
    # Render the current text for input area 2
    text_surface2 = font.render(num_elevators, True, BLACK)
    screen.blit(text_surface2, (input_rect2.x + 25, input_rect2.y + 5))
    
    # Draw the input areas
    # pygame.draw.rect(screen, WHITE, input_rect1, 2)
    # pygame.draw.rect(screen, BLACK, input_rect2, 2)
    # pygame.draw.rect(screen, BLACK, play_rect, 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within any input area
            if input_rect1.collidepoint(event.pos):
                active_input = input_rect1
                pygame.key.start_text_input()  # Start text input for input area 1
            elif input_rect2.collidepoint(event.pos):
                active_input = input_rect2
                pygame.key.start_text_input()  # Start text input for input area 2
            else:
                active_input = None
                pygame.key.stop_text_input()  # Stop text input if clicked outside input areas
            if play_rect.collidepoint(event.pos):
                try:
                    num_floors = int(num_floors)
                    num_elevators = int(num_elevators)
                    run = False
                    screen_size = pygame.display.get_desktop_sizes()
                    pygame.display.quit()
                    set_screen_position(num_elevators, num_floors, screen_size)
                    game = Game(num_elevators, num_floors)
                    game.boot_screen()
                except:
                    continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    num_floors = int(num_floors)
                    num_elevators = int(num_elevators)
                    run = False
                    screen_size = pygame.display.get_desktop_sizes()
                    pygame.display.quit()
                    set_screen_position(num_elevators, num_floors, screen_size)
                    game = Game(num_elevators, num_floors)
                    game.boot_screen()
                except:
                    break
            if active_input == input_rect1:
                  # Insert a line break into num_floors
                if event.key == pygame.K_BACKSPACE:
                    num_floors = num_floors[:-1]  # Remove the last character
                else:
                    num_floors += event.unicode  # Add the character to num_floors
            elif active_input == input_rect2:
                # if event.key == pygame.K_RETURN:
                #     num_elevators += '\n'  # Insert a line break into tnum_elevators
                if event.key == pygame.K_BACKSPACE:
                    num_elevators = num_elevators[:-1]  # Remove the last character
                else:
                    num_elevators += event.unicode  # Add the character to tnum_elevators

    
    pygame.display.flip()
    
    
