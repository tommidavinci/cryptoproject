class MovieStore:
    def __init__(self, db):
        self.db = db

    def search_movie(self, movie_name):
        #Search based on movie name
        result = self.db.query("SELECT movie_id, title FROM movies WHERE to_tsvector('english',title) @@ '" + movie_name + "' LIMIT 10;")
        return result

    def get_rated_movies(self, user_id):
        #Need to implement
        return [(1,"The Avenger")]

    def get_similar_movies(self, movie_id):
        #Need to implement
        return [(1,"The Avenger"),(2,"Iron man"),(3,"Spiderman")]

    def get_interested_movies(self, user_id):
        #Need to implement
        return [(1,"Nothing"),(2,"Iron man"),(3,"Spiderman")]