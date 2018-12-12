class MovieController:
    def __init__(self, movie_store, movie_view):
        self.movie_store = movie_store
        self.movie_view = movie_view

    def search_movie(self, movie_name):
        result = self.movie_store.search_movie(movie_name)
        if not result:
            error = self.movie_view.print_error("Could not find any movie similar to " + movie_name)
            return error
        movies = self.movie_view.print_movies(movie_name, result)
        return movies

    def get_rated_movies(self, user_id):
        result = self.movie_store.get_rated_movies(user_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that is rated by " + user_id)
            return error
        movies = self.movie_view.print_get_rated_movies(user_id, result)
        return movies

    def get_similar_movies(self, movie_id):
        result = self.movie_store.get_similar_movies(movie_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that is similar to movie with " + movie_id)
            return error
        movies = self.movie_view.print_get_similar_movies(movie_id, result)
        return movies

    def get_interested_movies(self, user_id):
        result = self.movie_store.get_interested_movies(user_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that you are interested in")
            return error
        movies = self.movie_view.print_get_interested_movies(user_id, result)
        return movies