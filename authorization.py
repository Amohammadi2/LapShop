from file_manager import load_users, save_users

def login():
    """ورود کاربر."""
    users = load_users()
    username = input("username: ")
    password = input("password: ")

    if username in users and users[username] == password:
        print("Login succeeded")
        input('Press enter to continue...')
        return username
    else:
        print("Username or password is incorrect")
        input('Press enter to continue...')
        return None

def register():
    """ثبت نام کاربر."""
    users = load_users()
    username = input("new username: ")
    password = input("new passwrod: ")

    if username in users:
        print("This username already exists, please choose another one")
        register() # repeat the process again
    else:
        users[username] = password
        save_users(users)
        print("Successfully registered")
        input('Press enter to continue...')