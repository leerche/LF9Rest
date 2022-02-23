import uuid

from model.ToDoList import ToDoList
from .User import User
class Entry:

    
    def __init__(self, text: str, toDoList: ToDoList, user: User):
        self.text = text
        self.list = toDoList
        self.user = user
        self.id = uuid.uuid4().hex

    def _asdict(self):
        return self.__dict__
        
