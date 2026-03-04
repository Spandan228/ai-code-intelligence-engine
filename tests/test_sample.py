def login_user(username, password):
    if username == "admin":
        return True
    return False


class DatabaseConnector:
    def connect(self):
        print("Connected")