from flask import Flask
import json
import humiditure as sensor
import sched, time
import threading
import datetime

app = Flask(__name__)

interval = 60

def read_humid_temp(max_attempts = 100):
    res = False
    n = 0
    while not res and n < max_attempts:
        res = sensor.read_dht11_dat()
        n += 1
        time.sleep(0.01)
    return res

def log_temp():
    res = read_humid_temp()
    if res:
        ts = datetime.datetime.now().timestamp()
        with open('./log.csv', 'a+') as f:
            f.write(f"{ts},{res[0]},{res[1]}\n")

def run_log(stop):
    while True and not stop():
        log_temp()
        time.sleep(interval)

@app.route('/')
def hello_world():
    res = read_humid_temp()
    if res:
        result_info = {
            "humidity": res[0],
            "temperature": res[1]
        }
        return json.dumps(result_info)
    return 'False'

started = False

if __name__ == '__main__' and not started:
    stqrted = True
    sensor.read_dht11_dat()
    stop_thread = False
    tread = threading.Thread(target=run_log, args=(lambda: stop_thread,))
    tread.start()
    app.run(debug=True, use_reloader=False, port=80, host='0.0.0.0')
    stop_thread = True
    tread.join()
    sensor.destroy()
