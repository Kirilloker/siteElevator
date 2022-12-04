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

import threading, time

def startShaftCheck():
    Shaft.checkShunt()


def startElevator():
    Elv.work()



t_Shaft = threading.Thread(target=startShaftCheck)

t_elevator = threading.Thread(target=startElevator)

t_manager = threading.Thread(target=Man.selectedFlor, args=(4,))

t_Shaft.start()

t_elevator.start()

t_manager.start()

time.sleep(10)
t_manager1 = threading.Thread(target=Man.selectedFlor, args=(8,))
t_manager1.start()

time.sleep(2)
t_manager2 = threading.Thread(target=Man.selectedFlor, args=(5,))
t_manager2.start()

time.sleep(4)
t_manager3 = threading.Thread(target=Man.selectedFlor, args=(2,))
t_manager3.start()

time.sleep(120)
t_manager4 = threading.Thread(target=Man.selectedFlor, args=(5,))
t_manager4.start()


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