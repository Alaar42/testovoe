import requests
import json
import pprint

url = 'http://127.0.0.1:5000/json-example'
data = {"login": "user123",
        "pass": "pass123"}

r = requests.post(url, json=data)
data_recieve = r.json()
datanew = {'token': ''}
datanew['token']= 'Bearer_'+data_recieve['token']

print(datanew)


url_message_post = 'http://127.0.0.1:5000/json-message'
message_to_post = input('введите сообщение для отправки в базу')
data = {"message": message_to_post}
r = requests.post(url_message_post, json=data, headers=datanew)
print(r.json())

