import uuid

class User:
    def __init__(self, lastName: str, firstName: str, username: str, email: str):

        self.lastName = lastName
        self.firstName = firstName
        self.username = username
        self.email = email
        self.id = uuid.uuid4().hex
    
    def _asdict(self):
        return self.__dict__