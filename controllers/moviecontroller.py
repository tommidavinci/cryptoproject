class MovieController:

    #################################################### setup
    def __init__(self, movie_store, movie_view):
        self.movie_store = movie_store
        self.movie_view = movie_view
        self.current_movie_list = []
    
    #################################################### Movie Functionality
    def get_precise_interested_movies(self, user_id):
        result = self.movie_store.get_precise_interested_movies(user_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that might be of interest to " + user_id)
            return error
        movies = self.movie_view.print_get_interested_movies(result)
        return movies

    def get_quick_interested_movies(self, user_id):
        result = self.movie_store.get_quick_interested_movies(user_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that might be of interest to " + user_id)
            return error
        movies = self.movie_view.print_get_interested_movies(result)
        return movies

    def get_similar_movies_by_genre(self, movie_id):
        result = self.movie_store.get_similar_movies_by_genre(movie_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that is similar to movie with " + movie_id)
            return error
        movies = self.movie_view.print_get_similar_movies_by_genre(movie_id, result)
        return movies

    def search_movie(self, movie_name):
        m_y = movie_name.split('--year ')
        if (len(m_y) > 1):
            result = self.movie_store.search_movie(m_y[0].strip(), m_y[1].strip())
        else:
            result = self.movie_store.search_movie(movie_name.strip())
        if not result:
            error = self.movie_view.print_error("Could not find any movie similar to " + movie_name)
            return error
        movies = self.movie_view.print_movies(movie_name, result)
        self.current_movie_list = result
        return movies

    #################################################### Review Functionality
    def list_reviews(self, user_id):
        result = self.movie_store.list_reviews(user_id)
        if not result:
            error = self.movie_view.print_error("No reviews present")
            return error
        return self.movie_view.print_list_reviews(result)

    def read_review(self, user_id, movie_id):
        result = self.movie_store.read_review(user_id, movie_id)
        if not result:
            error = self.movie_view.print_error("No review found for movie ID: " + str(movie_id))
            return error
        result = self.movie_view.print_review(result[0])
        return result

    def create_update_review(self, user_id, movie_id, title, review):
        result = self.movie_store.create_update_review(user_id, movie_id, title, review)
        if not result:
            error = self.movie_view.print_error("Could not create the review")
            return error
        result = self.movie_view.print_create_update_review(result[0])
        return result

    def delete_review(self, user_id, movie_id):
        result = self.movie_store.delete_review(user_id, movie_id)
        if not result:
            error = self.movie_view.print_error("Could not delete review for movie ID: " + str(movie_id))
            return error
        result = self.movie_view.print_delete_review(movie_id)
        return result
    
    #################################################### Rating Functionality
    def delete_movie_rating(self, user_id, movie_id):
        result = self.movie_store.delete_movie_rating(user_id, movie_id)
        if not result:
            error = self.movie_view.print_error("Could not delete the rating of the movie")
            return error
        movies = self.movie_view.print_delete_movie_rating(result)
        return movies

    def get_rated_movies(self, user_id):
        result = self.movie_store.get_rated_movies(user_id)
        if not result:
            error = self.movie_view.print_error("Could not find any movies that is rated by " + user_id)
            return error
        movies = self.movie_view.print_get_rated_movies(result)
        return movies

    def set_movie_rating(self, user_id, movie_id, rating):
        result = self.movie_store.set_movie_rating(user_id, movie_id, rating)
        if not result:
            error = self.movie_view.print_error("Could not rate specified movie", movie_id)
            return error
        movies = self.movie_view.print_set_movie_rating(result)
        return movies