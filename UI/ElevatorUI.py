from Logic.Elevator import Elevator
from Logic.Manager import Manager


class ElevatorUI:
    def __init__(self, elevator: Elevator, manager: Manager):
        self.elevator = elevator
        self.manager = manager

    def input_flor(self, selected_flor: int):
        self.manager.selectedFlor(selected_flor)