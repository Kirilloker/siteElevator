from Enum.Enumator import ShuntType


class Shunt:
    def __init__(self, shunt_type: ShuntType, flor : int):
        self.type = shunt_type
        self.flor = flor
