class MovieStore:
    def __init__(self, db, graphdb):
        self.db = db
        self.graphdb = graphdb

    ## Anon 
    def search_movie(self, movie_name, year = -1, limit = 10):
        #Search based on movie name
        #result = self.db.query("SELECT movie_id, title FROM movies WHERE to_tsvector('english',title) @@ '" + movie_name + "' LIMIT 10;")
        return self.db.query_with_params("select * from search_movie_title(%s, %s, %s)", (movie_name, year, limit))

    def get_similar_movies(self, movie_id, limit = 10):
        return self.db.query_with_params("select * from recommend_movie_by_genre(%s,%s)",(movie_id, limit))


    ## User
    def get_rated_movies(self, user_id):
        ratings = self.graphdb.get_movies_rated_by_user(user_id)
        sqlLookup = ""
        result = []
        for record in ratings:
            sqlLookup += "" + str(record['m.id']) + ','
            result.append(['', "", "", record["r.rating"]])
        movieNamesAndYear = self.db.query("select * from get_movies(array["+ sqlLookup.rstrip(',') +"])")
        for movie, res in movieNamesAndYear, result:
            res[0] = movie[0]
            res[1] = movie[1]
            res[2] = movie[2]
        return result
   
    def get_interested_movies(self, user_id):
        #Need to implement
        return [(1,"Nothing"),(2,"Iron man"),(3,"Spiderman")]
    
    def set_movie_rating(self, user_id, movie_id, rating):
        rating = self.graphdb.set_movie_rating(user_id, movie_id, rating)
        result = []
        for record in rating:
            result = ["", "", "", record['r.rating']]
            movie_name_and_year = self.db.query_with_params("select * from get_movie(%s)", (record['m.id']))
        for field, res in movie_name_and_year, result:
            res = field
        return result
        


    def test(self):
        return self.graphdb.test()