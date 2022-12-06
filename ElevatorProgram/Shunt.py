from Enum.Enumator import ShuntType


class Shunt:
    def __init__(self, shunt_type: ShuntType, floor: int):
        self.type = shunt_type
        self.floor = floor
