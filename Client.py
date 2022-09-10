import requests
import json



# CREDS FOR TESTING : (put them in data row(19))
# data = {"login": "Bob",
#         "pass": "coolPass42"}
# data = {"login": "Wrong_logind",
#         "pass": "nvm"}
# data = {"login": "user123",
#         "pass": "wrong_pass"}



# Функция получения токена
def get_token():
    url = 'http://127.0.0.1:5000/json-example'
    data = {"login": "asd1",
            "pass": "asd"}
    r = requests.post(url, json=data)
    data_recieve = r.json()
# Проверка на ошибку, если нет - продолжить
    if data_recieve['error'] == '':

        datanew = {'token': ''}
        datanew['token'] = 'Bearer_' + data_recieve['token']
        print(datanew)
        return datanew
    else: # Вывод ошибки, если такая присутсвует
        print(data_recieve['error'])
        return data_recieve

# Отправка сообщений с токеном из get_token(), если получили ошибку,
# то проверяем пост с неверным токеном
def post_msg(datanew):
    url_message_post = 'http://127.0.0.1:5000/json-message'
    message_to_post = input('введите сообщение для отправки в базу ')
    data = {"message": message_to_post}

    r = requests.post(url_message_post, json=data, headers=datanew)
    response = r.json()
    print(response)
    print('poka poka')


datanew = get_token()
# print(type(datanew))

post_msg(datanew)
