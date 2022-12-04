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
        self.timer = Timer(10, self)
        self.locker = threading.Lock()

    def SelectedFlor(self, selected_flor: int):  # Сделать асинхронным !!!!
        # Если номер этажа больше максимального количества или меньше нуля завершаем функцию
        if selected_flor > self.amount_flors or selected_flor <= 0:
            print("Такого этажа нет")
            return

        # Если выбранный этаж уже есть в списке - ничего не делаем
        if selected_flor in self.list_stops:
            print("Такой этаж уже есть в списке")
            return

        print("Выбран этаж:", selected_flor)
        # Если движемся вверх и был выбран этаж, который ниже того, куда мы едем
        # Но при этом выше того, на котором этаже мы сейчас,
        # То добавляем этаж к которому ехали в очередь, а выбранный этаж
        # Становится тем, к которму лифт стремится
        # + та же логика но если движемся вниз

        # Ставим монитор в кретической секции
        with self.locker:
            # Если никуда не едем, то просто добавляем элемент в массив
            if self.drive_flor == -1 and selected_flor != self.elevator.current_flor:
                self.list_stops.append(selected_flor)
            else:
                if (self.elevator.way == Way.up and self.drive_flor > selected_flor > self.elevator.current_flor) \
                        or (self.elevator.way == Way.down and self.drive_flor < selected_flor < self.elevator.current_flor):
                    self.list_stops.append(self.drive_flor)
                    self.drive_flor = selected_flor
                # Иначе просто добавляем этаж в список
                else:
                    self.list_stops.append(selected_flor)

        # Если лифт стоит на месте то начать движение
        if self.elevator.speed == 0:
            print("Мэнэджэер запускает лифт")
            self.stopOnFlor()

    def stopOnFlor(self):
        print("Лифт остановился, выбор следующего пути")
        # Получаем индекс этажа на который мы приехали
        index_flor = self.list_stops.index(self.drive_flor)
        # Сортируем массив по возрастанию
        self.list_stops.sort()

        # Если мы двигались вверх
        if self.elevator.way == Way.up:
            # Если достигли конца массива
            if index_flor + 1 == len(self.list_stops):
                # Разворачиваем лифт и вызываем эту же функцию
                self.elevator.way == Way.down
                self.stopOnFlor()
                return
            # Иначе выбираем следующий этаж к которому будем ехать выбрав следующий элемент массива
            # И удаляем тот этаж, на который приехали
            else:
                self.drive_flor = self.list_stops[index_flor + 1]
                self.list_stops.pop(index_flor)
        # Та же логика, но с движением лифта вниз
        else:
            if index_flor == 1:
                self.elevator.way == Way.up
                self.stopOnFlor()
                return
            else:
                self.drive_flor = self.list_stops[index_flor - 1]
                self.list_stops.pop(index_flor)

        print("Мэнэджэер установил скорость лифта 0,2")
        self.elevator.setSpeed(0.2)  # !!!!!!!!!!!!!!!!!

    def TouchShount(self, shunt: Shunt):
        # Если дотронулись до шунта, проверяем указывает ли этот
        # шунт, на этаж на который мы едем, если да, и останавливаем
        # или замедляем в зависимости от типа шунта
        if self.drive_flor == shunt.flor:
            if shunt.type == ShuntType.stop:
                self.elevator.setSpeed(0)
            elif shunt.type == ShuntType.slowing:
                self.elevator.setSpeed(0.05)  # !!!!!!!!!!!!!!!!

    def closeDoor(self):
        # Если дверь открыта - закрываем её
        if self.elevator.door == Door.open:
            self.elevator.close()

    def openDoor(self):
        # Если дверь закрыта и скорость лифта = 0, открываем дверь
        if self.elevator.speed == 0 and self.elevator.door == Door.close:
            self.elevator.open()
            self.timer.delayBeforeClose()  # Запустить ассинхронно
