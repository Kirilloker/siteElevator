import time
import asyncio

#from Shunt import Shunt
#from Elevator import Elevator
from Enum.Enumator import ShuntType
from Logic.Shunt import Shunt


class LiftShaft:
    def __init__(self, amount_flors:int, elevator):
        self.shunt: Shunt = []
        self.position_shunt: float= []
        self.amount_flors = amount_flors
        self.elevator = elevator
        self.createListShunt()

    def createListShunt(self):
        for i in range(1, self.amount_flors):
            self.position_shunt.append(i)
            self.shunt.append(Shunt(ShuntType.stop, i))

            self.position_shunt.append(i+0.3)
            self.shunt.append(Shunt(ShuntType.slowing, i))

            self.position_shunt.append(i+0.7)
            self.shunt.append(Shunt(ShuntType.slowing, i+1))

        self.position_shunt.append(self.amount_flors)
        self.shunt.append(Shunt(ShuntType.stop, self.amount_flors))

    def checkShunt(self):
        if self.elevator.getPos() in self.position_shunt:
            #print("*Лифт коснулся Шунта*")
            self.elevator.touchShunt(
                self.shunt[
                    self.position_shunt.index(self.elevator.getPos())
                          ])
        else:
            #print("*Лифт НЕ коснулся шунта*")
            pass

        time.sleep(0.1)
        self.checkShunt()
        #await asyncio.sleep(0.1)
        #await self.checkShunt()