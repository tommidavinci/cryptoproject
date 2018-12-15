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