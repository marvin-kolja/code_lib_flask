# Server will be started in this script

from app import app



if __name__ == "__main__":
    # server can be accessed from other devices
    # !!! Has to be (localhost / 127.0.0.1) when implementing the system !!!
    app.run(host='0.0.0.0')
