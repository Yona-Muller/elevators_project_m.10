import pygame
import sys
import json
import time
from building import Building

# Load configuration file
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

class GameManager:
    def __init__(self):
        """Initialize the game manager and elevator system"""
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        
        # Game window settings
        self.font = pygame.font.SysFont('Arial', 24)
        self.buildings = []
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Time tracking
        self.last_update_time = 0
        
        # Scrolling variables
        self.scroll_x = 0
        self.scroll_y = 0
        self.max_scroll_x = 0
        self.max_scroll_y = 0
        self.scroll_speed = 20
        self.view_width = 800
        self.view_height = 600
        
        self.__fullscreen = False
        
    def create_buildings(self, buildings_config):
        """
        Initialize buildings based on configuration

        Args:
            buildings_config: List of dictionaries with building definitions
                              [{'floors': 10, 'elevators': 3}, {'floors': 5, 'elevators': 2}, ...]
        """
        self.buildings = []
        
        # Compute required screen dimensions
        self.total_height = 0
        self.total_width = 0
        
        self.max_floors = max(building["floors"] for building in buildings_config)
        
        for i, building_conf in enumerate(buildings_config):
            num_floors = building_conf['floors']
            num_elevators = building_conf['elevators']
            
            # Calculate building width based on number of elevators
            width = self.calculate_building_width(num_elevators)
            
            # Add spacing between buildings
            if i > 0:
                self.total_width += 80  # Gap between buildings
                
            # Instantiate a new building
            building = Building(
                i, num_floors, num_elevators, self.max_floors,
                position=(self.total_width, CONFIG["floor"]["height"] * (self.max_floors - num_floors)),
                width=width
            )
            self.buildings.append(building)
            
            # Update max dimensions
            height = num_floors * CONFIG["floor"]["height"]
            self.total_height = max(self.total_height, height)
            self.total_width += width
        
        # Initialize the main screen
        self.view_width = min(self.total_width + 50, 1200)
        self.view_height = min(self.total_height + 50, 800)
        
        self.screen = pygame.display.set_mode((self.view_width, self.view_height))
        pygame.display.set_caption("Elevator Simulator")
        
        # Update scroll boundaries
        self.max_scroll_x = max(0, self.total_width - self.view_width + 50)
        self.max_scroll_y = max(0, self.total_height - self.view_height + 50)
        
    def calculate_building_width(self, num_elevators):
        """
        Calculate the width of a building based on the number of elevators

        Args:
            num_elevators: Number of elevators in the building

        Returns:
            int: Building width in pixels
        """
        elevator_width = CONFIG["elevator"]["width"]
        elevator_spacing = CONFIG["building"]["elevator_spacing"]
        margin = CONFIG["building"]["margin"]
        button_width = CONFIG["floor"]["button_width"]
        button_margin = CONFIG["floor"]["button_margin"]
        
        # Compute minimum required elevator area
        elevator_area_width = num_elevators * elevator_width
        if num_elevators > 1:
            elevator_area_width += (num_elevators - 1) * elevator_spacing
        
        # Total building width
        total_width = 2 * margin + elevator_area_width + button_width + button_margin
        
        # Ensure a minimum width
        return max(300, total_width)
    
    def handle_scroll(self, keys):
        """
        Handle screen scrolling via keyboard input

        Args:
            keys: Pressed key states
        """
        # Horizontal scrolling
        if keys[pygame.K_LEFT]:
            self.scroll_x = max(0, self.scroll_x - self.scroll_speed)
        if keys[pygame.K_RIGHT]:
            self.scroll_x = min(self.max_scroll_x, self.scroll_x + self.scroll_speed)
            
        # Vertical scrolling
        if keys[pygame.K_UP]:
            self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
        if keys[pygame.K_DOWN]:
            self.scroll_y = min(self.max_scroll_y, self.scroll_y + self.scroll_speed)
            
    def run(self):
        """Main game loop"""
        self.running = True
        self.last_update_time = time.time()
        
        while self.running:
            # Calculate time delta since last update
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.__fullscreen = not self.__fullscreen
                        if self.__fullscreen:
                            pygame.display.set_mode((self.view_width, self.view_height), pygame.FULLSCREEN)
                        else:
                            pygame.display.set_mode((self.view_width, self.view_height), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll_y = max(0, min(self.scroll_y - event.y * self.scroll_speed, self.max_scroll_y))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    adjusted_pos = (event.pos[0] + self.scroll_x, event.pos[1] + self.scroll_y)
                    
                    # Pass the click event to each building
                    for building in self.buildings:
                        building.handle_click(adjusted_pos)
            
            # Scroll handling
            keys = pygame.key.get_pressed()
            self.handle_scroll(keys)
            
            # Update buildings
            for building in self.buildings:
                building.update(dt)
            
            # Render
            self.draw()
            
            # Frame rate control
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def draw(self):
        """Render all game components"""
        # Create a surface representing the entire world
        world_surface = pygame.Surface((self.total_width + 100, self.total_height + 100))
        world_surface.fill((252, 243, 232))
        
        # Draw building outlines
        for building in self.buildings:
            building_rect = pygame.Rect(
                building.position[0], 
                building.position[1], 
                building.width, 
                building.num_floors * CONFIG["floor"]["height"]
            )
            pygame.draw.rect(world_surface, (220, 220, 220), building_rect)
            pygame.draw.rect(world_surface, (180, 180, 180), building_rect, 3)
        
        # Display scroll debug info
        scroll_info = self.font.render(f"Scroll: X={self.scroll_x}, Y={self.scroll_y}", True, (0, 0, 0))
        world_surface.blit(scroll_info, (10, 10))
        
        # Draw each building
        for building in self.buildings:
            # Adjust building position for scroll
            adjusted_position = (building.position[0], building.position[1])
            
            # Save and temporarily modify position
            original_position = building.position
            building.position = adjusted_position
            
            # Draw building
            building.draw(world_surface)
            
            # Restore original position
            building.position = original_position
        
        # Blit the relevant portion of the world surface to the screen
        self.screen.blit(world_surface, (-self.scroll_x, -self.scroll_y))
        
        # Refresh the display
        pygame.display.flip()

def main():
    """Entry point of the game"""
    game = GameManager()
    
    # Load building configuration (can be modified as needed)
    buildings_config = CONFIG["building"]["buildings"]
    
    # Create buildings
    game.create_buildings(buildings_config)
    
    # Start the game loop
    game.run()

if __name__ == "__main__":
    main()
