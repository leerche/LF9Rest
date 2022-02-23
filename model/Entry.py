import uuid
from .User import User


class Entry:

    
    def __init__(self, text: str, status: bool, user: User):
        self.text = text
        self.status = status
        self.user = user
        self.id = uuid.uuid4().hex

    def _asdict(self):
        return self.__dict__
        
