from elevator import Elevator

class ElevatorFactory:
    @staticmethod
    def create(building, index, base_x):
        return Elevator(building, index, base_x)
