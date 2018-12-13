class UserController:
    def __init__(self, user_store, user_view):
        self.user_store = user_store
        self.user_view = user_view

    def login(self, username, password):
        result = self.user_store.login(username,password)
        return 0

    def signup(self, username, password):
        result = self.user_store(username,password)
        return 0