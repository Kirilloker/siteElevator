#from Logic.Manager import Manager
from Enum.Enumator import Way, Door
from Logic.Shunt import Shunt
import time


class Elevator:
    def __init__(self, speed: float, way: Way, position: float, door: Door, current_flor: int, ):
        # Скорость лифта
        self.speed = speed
        # Направление лифта
        self.way = way
        # Позиция лифта
        self.position = position
        # Дверь открыта или закрыта
        self.door = door
        # Текущий этаж
        self.current_flor = current_flor  # ?
        self.manager = None

    def setManager(self, manager):
        self.manager = manager

    def TouchShunt(self, shunt: Shunt):
        self.manager.TouchShount(shunt)

    def setSpeed(self, speed):
        self.speed = speed

    def open(self):
        self.door = Door.open

    def close(self):
        self.door = Door.close

    def getPos(self):
        return round(self.position,2)

    def work(self):
        print("Позиция лифта:", self.getPos())
        print("Скорость лифта:", self.speed)
        # Запустить изначально асинхронно и крутить бесконечно
        if self.speed != 0:
            if self.way == Way.up:
                self.position += self.speed
            else:
                self.position -= self.speed

        time.sleep(1) # !!!!!!!!!!!!1
        self.work()
