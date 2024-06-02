import pygame

black = (0, 0, 0)


class Floor:
    def __init__(self, floor_num = None) -> None:
        self.__floor_num = floor_num
        self.__button = None
        self.__color_button = (20, 20, 20)
        self.__clock = None
        self.height_floor = 80
        self.width_floor = 300
        self.__image = None
        self.__image_rect = None
    

    def get_image(self):
        return self.__image
    
    def get_image_rect(self):
        return self.__image_rect

    def get_floor_num(self) -> int:
        return self.__floor_num

    def image_floor(self, screen, floor_locat, black_space = 7, space_left_side = 10):
        image_floor = "whites.png"
        img = pygame.image.load(image_floor)
        self.__image = pygame.transform.scale(
            img, (self.width_floor, self.height_floor))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (space_left_side, floor_locat)
        screen.blit(self.__image, self.__image_rect)
        pygame.draw.line(screen, black, [
                         space_left_side, floor_locat - black_space / 2], [space_left_side + self.width_floor, floor_locat - black_space / 2], black_space)
        pygame.display.flip()

    def __str__(self) -> str:
        return f'{self.__floor_num}'