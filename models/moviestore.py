class MovieStore:
    def __init__(self, db, graphdb):
        self.db = db
        self.graphdb = graphdb

    ## Anon 
    def search_movie(self, movie_name, year = -1, limit = 10):
        #Search based on movie name
        #result = self.db.query("SELECT movie_id, title FROM movies WHERE to_tsvector('english',title) @@ '" + movie_name + "' LIMIT 10;")
        return self.db.query_with_params("select * from search_movie_title(%s, %s, %s)", (movie_name, year, limit))

    def get_similar_movies_by_genre(self, movie_id, limit = 10):
        return self.db.query_with_params("select * from recommend_movie_by_genre(%s,%s)",(movie_id, limit))

    ## User
    def delete_movie_rating(self, user_id, movie_id):
        result = self.graphdb.delete_movie_rating(user_id, movie_id)
        movieInfo = self.db.query("select * from get_movies(array[" + str(movie_id) + "])")
        result = []
        result.append(movieInfo[0][0])
        result.append(movieInfo[0][1])
        result.append(movieInfo[0][2])
        return result
    
    def get_precise_interested_movies(self, user_id):
        prelimResult = self.graphdb.get_precise_similar_users(user_id)
        recommended_movies = self.graphdb.get_movies_from_users_not_rated_by_x(user_id, prelimResult)
        result = []
        import random
        length = len(recommended_movies._records)
        for num in range(20):
            result.append(str(recommended_movies._records[random.randint(0, length)]['m.id']))
            print(result[num])
        result = self.db.query("select * from get_movies(array[" + ','.join(result) + "])")
        return result

    def get_rated_movies(self, user_id):
        ratings = self.graphdb.get_movies_rated_by_user(user_id)
        sqlLookup = ""
        result = []
        for record in ratings:
            sqlLookup += "" + str(record['m.id']) + ','
            result.append(['', "", "", record["r.rating"]])
        movies = self.db.query("select * from get_movies(array["+ sqlLookup.rstrip(',') +"])")
        for i in range(len(result)):
            result[i][0] = movies[i][0]
            result[i][1] = movies[i][1]
            result[i][2] = movies[i][2]
        return result
    
    def set_movie_rating(self, user_id, movie_id, rating):
        rating = self.graphdb.set_movie_rating(user_id, movie_id, rating)
        intVal = rating._records[0]['m.id']
        sqlRes = self.db.query("select * from get_movies(array[" + str(intVal) + "])")
        result = []
        result.append(sqlRes[0][0])
        result.append(sqlRes[0][1])
        result.append(sqlRes[0][2])
        result.append(rating._records[0]['r.rating'])
        return result

    def test(self):
        return self.graphdb.test()