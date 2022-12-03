from Logic.Elevator import Elevator
from Logic.Manager import Manager
from Logic.LiftShaft import LiftShaft
from Logic.Shunt import Shunt
from Enum.Enumator import Way, ShuntType, Door


Elv = Elevator(speed=1,
               way=Way.up,
               position=1,
               door=Door.close,
               current_flor=1)

Man = Manager(Elv, 10, -1)

Elv.setManager(Man)

Shaft = LiftShaft(10, Elv)




import asyncio

async def startProgramm():
    await Shaft.checkShunt()
    print("Hello world")

async def cook(order, time_to_prepare):
    print(f'Новый заказ: {order}')
    await asyncio.sleep(time_to_prepare)
    print(order, '- готово')

asyncio.run(startProgramm())