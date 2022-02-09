class User:

    def __init__(self, name: str, firstName: str, username: str, email: str, id: int):
        self.name = name
        self.firstName = firstName
        self.username = username
        self.email = email
        self.id = id

    
    def _asdict(self):
        return self.__dict__