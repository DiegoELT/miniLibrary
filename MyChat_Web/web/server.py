from flask import Flask,render_template, request, session
from database import connector
from model import entities

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sessionclear')
def clearSesh():
    session.clear()
    return render_template('login.html')

@app.route('/login')
def login():
    if 'username' in session:
        return render_template('success.html')
    else:
        return render_template('login.html')

@app.route('/do_login', methods = ['POST'])
def do_login():

    username = request.form['username']
    password =  request.form['password']

    db_session = db.getSession(engine)
    users = db_session.query(entities.User)

    for user in users:
        if user.username == username and user.password == password:
            session['logged_user'] = username
            return render_template("success.html")
    return render_template("fail.html")

@app.route('/register', methods = ['GET'])
def register():
    return render_template("register.html")

@app.route('/do_register',methods = ['POST'])
def do_register():
    name = request.form['name']
    fullname = request.form['fullname']
    password = request.form['password']
    username = request.form['username']
    print(name, fullname, password, username)

    user = entities.User(username = username,
                         name = name,
                         fullname = fullname,
                         password = password)
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "Todo OK."

@app.route('/users', methods = ['GET'])
def users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    table = "<table><content></table>"
    fila = "<tr><td><id></td><td><name></td><td><fullname></td><td><username></td><td><password></td></tr>"
    filas = ""
    for user in users:
        temp = fila[:]
        temp = temp.replace("<id>",str(user.id))
        temp = temp.replace("<name>",user.name)
        temp = temp.replace("<fullname>", user.fullname)
        temp = temp.replace("<username>", user.username)
        temp = temp.replace("<password>", user.password)
        filas += temp
        print(temp)
    table = table.replace("<content>",filas)
    return table

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    response = ""
    for user in users:
        response += str(user.id)+"->"+user.name
    return response

@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        user.name = request.form['name']
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        user.username = request.form['username']
        db_session.add(user)
    db_session.commit()
    return "User updated!"


@app.route('/clean_users', methods = ['GET'])
def clear_users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    for user in users:
        db_session.delete(user)
    db_session.commit()
    return "Todos los usuarios eliminados Ó╭╮Ò "


@app.route('/users/<id>', methods = ['DELETE'])
def delete_users(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        db_session.delete(user)
    db_session.commit()
    return "User Deleted :C"

@app.route('/cuantasletras/<nombre>')
def cuantas_letras(nombre):
    return str(len(nombre))

@app.route('/sumar/<numero>')
def sumar(numero):
    if 'suma' not in session:
        session['suma'] = "0"

    session['suma'] = int(session['suma']) + int(numero)
    return str(session['suma'])

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('0.0.0.0'))
