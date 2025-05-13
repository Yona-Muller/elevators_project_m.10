from config import *
from building import Building

pygame.init()


class GameManager:

    def __init__(self, general_settings, building_settings) -> None:
        
        update_general_settings()
        building_settings = load_buildings_array()
        max_floors, _ = max(building_settings)
        canvas_height = max_floors * FLOOR_HEIGHT
        
        self.buildings = []
        for num_of_floors, num_of_elevators in building_settings:
            canvas_width = LEFT_MARGIN * 2 + FLOOR_WIDTH + num_of_elevators * ELEVATOR_WIDTH
            canvas = pygame.Surface((canvas_width, canvas_height))
            self.buildings.append(Building(num_of_floors, num_of_elevators, canvas))
        
        # self.__num_floors = num_floors
        # self.__num_ele = num_ele
        # self.__width = data["space_left"] * 2 + \
        #     data["width_floor"] + num_ele * data["width_ele"]
        # self.__height = data["space_down"] * \
        #     2 + num_floors * data["height_floor"]
        # self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.FULLSCREEN)
        # self.__click_position = None
        # self.__new_click = False
        # self.__fullscreen = True

    def boot_screen(self):
        """
        Sets up the initial game screen with building layout and starts the game loop.
        """
        pygame.display.set_caption("elevators game")
        self.__screen.fill((180, 232, 193))
        building = Building(self.__num_floors, self.__num_ele)
        building.build_floors(self.__screen, self.__height)
        building.build_ele(self.__screen, self.__height)
        self.screen_run(building)

    def screen_run(self, building: Building):
        """
        Main game loop that handles events, updates building state, and redraws the screen.

        Args:
        - building (Building): Instance of the Building class representing the game environment.
        """
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # Toggle fullscreen mode when 'F' key is pressed
                        self.__fullscreen = not self.__fullscreen
                        if self.__fullscreen:
                            pygame.display.set_mode((self.__width, self.__height), pygame.FULLSCREEN)
                        else:
                            pygame.display.set_mode((self.__width, self.__height))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__click_position = event.pos
                    self.__new_click = True
            building.update(self.__screen, self.__click_position,
                          self.__new_click)
            self.__new_click = False
            pygame.display.flip()


game = GameManager(data["num_floors"], data["num_ele"])
game.boot_screen()
