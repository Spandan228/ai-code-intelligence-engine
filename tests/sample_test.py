def login(username, password):
    return username == "admin"

class Database:
    def connect(self):
        print("Connected")