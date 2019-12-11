import json

class Temp():

    def __init__(self):
        pass

    def temp(self, data, file, option):
        path = f'app/temp/{file}.txt'
        json_data = {file: data}
        if option == "w":
            with open(path, "w") as _file:
                json.dump(json_data, _file)
        elif option == "r":
            with open(path, "r") as _file:
                _data = json.load(_file)
                return (_data[file])
        else:
            print("Temp file Error")