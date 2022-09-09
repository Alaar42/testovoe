import requests
import json
import pprint


def get_token():
    url = 'http://127.0.0.1:5000/json-example'
    data = {"login": "user121",
            "pass": "pass123"}

    r = requests.post(url, json=data)
    data_recieve = r.json()

    if data_recieve['error'] == '':

        datanew = {'token': ''}
        datanew['token'] = 'Bearer_' + data_recieve['token']
        print(datanew)
        return datanew
    else:
        print(data_recieve['error'])
        return data_recieve['error']


def post_msg(datanew):
    url_message_post = 'http://127.0.0.1:5000/json-message'
    message_to_post = input('введите сообщение для отправки в базу')
    data = {"message": message_to_post}
    r = requests.post(url_message_post, json=data, headers=datanew)
    print(r.json())
    answer = input('хотите ещё? y/n')
    answer.lower()
    if answer == "y" or answer == 'да':
        post_msg(datanew)
    else:
        print('poka poka')


datanew = get_token()
#post_msg(datanew)
