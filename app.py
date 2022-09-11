import json
from flask import Flask, request
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from db import engine, user, token, messages
import jwt

app = Flask(__name__)


# приём сообщения с проверкой токена
@app.route('/json-message', methods=['GET', 'POST'])
def message_accept():
    if request.method == 'POST':
        try:
            data = request.get_json()
# Забираем логин и хеддеры
            user_msg = data['message']
            headers = request.headers

            # print(headers)
            token_user = str(headers['token'][7:]) #Можно сделать разделене по "_"
            # print(b)
            # Подключаемся к бд, чтобы сравнить токен
            Session = sessionmaker(bind=engine)
            session = Session()
            result1 = session.query(token).filter_by(token=token_user)
            #print(result1)
            last_row = result1[-1]
            user_login = last_row['login']
            #print(last_row)
            token_bd = str(last_row['token'])

            # проверка токена из запроса и базы
            if token_bd == token_user:
                print(user_msg)
                if user_msg == 'history 10':
                    data_msg_return = {'msg': {'user': 'text'},
                                       'error': ''}
                    new_list = []
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    result2 = session.query(messages).all()
                    for row in result2[-11:-1]:
                        data_msg_return['msg']['user'] = row["login"]
                        data_msg_return['msg']['text'] = row["message"]

                        new_list.append(str(data_msg_return))

                    new_list = json.dumps(new_list)

                    # delete last token
                    with engine.connect() as conn:
                        last_token_del = conn.execute(
                            insert(token),
                            [
                                {"login": user_login, "token": 'expired_token'},

                            ]
                        )
                    return new_list

                # запись сообщения в бд
                # и запись об истечении токена
                with engine.connect() as conn:
                    add_msg = conn.execute(
                        insert(messages),
                        [
                            {"login": user_login, "message": user_msg},

                        ]
                    )
                    last_token_del = conn.execute(
                        insert(token),
                        [
                            {"login": user_login, "token": 'expired_token'},

                        ]
                    )
            # ответ клиенту
            json_response = {"auth": 'success',
                             "msg": "сообщение записанно",
                             'error': ''
                             }
            return json_response
        except:

            json_response = {'error': 'wrong token'}
            return json_response


# Функция проверки кредов и выдача токена
@app.route('/json-example', methods=['GET', 'POST'])
def json_example():
    print("Получен запрос")
    if request.method == 'POST':
        try:
            error_msg = ''
            tkn = ''
            data = request.get_json()
            login = data['login']
            password = data['pass']
            print("New connection")
            Session = sessionmaker(bind=engine)
            session = Session()
            result = session.query(user).all()
            login_in_table = False
            # Проверка логина и пароля
            for row in result:
                if login == row.login and password == row.password:
                    login_in_table = True
                    tkn = token_generation(login)

                    # Создание токена если креды верны
                    with engine.connect() as conn:
                        add_token = conn.execute(
                            insert(token),
                            [
                                {"token": tkn, "login": login},

                            ]
                        )
                elif login == row.login and password != row.password:
                    login_in_table = True
                    error_msg = 'wrong password'
            # print(error_msg)
            if login_in_table == False:
                error_msg = 'No such user'

            json_response = {
                "error": error_msg,
                "token": str(tkn)}
            print(json_response)
            return json_response
        except:
            print('Неизвестная ошибка')


# Генерация токена
def token_generation(login):
    print(login)
    key = 'secret'
    tkn = jwt.encode({"name": login}, key, algorithm="HS256")
    return tkn


if __name__ == '__main__':
    app.run(debug=True)
