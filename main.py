
from flask import Flask, Response, request
from json import dumps
from model.User import User
from model.Entry import Entry
from model.ToDoList import ToDoList

def default(o):
    return o._asdict()

def findUser(id):
    for user in users:
        if user.id == id:
            return user
    return None

def findList(id):
    for list in lists:
        if list.id == id:
            return list
    return None

def findEntry(id):
    for entry in entries:
        if entry.id == id:
            return entry
    return None

def findEntries(id):
    foundEntries = list()
    for entry in entries:
        if entry.list.id == id:
            foundEntries.append(entry)
    return foundEntries

users = [
    User("Lea Rieping"),
    User("Malte Rieping"),
    User("Hanno Rieping"),
    User("Michi Rieping")
]

lists = [
    ToDoList("Alte Liste"),
    ToDoList("Neue Liste")
]

entries = [
    Entry("Einkaufen gehen", users[0], lists[0]),
    Entry("Schlafen :)", users[1], lists[1])
]

app = Flask(__name__)

@app.route('/v1/users', methods = ['GET'])
def getAllUsers():
    return Response(dumps(users, default=default), status=200, mimetype='application/json')

@app.route('/v1/user', methods = ['POST'])
def addUser():
    args = request.form
    users.append(User(args.get('name')))
    return Response(dumps(users[-1], default=default), status=200, mimetype='application/json')

@app.route('/v1/user/<id>', methods = ['DELETE'])
def deleteUser(id):
    for index, user in enumerate(users, start=0):
        if user.id == id:
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
            entries = findEntries(list.id)
            return Response(dumps(entries, default=default), status=200, mimetype='application/json')
    return Response(status=404)

def deleteList(id):
    for index, list in enumerate(lists, start=0):
        if list.id == id:
            del lists[index]
            return Response(None, status=200, mimetype='application/json')
        else:
            list = None
    if list == None:
        return Response(status=404)


@app.route('/v1/list', methods = ['POST'])
def addList():
    args = request.form
    lists.append(ToDoList(args.get('name')))
    return Response(dumps(lists[-1], default=default), status=200, mimetype='application/json')

@app.route('/v1/list/<id>/entry', methods = ['POST'])
def addEntry(id):
    args = request.form
    user = findUser(args.get('userID'))
    toDoList = findList(id)
    if user != None and toDoList != None:
        entries.append(Entry(args.get('text'), toDoList, user))
        return Response(dumps(entries[-1], default=default), status=200, mimetype='application/json')
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
    entry = findEntry(entryId)
    if entry == None:
        return Response(status=404)
    user = findUser(args.get('user'))
    if user != None:
        entry.user = user
    if(args.get('text')):
        entry.text = args.get('text')
    return Response(dumps(entry, default=default), status=200, mimetype='application/json')
                    
def deleteEntry(id, entryId):
    for index, entry in enumerate(entries, start=0):
        if entry.id == entryId:
            del entries[index]
            return Response(None, status=200, mimetype='application/json')
    return Response(status=404)

if __name__ == '__main__':
    # starte Flask-ServerS
    app.run(host='localhost', port=5000)


