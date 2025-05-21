import pygame
import time
import json

# Load configuration file
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

class Elevator:
    def __init__(self, building, elevator_id, x_position):
        """
        Initialize a new elevator

        Args:
            building: Reference to the building object the elevator belongs to
            elevator_id: Unique identifier for the elevator
            x_position: X-axis position of the elevator
        """
        self.building = building
        self.id = elevator_id
        self.x = x_position

        # Load elevator image
        self.image = pygame.image.load(CONFIG["elevator"]["image_path"])
        self.image = pygame.transform.scale(self.image, (CONFIG["elevator"]["width"], CONFIG["elevator"]["height"]))

        # Load arrival sound
        self.ding_sound = pygame.mixer.Sound(CONFIG["sound"]["ding_path"])

        # Elevator attributes
        self.width = CONFIG["elevator"]["width"]
        self.height = CONFIG["elevator"]["height"]
        self.speed = CONFIG["elevator"]["speed"]
        self.door_open_time = CONFIG["elevator"]["door_open_time"]

        # Elevator state
        self.current_floor = 0
        self.target_floor = None
        self.y = self.calculate_y_position(self.current_floor)
        self.movement_start_time = None
        self.door_open_time_start = None
        self.is_moving = False
        self.is_door_open = False
        self.calls_queue = []

    def calculate_y_position(self, floor):
        """Calculate the Y position of the elevator based on the floor"""
        floor_height = CONFIG["floor"]["height"]

        # Position is at the bottom of the building minus the elevator height plus the offset to the desired floor
        building_height = self.building.max_floors * floor_height
        return building_height - floor_height * (floor + 1) + (floor_height - self.height) / 2

    def add_call(self, floor):
        """
        Add a call to the elevator

        Args:
            floor: The floor the elevator was called to

        Returns:
            Estimated arrival time
        """
        # If elevator is available and not currently moving
        if not self.is_moving and self.target_floor is None:
            self.target_floor = floor
            self.is_moving = True
            self.movement_start_time = time.time()
            return self.calculate_estimated_time(self.current_floor, floor)

        # If the elevator was already called to this floor, no need to add it again
        if floor in self.calls_queue or floor == self.target_floor:
            return self.get_estimated_arrival_time(floor)

        # Add the call to the queue
        self.calls_queue.append(floor)
        return self.get_estimated_arrival_time(floor)

    def calculate_estimated_time(self, from_floor, to_floor):
        """Calculate estimated travel time between floors"""
        floor_diff = abs(to_floor - from_floor)
        return floor_diff * self.speed + self.door_open_time

    def get_estimated_arrival_time(self, floor):
        """Calculate estimated arrival time to a specific floor"""
        current_time = time.time()

        # Remaining time to reach current target
        remaining_time = 0
        current_pos = self.current_floor

        if self.is_moving:
            # Time remaining to reach current target
            time_to_target = self.calculate_estimated_time(self.current_floor, self.target_floor)
            elapsed_time = current_time - self.movement_start_time
            remaining_time += max(0, time_to_target - elapsed_time)
            current_pos = self.target_floor
            
        if self.is_door_open:
            time_to_target = self.calculate_estimated_time(self.current_floor, self.target_floor) - self.door_open_time + self.door_open_time_start
            elapsed_time = current_time - self.movement_start_time
            remaining_time += max(0, time_to_target - elapsed_time)
            current_pos = self.target_floor

        # If requested floor is the current target
        if self.target_floor == floor:
            remaining_time += self.door_open_time
            return remaining_time
        
        # For each stop in the queue, calculate travel and stop time
        for f in self.calls_queue:
            travel_time = self.calculate_estimated_time(current_pos, f)
            remaining_time += travel_time
            if f == floor:
                return remaining_time
            current_pos = f

        # If the floor is not in the queue, it will be added at the end
        remaining_time += self.calculate_estimated_time(current_pos, floor) + self.door_open_time
        return remaining_time
    
    def arrived(self, target_y):
        self.y = target_y
        self.current_floor = self.target_floor
        self.is_moving = False
        self.is_door_open = True
        self.door_open_time_start = 0

        if self.ding_sound:
            self.ding_sound.play()

        self.building.elevator_arrived(self.id, self.current_floor)

    def update(self, dt):
        """
        Update the elevator's state

        Args:
            dt: Time elapsed since last update (in seconds)
        """
        # Check if the elevator is stopped with doors open
        if self.is_door_open:
            self.door_open_time_start += dt
            if self.door_open_time_start >= self.door_open_time:
                # Close the doors and set a new target if available
                self.is_door_open = False
                self.door_open_time_start = 0

                if self.calls_queue:
                    # Take the next target from the queue
                    self.target_floor = self.calls_queue.pop(0)
                    self.is_moving = True
                else:
                    self.target_floor = None
            return

        # If the elevator is not moving, no update needed
        if not self.is_moving or self.target_floor is None:
            return

        target_y = self.calculate_y_position(self.target_floor)
        direction = 1 if target_y > self.y else -1
        distance_to_move = CONFIG["floor"]["height"] / self.speed * dt
        self.y += max(distance_to_move, 1) * direction

        # Check if the elevator reached the target
        if (direction == 1 and self.y >= target_y) or (direction == -1 and self.y <= target_y):
            self.arrived(target_y)
            

    def draw(self, screen):
        """
        Draw the elevator on the screen

        Args:
            screen: The pygame drawing surface
        """
        screen.blit(self.image, (self.x, self.y))
