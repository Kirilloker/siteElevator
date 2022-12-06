import time
from Enum.Enumator import ShuntType
from Logic.Shunt import Shunt


class LiftShaft:
    def __init__(self, amount_floors: int):
        self.shunt = []
        self.position_shunt = []
        self.amount_floors = amount_floors
        # Создаем шунты
        self.createListShunt()

    def createListShunt(self):
        # Расставляем шунты в шахте лифта
        for i in range(1, self.amount_floors):
            self.position_shunt.append(i)
            self.shunt.append(Shunt(ShuntType.stop, i))

            self.position_shunt.append(i + 0.3)
            self.shunt.append(Shunt(ShuntType.slowing, i))

            self.position_shunt.append(i + 0.7)
            self.shunt.append(Shunt(ShuntType.slowing, i + 1))

        self.position_shunt.append(self.amount_floors)
        self.shunt.append(Shunt(ShuntType.stop, self.amount_floors))

    def checkShunt(self, elevator_pos):

        # Когда лифт касается шунта, сообщаем об этом
        if elevator_pos in self.position_shunt:
            return self.shunt[self.position_shunt.index(elevator_pos)]

        return None


