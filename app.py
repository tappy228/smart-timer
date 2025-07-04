from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from timer_logic import run_timer
import threading

app = Flask(__name__)
socketio = SocketIO(app)

stop_flag = [False]

@app.route('/')
def index():
    return render_template('form.html')  # страница с формой ввода

@app.route('/start', methods=['POST'])
def start():
    global stop_flag
    stop_flag[0] = False  # сброс флага перед стартом

    work_time = request.form['work_time']
    no_break = request.form['no_break']
    short_break = request.form['short_break']
    long_break = request.form['long_break']

    threading.Thread(target=run_timer, args=(work_time, no_break, short_break, long_break, socketio, stop_flag)).start()

    return render_template('timer.html')

@socketio.on('stop_timer')
def handle_stop_timer():
    global stop_flag
    stop_flag[0] = True  # устанавливаем флаг остановки
    emit('redirect_to_start')  # отправляем клиенту команду перенаправить

if __name__ == '__main__':
    socketio.run(app, debug=True)
