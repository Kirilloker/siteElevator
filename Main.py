import sqlite3
from flask import Flask, render_template, request, make_response
from Logic.Elevator import Elevator
from Logic.Manager import Manager
from Logic.LiftShaft import LiftShaft
from Enum.Enumator import Way, Door
import threading
import logging

count_floors = 10

Shaft = LiftShaft(count_floors)

Elv = Elevator(speed=0,
               way=Way.up,
               position=1,
               door=Door.open,
               current_floor=1,
               lift_shaft=Shaft
               )

Man = Manager(elevator=Elv,
              amount_floors=count_floors,
              drive_floor=-1,
              )

Elv.setManager(Man)

t_elevator = threading.Thread(target=Elv.work)
t_elevator.start()

app = Flask(__name__, template_folder='templates')


def get_db_connection():
    conn = sqlite3.connect('databaseData.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    return post


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/info', methods=['GET'])
def getInfo():
    y = get_post(1)
    new_str = str(y[1]) + "/" + str(y[2]) + "/" + str(y[3])

    content = new_str
    res = make_response(content)
    res.headers['Content-Type'] = 'text'
    return res


@app.route('/button', methods=['POST'])
def postInfo():
    button = request.args.get('button')
    if button == 'close':
        Man.closeDoor()
    elif button == 'open':
        Man.openDoor()
    else:
        print("Выбран этаж: ", button)
        Man.selectedFloor(int(button))

    res = make_response()
    return res


app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

if __name__ == '__main__':
    app.run(host='192.168.1.116', port=8200, debug=False, use_reloader=False)
