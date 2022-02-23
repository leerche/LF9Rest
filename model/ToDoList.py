import uuid
class ToDoList:

    
    def __init__(self, name: str):
        self.name = name
        self.id = uuid.uuid4().hex

    def _asdict(self):
        return self.__dict__    
