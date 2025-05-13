import pygame
import json

with open("data.json") as data_:
    data = json.load(data_)

black = (0, 0, 0)
white = (255, 255, 255)


class Floor:
    """
    Represents a floor in the building.

    Attributes:
    - __num (int): Floor number.
    - __image (pygame.Surface): Image representing the floor.
    - __image_rect (pygame.Rect): Rectangle object for positioning the floor image on the screen.
    - __ele_on_way (bool): Flag indicating if an elevator is on its way to this floor.
    - __timer (float): Timer indicating remaining time for elevator arrival.
    - start_time (float): Time when the elevator started moving towards this floor.
    """

    def __init__(self, num) -> None:
        """
        Initializes a floor with a specific number.

        Args:
        - num (int): Floor number.
        """
        self.__num = num
        self.__image = data["image_floor"]
        self.__image_rect = None
        self.__ele_on_way = False
        self.__timer = None
        self.start_time = None

    def get_image_rect(self):
        """
        Returns the rectangle object for the floor's image on the screen.

        Returns:
        - pygame.Rect: Rectangle object for positioning the floor image on the screen.
        """
        return self.__image_rect

    def get_image(self):
        """
        Returns the image object representing the floor.

        Returns:
        - pygame.Surface: Image object representing the floor.
        """
        return self.__image

    def set_image(self, image):
        """
        Sets a new image for the floor.

        Args:
        - image (pygame.Surface): New image to set for the floor.
        """
        self.__image = image

    def get_ele_on_way(self):
        """
        Checks if an elevator is on its way to this floor.

        Returns:
        - bool: True if an elevator is on its way, False otherwise.
        """
        return self.__ele_on_way

    def get_num(self):
        """
        Returns the floor number.

        Returns:
        - int: Floor number.
        """
        return self.__num

    def set_ele_on_way(self, value):
        """
        Sets the status of an elevator arriving at this floor.

        Args:
        - value (bool): New status of an elevator arriving at this floor.
        """
        self.__ele_on_way = value

    def get_timer(self):
        """
        Returns the timer indicating the time remaining for elevator arrival.

        Returns:
        - float: Time remaining for elevator arrival.
        """
        return self.__timer

    def set_timer(self, seconds):
        """
        Sets the timer for elevator arrival.

        Args:
        - seconds (float): Time remaining for elevator arrival.
        """
        self.__timer = seconds

    def draw_floor2(self, screen):
        """
        Draws the floor representation on the screen.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        """
        screen.blit(self.__image, self.__image_rect)
        font = pygame.font.Font(None, data["width_floor"] // 5)
        text = font.render(
            f"{self.__num}", True, (255, 255, 255))
        screen.blit(text, (data["width_floor"] * 0.71,
                    self.__image_rect.centery - 4))

    def draw_floor(self, screen, height, num_floors):
        """
        Draws the floor representation on the screen at a specific height.

        Args:
        - screen (pygame.Surface): The surface of the screen to draw on.
        - height (int): Initial height position to start drawing the floor.
        - num_floors (int): Total number of floors in the building.
        """
        img = pygame.image.load(self.__image)
        self.__image = pygame.transform.scale(
            img, (data["width_floor"], data["height_floor"]))
        self.__image_rect = self.__image.get_rect()
        self.__image_rect.topleft = (data["space_left"], height)
        screen.blit(self.__image, self.__image_rect)
        font = pygame.font.Font(None, data["height_floor"] // 2)
        text = font.render(f"{self.__num}", True, white)
        screen.blit(text, (data["width_floor"] * 0.72,
                    self.__image_rect.centery - 4))
