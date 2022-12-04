from Logic.Elevator import Elevator
from Logic.Manager import Manager
from Logic.LiftShaft import LiftShaft
from Logic.Shunt import Shunt
from Enum.Enumator import Way, ShuntType, Door


Elv = Elevator(speed=0,
               way=Way.up,
               position=1,
               door=Door.close,
               current_flor=1)

Man = Manager(elevator=Elv,
              amount_flors=10,
              drive_flor=-1)

Elv.setManager(Man)

Shaft = LiftShaft(10, Elv)

import threading



def startShaftCheck():
    Shaft.checkShunt()

def startElevator():
    Elv.work()



t_Shaft = threading.Thread(target=startShaftCheck)

t_elevator = threading.Thread(target=startElevator)

t_manager = threading.Thread(target=Man.SelectedFlor, args=(4,))

t_Shaft.start()

t_elevator.start()

t_manager.start()





"""
import asyncio

async def startProgramm():
    await Shaft.checkShunt()
    await test()

async def test():
    print("Hello world")

async def cook(order, time_to_prepare):
    print(f'Новый заказ: {order}')
    await asyncio.sleep(time_to_prepare)
    print(order, '- готово')

asyncio.run(startProgramm())
"""