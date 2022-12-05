from Enum.Enumator import Way, Door, ShuntType, LogType
from Logic.Timer import Timer
from Logic.Shunt import Shunt
import threading
from Logic.db import DBLog


class Manager:
    def __init__(self, elevator, amount_flors: int, drive_flor: int):
        # Количество этажей
        self.amount_flors = amount_flors
        # Ссылка на лифт
        self.elevator = elevator
        # Список этажей на которых нужно остановится
        self.list_stops = []
        # Этаж на который едем
        self.drive_flor = drive_flor
        self.timer = Timer(5, self)
        self.lockerADD = threading.Lock()
        self.lockerDELETE = threading.Lock()

    def selectedFlor(self, selected_flor: int):  # Сделать асинхронным !!!!
        if selected_flor > self.amount_flors or selected_flor <= 0:
            return

        # Если выбранный этаж уже есть в списке - ничего не делаем
        if selected_flor in self.list_stops:
            self.AddLog(LogType.Warning, "Был выбран этаж, который уже есть в списке очереди")
            return

        self.AddLog(LogType.SelectFlor, "В очередь был добавлен " + str(selected_flor) + " этаж")

        # Ставим монитор в критической секции
        with self.lockerADD:
            # Если никуда не едем, то просто добавляем элемент в массив
            if self.elevator.speed == 0 and selected_flor != self.elevator.current_flor:
                self.drive_flor = selected_flor
                self.list_stops.append(selected_flor)
            else:
                if (self.elevator.way == Way.up and self.drive_flor > selected_flor > self.elevator.current_flor) \
                        or (
                        self.elevator.way == Way.down and self.drive_flor < selected_flor < self.elevator.current_flor):
                    self.list_stops.append(self.drive_flor)
                    self.drive_flor = selected_flor
                else:
                    self.list_stops.append(selected_flor)

        if self.elevator.speed == 0:
            self.startMove()

    def stopOnFlor(self):
        # Ставим монитор в критической секции
        with self.lockerDELETE:
            if self.drive_flor not in self.list_stops:
                return

            self.list_stops.sort()

            # Получаем индекс этажа на который мы приехали
            index_flor = self.list_stops.index(self.drive_flor)

            if len(self.list_stops) == 1:
                self.list_stops.pop(0)
                return

            # Если едем вверх
            if self.elevator.way == Way.up:
                # Если не доехали до конца массива, то берем следующий элемент
                # Иначе предыдущий
                if index_flor + 1 != len(self.list_stops):
                    self.drive_flor = self.list_stops[index_flor + 1]
                else:
                    self.drive_flor = self.list_stops[index_flor - 1]
            # Если едем вниз
            else:
                # Если не достигли нижнего этажа в списке, то берем предыдущий элемент
                # Иначе берем следующий
                if index_flor != 0:
                    self.drive_flor = self.list_stops[index_flor - 1]
                else:
                    self.drive_flor = self.list_stops[index_flor + 1]

            # Удаляем этаж на который приехали
            self.list_stops.pop(index_flor)

            self.startMove()

    def touchShount(self, shunt: Shunt):
        # Когда проезжаем шунт остановки, меняем значения текущего этажа у лифта
        if shunt.type == ShuntType.stop:
            self.elevator.setCurrentFlor(shunt.flor)

        # Если шунт указывает на тот этаж который мы едем
        if self.drive_flor == shunt.flor:
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

            self.elevator.close()
            self.stopOnFlor()

    def openDoor(self):
        if self.elevator.speed == 0 and self.elevator.door == Door.close:
            self.AddLog(LogType.Elevator, "Лифт остановлен на этаже " + str(self.elevator.current_flor))
            self.AddLog(LogType.Door, "Двери открываются")

            self.elevator.open()
            self.timer.delayBeforeClose()

    def startMove(self):
        if self.elevator.current_flor < self.drive_flor:
            self.elevator.way = Way.up
        elif self.elevator.current_flor > self.drive_flor:
            self.elevator.way = Way.down

        self.AddLog(LogType.Elevator, "Лифт поехал на этаж: " + str(self.drive_flor))

        self.elevator.setSpeed(0.1)


    def AddLog(self, type_log: LogType, message):
        dbLog = DBLog("databaseLog.db", 'LogSQL.sql')
        dbLog.AddNote(type_log, message)