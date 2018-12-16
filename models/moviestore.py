class MovieStore:
    def __init__(self, db):
        self.db = db

    ## Anon 
    def search_movie(self, movie_name, year = -1, limit = 10):
        #Search based on movie name
        #result = self.db.query("SELECT movie_id, title FROM movies WHERE to_tsvector('english',title) @@ '" + movie_name + "' LIMIT 10;")
        return self.db.query_with_params("select * from search_movie_title(%s, %s, %s)", (movie_name, year, limit))

    def get_similar_movies_by_genre(self, movie_id, limit = 10):
        return self.db.query_with_params("select * from recommend_movie_by_genre(%s,%s)",(movie_id, limit))

    ## User
    def get_rated_movies(self, user_id):
        #Need to 
        return [(1,"The Avenger")]
   
    def get_interested_movies(self, user_id):
        #Need to implement
        return [(1,"Nothing"),(2,"Iron man"),(3,"Spiderman")]