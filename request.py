import requests

url = "http://localhost:5000/first/scancard"
myobj = {'id': '435897209420'}


x = requests.post(url, myobj)

print(x.text)