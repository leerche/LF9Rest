
from flask import Flask, Response
from json import dumps
from model.User import User
from model.Entry import Entry

def default(o):
    return o._asdict()

users = [
    User("Rieping", "Lea", "LR", "Lea.Rieping@outlook.de", 1)
]

app = Flask(__name__)

@app.route('/v1/users', methods = ['GET'])
def getAllUsers():

    return Response(dumps(users, default=default), status=200, mimetype='application/json')

if __name__ == '__main__':
    # starte Flask-Server
    app.run(host='localhost', port=5000)



