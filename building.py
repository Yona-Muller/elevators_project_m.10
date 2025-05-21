import pygame
import json
from floor import Floor
from factory import ElevatorFactory

# Load the configuration file
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

class Building:
    def __init__(self, building_id, num_floors, num_elevators, max_floors, position=(0, 0), width=400):
        """
        Initialize a new building

        Args:
            building_id: Unique identifier for the building
            num_floors: Number of floors in the building
            num_elevators: Number of elevators in the building
            position: Position of the building on screen (x, y)
            width: Width of the building in pixels
        """
        self.id = building_id
        self.num_floors = num_floors
        self.num_elevators = num_elevators
        self.position = position
        self.width = width
        self.max_floors = max_floors

        # Spacing between elevators
        self.elevator_spacing = CONFIG["building"]["elevator_spacing"]
        self.margin = CONFIG["building"]["margin"]

        # Create the floors
        self.floors = [Floor(self, i, self.width) for i in range(num_floors)]

        # Create the elevators
        self.elevators = []
        elevator_width = CONFIG["elevator"]["width"]
        available_width = self.width - 2 * self.margin - CONFIG["floor"]["button_width"] - CONFIG["floor"]["button_margin"]

        if num_elevators > 0:
            # Calculate spacing between elevators
            total_elevator_width = num_elevators * elevator_width
            total_spacing = (num_elevators - 1) * self.elevator_spacing

            if total_elevator_width + total_spacing > available_width:
                # Adjust spacing if there is not enough space
                self.elevator_spacing = max(2, (available_width - total_elevator_width) / (num_elevators - 1) if num_elevators > 1 else 0)

            # Create elevators at calculated positions
            start_x = self.margin + CONFIG["floor"]["width"] + CONFIG["floor"]["margin_left"]
            for i in range(num_elevators):
                x = start_x + i * (elevator_width + self.elevator_spacing)
                self.elevators.append(ElevatorFactory.create(self, i, x + self.position[0]))

    def request_elevator(self, floor_num):
        """
        Request an elevator to a specific floor

        Args:
            floor_num: Floor number requesting the elevator

        Returns:
            float: Estimated time for elevator arrival (in seconds)
        """
        # Find the available elevator with the fastest arrival time
        best_elevator = None
        min_arrival_time = float('inf')
        for elevator in self.elevators:
            arrival_time = elevator.get_estimated_arrival_time(floor_num)

            # Choose the elevator with the shortest arrival time
            if arrival_time < min_arrival_time:
                min_arrival_time = arrival_time
                best_elevator = elevator

        if best_elevator:
            # Activate the selected elevator
            arrival_time = best_elevator.add_call(floor_num)
            return arrival_time

    def elevator_arrived(self, elevator_id, floor_num):
        """
        Notify that an elevator has arrived at a floor

        Args:
            elevator_id: ID of the elevator that arrived
            floor_num: Floor number where the elevator arrived
        """
        # Update the floor that the elevator arrived
        self.floors[floor_num].elevator_arrived()

    def update(self, dt):
        """
        Update the state of the building and its objects

        Args:
            dt: Time passed since last update (in seconds)
        """
        # Update all floors
        for floor in self.floors:
            floor.update_timer(dt)

        # Update all elevators
        for elevator in self.elevators:
            elevator.update(dt)

    def handle_click(self, pos):
        """
        Handle mouse click

        Args:
            pos: Position of the click (x, y)
        """
        # Adjust click position relative to building position
        adjusted_pos = (pos[0] - self.position[0], pos[1] - self.position[1])

        # Check if the click hit any of the floor buttons
        for floor in self.floors:
            if floor.check_button_click(adjusted_pos):
                break  # Stop the loop if a button was clicked

    def draw(self, screen):
        """
        Draw the building on the screen

        Args:
            screen: The pygame drawing surface
        """
        # Save the current screen surface for overlay use
        # screen_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.num_floors * CONFIG["floor"]["height"])
        building_surface = pygame.Surface((self.width, self.num_floors * CONFIG["floor"]["height"]))
        building_surface.fill((252, 243, 232))  # Background color for the building

        # Draw the floors
        for floor in self.floors:
            floor.draw(building_surface)

        # Display the building on the screen
        screen.blit(building_surface, self.position)

        # Draw the elevators
        for elevator in self.elevators:
            elevator.draw(screen)
