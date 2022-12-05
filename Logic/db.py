import sqlite3
from Enum.Enumator import LogType


class DBLog:
    def __init__(self, name, ex_script, clearDB=False):
        self.name = name
        self.ex_script = ex_script
        self.connection = sqlite3.connect(name)
        self.cur = None
        self.createDB(clearDB)

    def createDB(self, clearDB):
        if clearDB:
            with open(self.ex_script) as f:
                self.connection.executescript(f.read())

        self.cur = self.connection.cursor()

    def AddNote(self, type_note: LogType, message: str):
        self.cur.execute("INSERT INTO posts (tag, content) VALUES (?, ?)",
                    (type_note.value, message)
                    )
        self.connection.commit()

    def __del__(self):
        self.connection.close()


class DBData:
    def __init__(self, name, ex_script, clearDB=False):
        self.name = name
        self.ex_script = ex_script
        self.connection = sqlite3.connect(name)
        self.cur = None
        self.createDB(clearDB)

    def createDB(self, clearDB):
        if clearDB:
            with open(self.ex_script) as f:
                self.connection.executescript(f.read())

        self.cur = self.connection.cursor()

    def Change(self, str_speed, str_floor, str_door):
        self.cur.execute("INSERT INTO posts (_speed, _floor, _door) VALUES (?, ?, ?)",
                   (str_speed, str_floor, str_door)
                   )

        self.connection.commit()

    def __del__(self):
        self.connection.close()
