from flask import Flask, render_template, request
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from db import engine, user, token, messages
import random
import jwt

import string

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        login = str(request.form['login'])
        print(login)


@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        user = request.form.get('login')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(user, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/json-message', methods=['GET', 'POST'])
def message_accept():
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_msg = data['message']

            headers = request.headers

            b = str(headers['token'][7:])
            Session = sessionmaker(bind=engine)
            session = Session()
            # result1 = session.query.order_by(session.id.desc()).first()

            result1 = session.query(token).filter_by(token=b)

            last_row = result1[-1]
            user_login = last_row['login']
            print(last_row)
            a = str(last_row['token'])


            if a == b:
                print('ОН СРАВНИЛ')
                with engine.connect() as conn:
                    add_msg = conn.execute(
                        insert(messages),
                        [
                            {"login": user_login, "message": user_msg},

                        ]
                    )



            json_response = {"auth": 'success',
                             "msg": "сообщение записанно"}
            return json_response
        except:
            print("m?")


@app.route('/json-example', methods=['GET', 'POST'])
def json_example():
    print("Получен запрос")
    if request.method == 'POST':
        try:
            # print(request.get_json())
            data = request.get_json()

            login = data['login']
            password = data['pass']
            print("Connecting to DB")
            Session = sessionmaker(bind=engine)
            session = Session()
            result = session.query(user).all()

            print(result)
            for row in result:
                print(row)
                if login == row.login and password == row.password:
                    tkn = token_generation(login)
                    print(tkn)
                    with engine.connect() as conn:
                        add_token = conn.execute(
                            insert(token),
                            [
                                {"token": tkn, "login": login},

                            ]
                        )

            json_response = {"token": str(tkn)}
            return json_response
        except:
            print('error')


def token_generation(login):
    print(login)
    key = 'secret'
    tkn = jwt.encode({"name": login}, key, algorithm="HS256")
    # print(tkn)
    return tkn


if __name__ == '__main__':
    app.run(debug=True)
