from Enum.Enumator import Way, Door
from Logic.Shunt import Shunt
from Logic.db import DBData
import time


class Elevator:
    def __init__(self, speed: float, way: Way, position: float, door: Door, current_flor: int, lift_shaft):
        # Скорость лифта
        self.speed = speed
        # Направление лифта
        self.way = way
        # Позиция лифта
        self.position = position
        # Дверь открыта или закрыта
        self.door = door
        # Текущий этаж
        self.current_flor = current_flor
        self.manager = None
        self.lift_shaft = lift_shaft

    def setManager(self, manager):
        self.manager = manager

    def setCurrentFlor(self, current_flor):
        print("Установлен новый этаж", self.current_flor)
        self.current_flor = current_flor
        self.changeDB()

    def touchShunt(self, shunt: Shunt):
        #print("SHUNT: ", shunt.flor)
        #print("SHUNTyp: ", shunt.type)
        self.manager.touchShount(shunt)

    def setSpeed(self, speed):
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
            str_speed = "1"
        elif self.speed == 0.05:
            str_speed = "0.5"

        str_floor = str(self.current_flor)

        str_door = "Open"

        if self.door == Door.close:
            str_door = "Close"

        # print("speed",str_speed)
        # print("floor",str_floor)
        # print("door",str_door)
        dataDB = DBData("databaseData.db", 'dataSQL.sql', True)
        dataDB.Change(str_speed, str_floor, str_door)

    def work(self):
        while True:
            # print("Позиция лифта:", self.getPos())
            if self.speed != 0:
                if self.way == Way.up:
                    self.position += self.speed
                else:
                    self.position -= self.speed

            #print("POS: ", self.getPos())
            check_shunt = self.lift_shaft.checkShunt(self.getPos())
            if check_shunt is not None:
                self.touchShunt(check_shunt)

            time.sleep(0.2)
