from Logic.Elevator import Elevator
from Logic.Manager import Manager
from Logic.Shunt import Shunt
from Enum.Enumator import Way, ShuntType, Door

Elv = Elevator(speed=1,
               way=Way.up,
               position=1,
               door=Door.close,
               current_flor=1)

Man = Manager(Elv, 10, -1)

