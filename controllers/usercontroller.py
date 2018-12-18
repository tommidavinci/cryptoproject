class UserController:

    #################################################### setup
    def __init__(self, user_store, user_view):
        self.user_store = user_store
        self.user_view = user_view

    #################################################### Functionality
    def login(self, username, password):
        return self.user_store.login(username,password)

    def signup(self, username, password):
        return self.user_store.signup(username,password)