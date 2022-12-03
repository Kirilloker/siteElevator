import time
import asyncio

from Shunt import Shunt
from Elevator import Elevator
from Enum.Enumator import ShuntType


class LiftShaft:
    def __init__(self, amount_flors:int, elevator: Elevator):
        self.shunt: Shunt = []
        self.position_shunt: float= []
        self.amount_flors = amount_flors
        self.elevator = elevator
        self.createListShunt()

    def createListShunt(self):
        for i in range(1, self.amount_flors):
            self.position_shunt.append(i)
            self.shunt(Shunt(ShuntType.stop, i))

            self.position_shunt.append(i+0.2)
            self.shunt(Shunt(ShuntType.slowing, i))

            self.position_shunt.append(i+0.8)
            self.shunt(Shunt(ShuntType.slowing, i+0.8))

        self.position_shunt.append(self.amount_flors)
        self.shunt(Shunt(ShuntType.stop, self.amount_flors))

    async def checkShunt(self):
        if self.elevator.position in self.position_shunt:
            print("*Лифт коснулся Шунта*")
            self.elevator.TouchShunt(
                self.shunt[
                    self.position_shunt.index(self.elevator.position)
                          ])
        else:
            print("*Лифт НЕ коснулся шунта*")
        time.sleep(0.1)
        self.checkShunt()
        #await asyncio.sleep(0.1)
        #await self.checkShunt()