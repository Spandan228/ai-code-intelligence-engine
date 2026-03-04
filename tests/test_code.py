def login_user(username, password):
    return username == "admin" and password == "123"

def connect_database():
    print("Connected")