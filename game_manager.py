from config import *
from building import Building

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class GameManager:

    def __init__(self, general_settings, building_settings) -> None:
        self.buildings = []
        update_general_settings()
        building_settings = load_buildings_array()
        max_floors, _ = max(building_settings)
        canvas_height = max_floors * FLOOR_HEIGHT
        canvas_width = LEFT_MARGIN * 2 + FLOOR_WIDTH + 3 * ELEVATOR_WIDTH
        canvas = pygame.Surface((canvas_width, canvas_height))
        self.buildings.append(Building(16, 3, canvas))
        
        
        total_width = 0
        for num_of_floors, num_of_elevators in building_settings:
            canvas_width = LEFT_MARGIN * 2 + FLOOR_WIDTH + num_of_elevators * ELEVATOR_WIDTH
            building_surface = pygame.Surface((canvas_width, canvas_height), pygame.SRCALPHA)
            building = Building(num_of_floors, num_of_elevators, building_surface)
            building.x_offset = total_width
            self.buildings.append(building)
            total_width += canvas_width + 50
            
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__scroll_x = 0
        self.__scroll_y = 0
        self.__world_surface = pygame.Surface((total_width, canvas_height))

    def boot_screen(self):
        """
        Sets up the initial game screen with building layout and starts the game loop.
        """
        pygame.display.set_caption("elevators game")
        self.__new_click = False
        self.__click_position = None
        self.__fullscreen = False
        self.screen_run()

    def screen_run(self):
        """
        Main game loop that handles events, updates building state, and redraws the screen.

        Args:
        - building (Building): Instance of the Building class representing the game environment.
        """
        run = True
        clock = pygame.time.Clock()
        
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.__fullscreen = not self.__fullscreen
                        if self.__fullscreen:
                            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        else:
                            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    elif event.key == pygame.K_LEFT:
                        self.__scroll_x = max(self.__scroll_x - 30, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.__scroll_x += 30
                    elif event.key == pygame.K_UP:
                        self.__scroll_y = max(self.__scroll_y - 30, 0)
                    elif event.key == pygame.K_DOWN:
                        self.__scroll_y += 30
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__click_position = event.pos
                    self.__new_click = True

            self.__world_surface.fill((180, 232, 193))

            for building in self.buildings:
                building.update(self.__world_surface, self.__click_position, self.__new_click, x_offset=building.x_offset)

            self.__new_click = False
            self.__screen.blit(self.__world_surface, (-self.__scroll_x, -self.__scroll_y))
            pygame.display.flip()



game = GameManager({
  "buildings": {
    "building_0": {
      "number_of_floors": 10,
      "number_of_elevators": 3
    },
    "building_1": {
      "number_of_floors": 10,
      "number_of_elevators": 3
    },
    "building_2": {
      "number_of_floors": 10,
      "number_of_elevators": 3
    },
    "building_3": {
      "number_of_floors": 10,
      "number_of_elevators": 3
    },
    "building_4": {
      "number_of_floors": 10,
      "number_of_elevators": 3
    }
  }
}, load_buildings_array())
game.boot_screen()

