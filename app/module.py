import app
import threading
import json
from reader import Reader

def w_temp(data):
    with open('app/temp/data.txt', 'w') as file:
        json.dump(data, file)
    print("id printed to file")

def run_job():
    global stop_writing_id
    while True:
        reader = Reader()
        returned = reader.read()
        if returned == '0x0':
            data = {"code": returned}
            print("Scanner error!")
            w_temp(data)
            continue
        else: 
            data = returned
            if stop_writing_id == False:
                w_temp(data)

thread = threading.Thread(target=run_job)

@app.before_first_request
def active_job():
    global stop_writing_id
    stop_writing_id = True
    print("Variables are global")
    thread.start()
    print("Thread started")