movie_format =          "id: {0} | {1} - {2}\n{3}\n" 
review_format =         "id: {0} | {1} - {2}\n{3}\n{4}\n\n{5}\n\nBy:{6}"
list_review_format =    "id: {0} | {1} - {2} | '{3}'\n"
class MovieView:
    
    #################################################### Movies
    def print_movies(self, movie_name, movies):
        result = "Found movies that is similar to search string \"{0}\"\n\n".format(movie_name)
        for movie in movies:
            result += movie_format.format(movie[0], movie[1], movie[2], "")
        return result

    def print_get_interested_movies(self, movies):
        result = "Found movies that you might get interested based on your prior ratings:\n"
        for movie in movies:
            if movie[0] != movies[0][0]:
                result += movie_format.format(movie[0], movie[1].pop(0), movie[2], self.array_to_string(movie[1]))
        return result

    def print_get_similar_movies_by_genre(self, movie_id, movies):
        mov = movies.pop(0)
        result = "Found movies of similar genre to id: {0} | {1} - {2}:\n{3}\n".format(mov[0], mov[1].pop(0), mov[2], self.array_to_string(mov[1]))
        for movie in movies:
            result += movie_format.format(movie[0], movie[1].pop(0), movie[2], self.array_to_string(movie[1]))
        return result
    
    #################################################### Rating
    def print_delete_movie_rating(self, movies):
        result = "Deleted rating of movie: \n"
        result += movie_format.format(movies[0], movies[1].pop(0), movies[2], self.array_to_string(movies[1]))
        return result

    def print_get_rated_movies(self, movies):
        result = "Found movies that you have rated: \n"
        for movie in movies:
            result += "id: {0} | {1} - {2} | Rating: {3}\n".format(movie[0], movie[1].pop(0), movie[2], movie[3])
            result += "{0}\n".format(self.array_to_string(movie[1]))
        return result
    

    def print_set_movie_rating(self, movies):
        result = "Rated movie: \n"
        result += "id: {0} | {1} - {2} | Rating: {3}\n".format(movies[0], movies[1].pop(0), movies[2], movies[3])
        result += "{0}".format(self.array_to_string(movies[1]))
        return result
    
    #################################################### Review
    def print_list_reviews(self, reviews):
        result = "List of reviewed movies\n"
        for review in reviews:
            result += list_review_format.format(str(review[0]),review[1],str(review[2]),review[3])
        return result
    
    def print_review(self, review):
        return review_format.format(str(review[0]), review[1].pop(0), str(review[2]),
                                    self.array_to_string(review[1]), review[4], review[5], review[3])

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

        welcome += '\n3. List all the movies that you might interested in (Precise)'
        welcome += '\n4. List all the movies that you might interested in (Quick)'
        welcome += '\n5. List all the movies that you have rated' 
        welcome += '\n6. Rate a movie or update an existing rating '
        welcome += '\n7. Delete your rating for a movie'
        
        welcome += '\n8. List all movies that you reviewed'
        welcome += '\n9. Read a review'
        welcome += '\n10. Create or Update a review for a movie'
        welcome += '\n11. Delete your review for a movie'
        
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
            res = res.rstrip(" | a.k.a. ")
            return res + "\n"
        return ""

    def print_error(self, message):
        return "Error: " + message