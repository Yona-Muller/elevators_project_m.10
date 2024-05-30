import pygame


class Elevator:
    def __init__(self, num_elevator) -> None:
        self.__image = None
        self.__image_rect = None
        
    def get_image_rect(self):
        return self.__image_rect
    
    def set_image_rect(self, item):
        self.__image_rect = item

    def get_image(self):
        return self.__image

    def image_elevator(self, screen, elevator_loc_width, elevator_loc_height):
        image_elevator = "elv.png"
        img = pygame.image.load(image_elevator)
        self.__image = pygame.transform.scale(img, (82, 82))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (elevator_loc_width, elevator_loc_height)
        screen.blit(self.__image, self.__image_rect)
        pygame.display.flip()


