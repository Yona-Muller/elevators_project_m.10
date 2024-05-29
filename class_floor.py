import pygame

class Floor:
    def __init__(self, floor_num = None) -> None:
        self.__floor_num = floor_num
        self.__button = None
        self.__color_button = (20, 20, 20)
        self.__clock = None

    def get_floor_num(self):
        return self.__floor_num
    
    # def set_floor_num(self):
    #     if not self.__floor_num():
    #         self.__floor_num = 0
    #     else:
    #         self.__floor_num += 1

    def image_floor(self, screen, floor_locat):
        image_floor = "whites.png"
        img = pygame.image.load(image_floor)
        image = pygame.transform.scale(img, (300, 80))
        image_rect = image.get_rect()
        image_rect.topleft = (10, floor_locat)
        screen.blit(image, image_rect)
        pygame.draw.line(screen, (0, 0, 0), [10, floor_locat - 4], [309, floor_locat - 4], 7)
        pygame.display.flip()
