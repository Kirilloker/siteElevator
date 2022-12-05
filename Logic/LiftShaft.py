import time
from Enum.Enumator import ShuntType
from Logic.Shunt import Shunt


class LiftShaft:
    def __init__(self, amount_flors: int, elevator):
        self.shunt = []
        self.position_shunt = []
        self.amount_flors = amount_flors
        self.elevator = elevator
        # Создаем шунты
        self.createListShunt()

    def createListShunt(self):
        # Расставляем шунты в шахте лифта
        for i in range(1, self.amount_flors):
            self.position_shunt.append(i)
            self.shunt.append(Shunt(ShuntType.stop, i))

            self.position_shunt.append(i + 0.3)
            self.shunt.append(Shunt(ShuntType.slowing, i))

            self.position_shunt.append(i + 0.7)
            self.shunt.append(Shunt(ShuntType.slowing, i + 1))

        self.position_shunt.append(self.amount_flors)
        self.shunt.append(Shunt(ShuntType.stop, self.amount_flors))

    def checkShunt(self):
        while True:
            # Когда лифт касается шунта, сообщаем об этом
            if self.elevator.getPos() in self.position_shunt:
                self.elevator.touchShunt(
                    self.shunt[
                        self.position_shunt.index(self.elevator.getPos())
                              ])

            time.sleep(0.5)
