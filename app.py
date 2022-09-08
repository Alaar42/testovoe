from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from db import engine, user, token
import random
import string
hello_world = "Nadyshka-Perdusha-Krasatushka"
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



@app.route('/json-example', methods=['GET', 'POST'])
def json_example():
    print("Получен запрос")
    if request.method == 'POST':
        try:
            #print(request.get_json())
            data = request.get_json()

            login = data['login']
            password = data['pass']

            print("Connecting to DB")
            Session = sessionmaker(bind=engine)
            session = Session()
            #result = session.query(user, token).all()
            result = session.query(user).all()

            print(result)
            for row in result:
                print(row)
                if login == row.login and password == row.password:
                    tkn = random.randint(0, 9999)

                    #tkn = row.token

            #print(tkn)
            json_response = {"token": str(tkn)}
            #print(login)
            return json_response
        except:
            print('error')




if __name__ == '__main__':
    app.run(debug=True)
