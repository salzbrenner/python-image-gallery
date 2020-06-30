class User:
    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def __repr__(self):
        return f"User with {self.username}, {self.password}, {self.full_name}"