from Enum.Enumator import Way, Door
from ElevatorProgram.Shunt import Shunt
from ElevatorProgram.db import DBData
import time


class Elevator:
    def __init__(self, speed: float, way: Way, position: float, door: Door, current_floor: int, lift_shaft):
        # Скорость лифта
        self.speed = speed
        # Направление лифта
        self.way = way
        # Позиция лифта
        self.position = position
        # Дверь открыта или закрыта
        self.door = door
        # Текущий этаж
        self.current_floor = current_floor
        self.manager = None
        self.lift_shaft = lift_shaft
        self.changeDB()

    def setManager(self, manager):
        self.manager = manager

    def setCurrentFloor(self, current_floor):
        if current_floor != self.current_floor:
            self.current_floor = current_floor
            print("Установлен новый этаж", self.current_floor)
            self.changeDB()

    def touchShunt(self, shunt: Shunt):
        self.manager.touchShunt(shunt)

    def setSpeed(self, speed):
        if self.speed != speed:
            self.speed = speed
            self.changeDB()

    def open(self):
        self.door = Door.open
        self.changeDB()

    def close(self):
        self.door = Door.close
        self.changeDB()

    def getPos(self):
        return round(self.position, 2)

    def changeDB(self):
        str_speed = ""

        if self.speed == 0:
            str_speed = "0"
        elif self.speed == 0.1:
            str_speed = "3"
        elif self.speed == 0.05:
            str_speed = "1"

        str_floor = str(self.current_floor)

        str_door = "Open"

        if self.door == Door.close:
            str_door = "Close"

        dataDB = DBData("databaseData.db", 'dataSQL.sql', True)
        dataDB.Change(str_speed, str_floor, str_door)

    def work(self):
        while True:
            if self.speed != 0:
                if self.way == Way.up:
                    self.position += self.speed
                else:
                    self.position -= self.speed

            check_shunt = self.lift_shaft.checkShunt(self.getPos())

            if check_shunt is not None:
                self.touchShunt(check_shunt)

            time.sleep(0.2)
