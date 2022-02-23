import uuid
from .Entry import Entry


class ToDoList:

    
    def __init__(self, name: str, entries: 'list[Entry]'):
        self.name = name
        self.entries = entries
        self.id = uuid.uuid4().hex

    def _asdict(self):
        return self.__dict__    
