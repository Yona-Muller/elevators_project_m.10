import pygame


class Elevator:
    def __init__(self, num_elevator) -> None:
        self.__image = None
        self.__num_elevators = num_elevator

    def move_up(self):
        pass

    def move_down(self):
        pass

    def image_elevator(self, screen, elevator_loc_width, elevator_loc_height):
        image_elevator = "elv.png"
        img = pygame.image.load(image_elevator)
        image = pygame.transform.scale(img, (82, 82))
        image_rect = image.get_rect()
        image_rect.topleft = (elevator_loc_width, elevator_loc_height)
        screen.blit(image, image_rect)
        pygame.display.flip()


# yona = Elevator
# yona.image_elevator(yona)