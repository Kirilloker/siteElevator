from Enum.Enumator import Way, Door, ShuntType, LogType
from Logic.Timer import Timer
from Logic.Shunt import Shunt
import threading
from Logic.db import DBLog


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

    def selectedFloor(self, selected_floor: int):  # Сделать асинхронным !!!!
        if selected_floor > self.amount_floors or selected_floor <= 0:
            return

        # Если выбранный этаж уже есть в списке - ничего не делаем
        if selected_floor in self.list_stops:
            self.AddLog(LogType.Warning, "Был выбран этаж, который уже есть в списке очереди")
            return

        if selected_floor == self.elevator.current_floor:
            return 

        self.AddLog(LogType.SelectFloor, "В очередь был добавлен " + str(selected_floor) + " этаж")
        print("В очередь был добавлен " + str(selected_floor) + " этаж")

        # Ставим монитор в критической секции
        with self.lockerADD:
            # Если никуда не едем, то просто добавляем элемент в массив
            if self.elevator.speed == 0 and selected_floor != self.elevator.current_floor:
                self.drive_floor = selected_floor
                print("dr1: ", self.drive_floor)
                self.list_stops.append(selected_floor)
            else:
                if (self.elevator.way == Way.up and self.drive_floor > selected_floor > self.elevator.current_floor) \
                        or (
                        self.elevator.way == Way.down and self.drive_floor < selected_floor < self.elevator.current_floor):
                    #self.list_stops.append(self.drive_floor)
                    self.drive_floor = selected_floor
                    print("dr2: ", self.drive_floor)
                else:
                    self.list_stops.append(selected_floor)

        if self.elevator.speed == 0 and len(self.list_stops) == 1 and self.drive_floor in self.list_stops:
            self.closeDoor()
            self.FindNextFloor()

    def FindNextFloor(self):
        # Ставим монитор в критической секции
        with self.lockerDELETE:
            print("List stops:", self.list_stops)
            if len(self.list_stops) == 0 or self.list_stops is None:
                print("test0")
                return

            new_floor = None
            # Если едем вверх
            if self.elevator.way == Way.up:
                new_floor = self.GetUp(self.list_stops, self.elevator.current_floor)
                print("test1")
                if new_floor is None:
                    print("test2")
                    new_floor = self.GetDown(self.list_stops, self.elevator.current_floor)
            else:
                new_floor = self.GetDown(self.list_stops, self.elevator.current_floor)
                print("test3")
                if new_floor is None:
                    print("test4")
                    new_floor = self.GetUp(self.list_stops, self.elevator.current_floor)

            if new_floor is None:
                print("БЛЯЯЯЯЯЯТЬ ОШИКБАААА")
            else:
                print("Новый этаж эта ", new_floor)
            print("New flor:", new_floor)

            self.drive_floor = new_floor

            self.startMove()

    def touchShount(self, shunt: Shunt):
        # Когда проезжаем шунт остановки, меняем значения текущего этажа у лифта
        if shunt.type == ShuntType.stop:
            self.elevator.setCurrentFloor(shunt.floor)

        # Если шунт указывает на тот этаж который мы едем
        if self.drive_floor == shunt.floor:
            # Если это шунт остановки зануляем скорость
            # Если это шунт замедления, уменьшаем скорость

            if shunt.type == ShuntType.stop:
                self.elevator.setSpeed(0)

                if len(self.list_stops) != 0:
                    self.openDoor()

            elif shunt.type == ShuntType.slowing:
                self.elevator.setSpeed(0.05)

    def closeDoor(self):
        if self.elevator.door == Door.open:
            self.AddLog(LogType.Door, "Двери закрываются")
            print("Двери закрываются")

            self.elevator.close()
            # self.FindNextFloor()

    def openDoor(self):
        if self.elevator.speed == 0:
            self.AddLog(LogType.Elevator, "Лифт остановлен на этаже " + str(self.elevator.current_floor))
            self.AddLog(LogType.Door, "Двери открываются")
            print("Лифт остановлен на этаже " + str(self.elevator.current_floor))
            print("Двери открываются")

            print("LIST SROPPTS:", self.list_stops)
            if self.drive_floor in self.list_stops:

                print("из списка был удален:", self.drive_floor)
                self.list_stops.remove(self.drive_floor)
                print(self.list_stops)

            self.elevator.open()
            self.timer.delayBeforeClose()

    def startMove(self):
        if self.elevator.current_floor < self.drive_floor:
            self.elevator.way = Way.up
            self.AddLog(LogType.Elevator, "Лифт направляется вверх ")
            print("Лифт направляется вверх ")
        elif self.elevator.current_floor > self.drive_floor:
            self.elevator.way = Way.down
            self.AddLog(LogType.Elevator, "Лифт направляется вниз ")
            print("Лифт направляется вниз ")

        self.AddLog(LogType.Elevator, "Лифт поехал на этаж: " + str(self.drive_floor))
        print("Лифт поехал на этаж: " + str(self.drive_floor))

        self.elevator.setSpeed(0.1)


    def GetUp(self, array, current):
        array.sort()

        for i in range(len(array)):
            if array[i] > current:
                return array[i]

        return None


    def GetDown(self, array, current):
        print(array)
        array.sort()
        array.reverse()

        for i in range(len(array)):
            if array[i] < current:
                return array[i]

        return None

    def AddLog(self, type_log: LogType, message):
        dbLog = DBLog("databaseLog.db", 'LogSQL.sql')
        dbLog.AddNote(type_log, message)