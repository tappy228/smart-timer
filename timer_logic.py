import pyttsx3
import time

all_time = 0
kol_vo_otd = 1

def run_timer(n1, n2, n3, n4, socketio, stop_flag):
    global all_time
    global kol_vo_otd
    
    all_time = 0
    kol_vo_otd = 1
    
    time__1 = n1  # строка "часы:минуты"
    stroka_time1 = [int(x) for x in time__1.split(":")]
    time1 = stroka_time1[0] * 60 * 60 + stroka_time1[1] * 60
    time_work = int(n2) * 60
    break_long = int(n3) * 60
    break_short = int(n4) * 60

    def send_status(phase, remaining):
        socketio.emit('timer_update', {
            'phase': phase,
            'time': f"{remaining // 60:02}:{remaining % 60:02}"
        })

    def breaky(x):
        global kol_vo_otd, all_time
        if all_time >= time1 or stop_flag[0]:
            return
        kol_vo_otd += 1
        for i in range(x, -1, -1):
            if stop_flag[0] or all_time >= time1:
                return
            all_time += 1
            print(f"осталось перерыва {i // 60} мин {i % 60} сек | прошло: {all_time // 60} мин {all_time % 60} сек")
            send_status("перерыв", i)
            time.sleep(1)

    def work(x):
        global all_time
        if stop_flag[0] or all_time >= time1:
            return
        print("пора работать")
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 2.0)
        engine.say("пора работать")
        engine.runAndWait()

        for i in range(x, -1, -1):
            if stop_flag[0] or all_time >= time1:
                return
            print(f"осталось работать {i // 60} мин {i % 60} сек | прошло: {all_time // 60} мин {all_time % 60} сек")
            send_status("работа", i)
            all_time += 1
            time.sleep(1)

        if kol_vo_otd % 4 != 0:
            print("пора сделать короткий перерыв")
            engine.say("пора сделать короткий перерыв")
            engine.runAndWait()
            breaky(break_short)
        else:
            print("пора сделать длинный перерыв")
            engine.say("пора сделать длинный перерыв")
            engine.runAndWait()
            breaky(break_short)
            breaky(break_long)

    if time1 == 0:
        print("пошел в жопу")
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 2.0)
        engine.say("пошел в жопу")
        engine.runAndWait()
        return

    while not stop_flag[0] and (time1 - all_time) > break_long + time_work:
        work(time_work)
    if not stop_flag[0]:
        work(time_work)
        print("время вышло")
