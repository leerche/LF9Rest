
from flask import Flask, Request, Response, request
from json import dumps
from model.User import User
from model.Entry import Entry
from model.ToDoList import ToDoList
from distutils.util import strtobool


def default(o):
    return o._asdict()

users = [
    User("Rieping", "Lea", "LR", "Lea.Rieping@outlook.de"),
    User("Rieping", "Malte", "MR", "Malte.Rieping@outlook.de"),
    User("Rieping", "Michi", "MR2", "Michi.Rieping@outlook.de"),
    User("Rieping", "Hanno", "HR", "Hanno.Rieping@outlook.de")
]

def findUser(id):
    for user in users:
        if user.id == id:
            return user
    return None


entries = [
    Entry("Einkaufen gehen", "NOT DONE", users[0]),
    Entry("Schlafen :)", ":D", users[1])
]

lists = [
    ToDoList("Alte Liste", [entries[0], entries[1]]),
    ToDoList("Neue Liste", [entries[0]])
]

app = Flask(__name__)

@app.route('/v1/users', methods = ['GET'])
def getAllUsers():
    return Response(dumps(users, default=default), status=200, mimetype='application/json')

@app.route('/v1/user', methods = ['POST'])
def addUser():
    args = request.form
    users.append(User(args.get('lastName'), args.get('firstName'), args.get('username'), args.get('email')))
    return Response(dumps(users[-1], default=default), status=200, mimetype='application/json')

@app.route('/v1/user/<id>', methods = ['DELETE'])
def deleteUser(id):
    for index, user in enumerate(users, start=0):
        if int(user.id) == int(id):
            del users[index]
            break
        else:
            user = None

    if user == None:
        return Response(status=404)
    return Response(None, status=200, mimetype='application/json')

@app.route('/v1/list/<id>', methods = ['GET', 'DELETE'])
def singleList(id):
    if request.method == 'GET':
        return getList(id)
    elif request.method == 'DELETE':
        return deleteList(id)

def getList(id):
    for list in lists:
        if list.id == id:
            return Response(dumps(list, default=default), status=200, mimetype='application/json')
    return Response(status=404)

def deleteList(id):
    for index, list in enumerate(lists, start=0):
        if list.id == id:
            del lists[index]
            break
        else:
            list = None

    if list == None:
        return Response(status=404)
    return Response(None, status=200, mimetype='application/json')

@app.route('/v1/list', methods = ['POST'])
def addList():
    args = request.form
    lists.append(ToDoList(args.get('name'), []))
    return Response(dumps(lists[-1], default=default), status=200, mimetype='application/json')

@app.route('/v1/list/<id>/entry', methods = ['POST'])
def addEntry(id):
    args = request.form

    for list in lists:
        if list.id == id:
            user = findUser(args.get('user'))
            if user != None:
                list.entries.append(Entry(args.get('text'), strtobool(args.get('status')), user))
                return Response(dumps(list.entries[-1], default=default), status=200, mimetype='application/json')
    # nicht in unserer Spezifikation
    return Response(status=404)

@app.route('/v1/list/<id>/entry/<entryId>', methods = ['DELETE', 'POST'])
def singleEntry(id, entryId):
    if request.method == 'POST':
        return updateEntry(id, entryId)
    elif request.method == 'DELETE':
        return deleteEntry(id, entryId)


def updateEntry(id, entryId):
    args = request.form
    for list in lists:
        if list.id == id:
            for entry in list.entries:
                if entry.id == entryId:
                    entry.status =  strtobool(args.get('status'))
                    user = findUser(args.get('user'))
                    if user != None:
                        entry.user = user
                    entry.text = args.get('text')
                    return Response(dumps(entry, default=default), status=200, mimetype='application/json')
    return Response(status=404)


def deleteEntry(id, entryId):
    for list in lists:
        if list.id == id:
            for index, entry in enumerate(list.entries, start=0):
                if entry.id == entryId:
                    del list.entries[index]
                    return Response(None, status=200, mimetype='application/json')
    return Response(status=404)



if __name__ == '__main__':
    # starte Flask-ServerS
    app.run(host='localhost', port=5000)


