#from Logic.Elevator import Elevator
from Enum.Enumator import Way, Door, ShuntType
from Logic.Timer import Timer
from Logic.Shunt import Shunt
import threading


class Manager:
    def __init__(self, elevator, amount_flors: int, drive_flor: int):
        # Количество этажей
        self.amount_flors = amount_flors
        # Ссылка на лифт
        self.elevator = elevator
        # Список этажей на которых нужно остановится
        self.list_stops: int = []
        # Этаж на который едем
        self.drive_flor = drive_flor
        self.timer = Timer(5, self)
        self.lockerADD = threading.Lock()
        self.lockerDELETE = threading.Lock()

    def selectedFlor(self, selected_flor: int):  # Сделать асинхронным !!!!
        if selected_flor > self.amount_flors or selected_flor <= 0:
            print("Такого этажа нет")
            return

        # Если выбранный этаж уже есть в списке - ничего не делаем
        if selected_flor in self.list_stops:
            print("Такой этаж уже есть в списке")
            return

        print("Выбран этаж:", selected_flor)

        # Ставим монитор в критической секции
        with self.lockerADD:
            
            # Если никуда не едем, то просто добавляем элемент в массив
            if self.drive_flor == -1 and selected_flor != self.elevator.current_flor:
                self.drive_flor = selected_flor
                self.list_stops.append(selected_flor)
                print("Добавлен1 этаж: ", selected_flor)
            else:
                if (self.elevator.way == Way.up and self.drive_flor > selected_flor > self.elevator.current_flor) \
                        or (self.elevator.way == Way.down and self.drive_flor < selected_flor < self.elevator.current_flor):
                    self.list_stops.append(self.drive_flor)
                    print("Добавлен2 этаж: ", selected_flor)
                    self.drive_flor = selected_flor
                # Иначе просто добавляем этаж в список
                else:
                    self.list_stops.append(selected_flor)
                    print("Добавлен3 этаж: ", selected_flor)

        print("Едем на этаж: ", self.drive_flor)

        # Если лифт стоит на месте то начать движение
        if self.elevator.speed == 0:
            #print("Мэнэджэер устанавливает скорость 0.1")
            #self.elevator.setSpeed(0.1)
            self.stopOnFlor()
    def stopOnFlor(self):
        with self.lockerDELETE:
            if self.drive_flor not in self.list_stops:
                return

            print("Лифт остановился, выбор следующего пути")
            # Сортируем массив по возрастанию

            self.list_stops.sort()
            # Получаем индекс этажа на который мы приехали
            index_flor = self.list_stops.index(self.drive_flor)

            print("Очередь этажей: ", self.list_stops)
            print("Индекс этажа на который приехали:", index_flor)

            if len(self.list_stops) == 1:
                self.list_stops.pop(0)
                return

            if self.elevator.way == Way.up and index_flor + 1 == len(self.list_stops):
                self.elevator.way = Way.down

            if self.elevator.way == Way.down and index_flor == 0:
                self.elevator.way = Way.up

            if self.elevator.way == Way.up:
                self.drive_flor = self.list_stops[index_flor + 1]
                self.list_stops.pop(index_flor)
            else:
                self.drive_flor = self.list_stops[index_flor - 1]
                self.list_stops.pop(index_flor)

            print("Лифт едет на этаж: ", self.drive_flor)
            print("Список остановок этажей:", self.list_stops)

            print("Мэнэджэер установил скорость лифта 0,1")
            self.elevator.setSpeed(0.1)  # !!!!!!!!!!!!!!!!!

    def touchShount(self, shunt: Shunt):
        if shunt.type == ShuntType.stop:
            self.elevator.current_flor = shunt.flor

        # Если шунт указывает на тот этаж который мы едем
        if self.drive_flor == shunt.flor:
            if shunt.type == ShuntType.stop:
                print("Лифт коснулся шунта Остановки")
                self.elevator.setSpeed(0)
                self.openDoor()
            elif shunt.type == ShuntType.slowing:
                print("Лифт коснулся шунта замедления")
                self.elevator.setSpeed(0.05)  # !!!!!!!!!!!!!!!!

    def closeDoor(self):
        if self.elevator.door == Door.open:
            print("Двери закрываются")
            self.elevator.close()
            self.stopOnFlor()

    def openDoor(self):
        if self.elevator.speed == 0 and self.elevator.door == Door.close:
            print("Двери открываются")
            self.elevator.open()
            self.timer.delayBeforeClose()  # Запустить ассинхронно

