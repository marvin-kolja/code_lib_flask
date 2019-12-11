from app import app

import threading
import json

from app.reader import Reader

from app.temp import Temp

import os

temp = Temp()

decoration = " ** "

def run_job():
    while True:
        reader = Reader()
        returned = reader.read()
        if returned == '0x0':
            print("Scanner error!")
            temp.temp(returned, "id", "w")
            continue
        else: 
            if temp.temp(None, "write_status", "r") == True:
                temp.temp(returned, "id", "w")
    
thread = threading.Thread(target=run_job)

@app.before_request
def active_job():
    try:
        with open("app/temp/id.txt", "r") as f:
            print("File exist, will be deleted")
    except:
        pass
    else:
        os.system('rm app/temp/id.txt')
    
    


if __name__ == "__main__":

    print(f"{decoration}Waiting for Thread to be started")
    temp.temp(True, "write_status", "w")
    thread.start()
    print(f"{decoration}Thread started")

    app.run(host='0.0.0.0')
