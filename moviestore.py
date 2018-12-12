class MovieStore:
    def __init__(self, db):
        self.db = db

    def search_movie(self, movie_name):
        #Search based on movie name, not genre, need to fix
        result = self.db.query("SELECT movie_id, title FROM movies WHERE to_tsvector('english',title) @@ '" + movie_name + "' LIMIT 10;")
        return result

    def get_rated_movies(self, user_id):
        return [(1,"The Avenger")]