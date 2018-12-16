class MovieView:

    def print_error(self, message):
        return "Error: " + message

    def print_movies(self, movie_name, movies):
        result = "Found movies that is similar to search string {0}\n".format(movie_name)
        for movie in movies:
            result += "Movie Id: {0}   -  Movie Name: {1} - Year: {2}\n".format(movie[0], movie[1], movie[2])
        return result

    def print_get_rated_movies(self, user_id, movies):
        result = "Found movies that you have rated: \n"
        for movie in movies:
            result += "Movie Id: {0}   -  Movie Name: {1}\n".format(movie[0], movie[1])
        return result

    def print_get_similar_movies(self, movie_id, movies):
        result = "Found movies that has similar genres with movie ID {0}:\n".format(movie_id)
        for movie in movies:
            result += "Movie Id: {0}   -  Movie Name: {1}\n".format(movie[0], movie[1])
        return result

    def print_get_interested_movies(self, user_id, movies):
        result = "Found movies that you might get interested:\n"
        for movie in movies:
            result += "Movie Id: {0}   -  Movie Name: {1}\n".format(movie[0], movie[1])
        return result

    def print_user_functions(self, userName):
        welcome = '\nWelcome {}'.format(userName)
        welcome += '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that has similar genres with a given movie'
        welcome += '\n3. List all the movies that you have rated or reviewed' 
        welcome += '\n4. List all the movies that you might interested in' #?
        welcome += '\n5. Rate a movie' # c rating
        welcome += '\n6. Edit your rate for a movie' 
        welcome += '\n7. Delete your rate for a movie'
        welcome += '\n8. Create a review for a movie'
        welcome += '\n9. Edit your review for a movie'
        welcome += '\n10. Delete your review for a movie'
        welcome += '\n11. Create a user (Admin right)'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        return welcome

    def print_anon_functions(self, userName):
        welcome = '\nWelcome {}'.format(userName)
        welcome = '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that has similar genres with a given movie'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        return welcome