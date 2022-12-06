from Enum.Enumator import Way, Door, ShuntType, LogType
from ElevatorProgram.Timer import Timer
from ElevatorProgram.Shunt import Shunt
import threading
from ElevatorProgram.db import DBLog


def AddLog(type_log: LogType, message):
    dbLog = DBLog("databaseLog.db", 'LogSQL.sql')
    dbLog.AddNote(type_log, message)


def GetDown(array, current):
    array.sort()
    array.reverse()

    for i in range(len(array)):
        if array[i] < current:
            return array[i]

    return None


def GetUp(array, current):
    array.sort()

    for i in range(len(array)):
        if array[i] > current:
            return array[i]

    return None


class Manager:
    def __init__(self, elevator, amount_floors: int, drive_floor: int):
        # Количество этажей
        self.amount_floors = amount_floors
        # Ссылка на лифт
        self.elevator = elevator
        # Список этажей на которых нужно остановится
        self.list_stops = []
        # Этаж на который едем
        self.drive_floor = drive_floor
        self.timer = Timer(5, self)
        self.lockerADD = threading.Lock()
        self.lockerDELETE = threading.Lock()

    def selectedFloor(self, selected_floor: int):
        if selected_floor > self.amount_floors or selected_floor <= 0:
            return

        if selected_floor in self.list_stops:
            return

        if selected_floor == self.elevator.current_floor:
            return

        AddLog(LogType.SelectFloor, "В очередь был добавлен " + str(selected_floor) + " этаж")

        # Ставим монитор в критической секции
        with self.lockerADD:
            # Если никуда не едем, то просто добавляем элемент в массив
            if self.elevator.speed == 0 and selected_floor != self.elevator.current_floor:
                self.drive_floor = selected_floor
                self.list_stops.append(selected_floor)
            else:
                if (self.elevator.way == Way.up and self.drive_floor > selected_floor > self.elevator.current_floor) \
                        or (self.elevator.way == Way.down and self.drive_floor < selected_floor < self.elevator.current_floor):
                    self.drive_floor = selected_floor
                else:
                    self.list_stops.append(selected_floor)

        if self.elevator.speed == 0 and len(self.list_stops) == 1 and self.drive_floor in self.list_stops:
            self.closeDoor()
            self.findNextFloor()

    def findNextFloor(self):
        # Ставим монитор в критической секции
        with self.lockerDELETE:
            if len(self.list_stops) == 0 or self.list_stops is None:
                return

            new_floor = None

            # Если едем вверх
            if self.elevator.way == Way.up:
                new_floor = GetUp(self.list_stops, self.elevator.current_floor)
                if new_floor is None:
                    new_floor = GetDown(self.list_stops, self.elevator.current_floor)
            else:
                new_floor = GetDown(self.list_stops, self.elevator.current_floor)
                if new_floor is None:
                    new_floor = GetUp(self.list_stops, self.elevator.current_floor)

            if new_floor is None:
                print("Error!")

            self.drive_floor = new_floor

            self.startMove()

    def touchShunt(self, shunt: Shunt):
        # Когда проезжаем шунт остановки, меняем значения текущего этажа у лифта
        if shunt.type == ShuntType.stop:
            self.elevator.setCurrentFloor(shunt.floor)

        # Если шунт указывает на тот этаж который мы едем
        if self.drive_floor == shunt.floor:
            if shunt.type == ShuntType.stop:
                self.elevator.setSpeed(0)

                # ?
                if len(self.list_stops) != 0:
                    AddLog(LogType.Elevator, "Лифт остановлен на этаже " + str(self.elevator.current_floor))

                    if self.drive_floor in self.list_stops:
                        self.list_stops.remove(self.drive_floor)

                    self.openDoor()

            elif shunt.type == ShuntType.slowing:
                self.elevator.setSpeed(0.05)

    def closeDoor(self):
        if self.elevator.door == Door.open:
            AddLog(LogType.Door, "Двери закрываются")
            self.elevator.close()

    def openDoor(self):
        if self.elevator.speed == 0:
            AddLog(LogType.Door, "Двери открываются")
            self.elevator.open()
            self.timer.delayBeforeClose()

    def startMove(self):
        if self.elevator.current_floor < self.drive_floor:
            self.elevator.way = Way.up
            AddLog(LogType.Elevator, "Лифт направляется вверх ")
        elif self.elevator.current_floor > self.drive_floor:
            self.elevator.way = Way.down
            AddLog(LogType.Elevator, "Лифт направляется вниз ")

        AddLog(LogType.Elevator, "Лифт движется на этаж: " + str(self.drive_floor))

        self.elevator.setSpeed(0.1)
