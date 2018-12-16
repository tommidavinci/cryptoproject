class UserView:
    
    def print_error(self, message):
        return "Error: " + message

    def print_signup_failed(self, username):
        return "Error: Username \"{0}\" already in use".format(username) 

    def print_login_failed(self, message):
        return ""