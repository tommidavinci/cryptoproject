movie_format =          "id: {0} | {1} - {2}\na.k.a {3}\n" 
review_format =         "id: {0} | {1} - {2}\n{3}\n{4}\n\n{5}\n\nBy:{6}"
list_review_format =    "id: {0} | {1} - {2} | '{3}'\n"
class MovieView:
    
    #################################################### Movies
    def print_movies(self, movie_name, movies):
        result = "Found movies that is similar to search string \"{0}\"\n".format(movie_name)
        for movie in movies:
            result += movie_format.format(movie[0], self.array_to_string(movie[1]), movie[2])
        return result

    def print_get_interested_movies(self, movies):
        result = "Found movies that you might get interested based on your prior ratings:\n"
        for movie in movies:
            result += movie_format.format(movie[0], self.array_to_string(movie[1]), movie[2])
        return result

    def print_get_similar_movies_by_genre(self, movie_id, movies): # Which is called?
        result = "Found movies of similar genre to {0} - {1}\n".format(movies[0],movie_format[2])
        for i in range(1,len(movies)):
            result += movie_format.format(movies[i][0], movies[i][1][0], movies[i][2])
            if len(movies[i][1]) > 1:
                result += "    A.K.A.: "
                for j in range(1, len(movies[i][1])):
                        result += movies[i][1][j] + " | "
        return result.rstrip(" | ")
    
    #################################################### Rating
    def print_delete_movie_rating(self, movies):
        result = "Deleted rating of movie: \n"
        result += movie_format.format(movies[0], movies[1].pop(0), movies[2], self.array_to_string(movies[1]))
        return result

    def print_get_rated_movies(self, movies):
        result = "Found movies that you have rated: \n"
        for movie in movies:
            result += "Movie Id: {0}   -  Movie Name: {1} - Year: {2}   -  Rating: {3}\n".format(movie[0], self.array_to_string(movie[1]), movie[2], movie[3])
        return result
    

    def print_set_movie_rating(self, movies):
        result = "Rated movie: \n"
        result += "Movie Id: {0}   -  Movie Name: {1} - Year: {2}   -  Rating: {3}\n".format(movies[0], self.array_to_string(movies[1]), movies[2], movies[3])
        return result
    
    #################################################### Review
    def print_list_reviews(self, reviews):
        result = "List of reviewed movies\n"
        for review in reviews:
            result += list_review_format.format(str(review[0]),review[1],str(review[2]),review[3])
        return result
    
    def print_review(self, review):
        return review_format.format(review[0],review[1].pop(0),review[2], self.array_to_string(review[1]),review[4],review[5], review[3])

    def print_create_update_review(self, review):
        result = "Created or updated review: \n"
        result += review_format.format(str(review[0]),review[1].pop(0), str(review[2]),
                                        self.array_to_string(review[1]), review[4], review[5], review[3])
        return result
    
    def print_delete_review(self, movie):
        result = "Deleted review of movie ID: " + str(movie)
        return result

    #################################################### Menus
    def print_user_functions(self, userName):
        welcome = '\nWelcome {}'.format(userName)
        welcome += '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that has similar genres with a given movie'

        welcome += '\n3. List all the movies that you might interested in (Precise)' #?
        welcome += '\n4. List all the movies that you have rated' 
        welcome += '\n5. Rate a movie or update an existing rating ' # c rating
        # welcome += '\n6. Edit your rate for a movie' 
        welcome += '\n6. Delete your rate for a movie'
        
        welcome += '\n7. List all movies that you reviewed'
        welcome += '\n8. Read a review'
        welcome += '\n9. Create or Update a review for a movie'
        welcome += '\n10. Delete your review for a movie'
        # welcome += '\n11. Create a user (Admin right)'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        return welcome

    def print_anon_functions(self, userName):
        welcome = '\nWelcome {}'.format(userName)
        welcome = '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that has similar genres with a given movie'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        return welcome

    #################################################### Utility & Error
    def array_to_string(self, array):
        if len(array) > 0:
            res = "a.k.a. "
            for item in array:
                res += str(item) + " | a.k.a. "
            return res.rstrip(" | a.k.a. ")
        return ""

    def print_error(self, message):
        return "Error: " + message