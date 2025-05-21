import pygame
import json

# Load configuration file
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

class Floor:
    def __init__(self, building, floor_number, width):
        """
        Initialize a new floor

        Args:
            building: Reference to the building object the floor belongs to
            floor_number: The floor number (starting from 0)
            width: The width of the floor in pixels
        """
        self.building = building
        self.floor_number = floor_number
        self.width = width
        self.height = CONFIG["floor"]["height"]
        self.separator_height = CONFIG["floor"]["separator_height"]
        
        # Floor button settings
        self.button_width = CONFIG["floor"]["button_width"]
        self.button_height = CONFIG["floor"]["button_height"]
        self.button_margin = CONFIG["floor"]["button_margin"]
        self.button_rect = None
        
        # Floor attributes
        self.has_call = False
        self.button_active = False
        self.countdown_timer = None
        
        self.floor_bg_image = pygame.image.load("assets/floor_bg.png")
        
        # Font for text
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 22)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
    def call_elevator(self):
        """
        Trigger an elevator call from this floor

        Returns:
            float: Estimated time for the elevator to arrive (in seconds)
        """
        if not self.button_active:
            self.button_active = True
            # Request the building to assign an elevator to this floor
            arrival_time = self.building.request_elevator(self.floor_number)
            self.countdown_timer = arrival_time
            return arrival_time
        return self.countdown_timer
    
    def elevator_arrived(self):
        """Mark that the elevator has arrived at this floor"""
        self.button_active = False
        self.countdown_timer = None
    
    def update_timer(self, dt):
        """
        Update the floor's timer state

        Args:
            dt: Time passed since the last update (in seconds)
        """
        if self.countdown_timer is not None:
            self.countdown_timer = max(0, self.countdown_timer - dt)
    
    def check_button_click(self, pos):
        """
        Check if a click hit the floor's button

        Args:
            pos: Click position (x, y)

        Returns:
            bool: Whether the button was clicked
        """
        if self.button_rect and self.button_rect.collidepoint(pos):
            self.call_elevator()
            return True
        return False
        
    def draw(self, screen, y_offset=0):
        """
        Draw the floor on the screen

        Args:
            screen: The pygame drawing surface
            y_offset: Vertical offset (for scrolling)
        """
        # Calculate the vertical position of the floor (from top to bottom)
        y = y_offset + self.height * (self.building.num_floors - self.floor_number - 1)
        
        # Draw the background image (preloaded)
        if self.floor_bg_image:  
            image_scaled = pygame.transform.scale(self.floor_bg_image, (CONFIG["floor"]["width"], CONFIG["floor"]["height"]))
            screen.blit(image_scaled, (CONFIG["floor"]["margin_left"], y))
        
        # Draw the separator line between floors
        pygame.draw.rect(screen, (0, 0, 0), 
                         (CONFIG["floor"]["margin_left"], y, CONFIG["floor"]["width"], self.separator_height))
        
        # Draw the floor button
        button_x = self.button_margin + CONFIG["floor"]["margin_left"]
        button_y = y + (self.height - self.button_height) / 2
        
        # Update the button's rect with the new position
        self.button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
        
        # Button color changes if active
        button_color = (200, 200, 200)
        text_color = (0, 0, 0)
        
        if self.button_active:
            text_color = (0, 200, 0)  # Green text when elevator is on the way
        
        pygame.draw.rect(screen, button_color, self.button_rect)
        
        # Draw the floor number text inside the button
        floor_text = self.font.render(str(self.floor_number), True, text_color)
        floor_text_rect = floor_text.get_rect(center=self.button_rect.center)
        screen.blit(floor_text, floor_text_rect)
        
        # If there's a countdown timer, display it prominently
        if self.countdown_timer is not None and self.button_active:
            # Draw background for the timer
            timer_bg_rect = pygame.Rect(self.button_rect.left + 35, self.button_rect.y, 50, self.button_rect.height + 15)
            pygame.draw.rect(screen, (255, 240, 240), timer_bg_rect)
            pygame.draw.rect(screen, (127, 107, 107), timer_bg_rect, 2)  # Border
            
            # Display timer with bold font
            seconds_left = max(0.0, self.countdown_timer - CONFIG["elevator"]["door_open_time"])
            timer_text = self.font.render(f"{seconds_left:.1f}s", True, (173, 131, 131))
            timer_rect = timer_text.get_rect(center=timer_bg_rect.center)
            screen.blit(timer_text, timer_rect)
