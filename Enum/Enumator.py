import enum


class Way(enum.Enum):
    up = 1,
    down = 0


class Door(enum.Enum):
    close = 1,
    open = 0,


class ShuntType(enum.Enum):
    slowing = 1,
    stop = 0


class LogType(enum.Enum):
    Door = "Дверь"
    Warning = "Предупреждение"
    SelectFloor = "Выбран этаж"
    Elevator = "Лифт"
