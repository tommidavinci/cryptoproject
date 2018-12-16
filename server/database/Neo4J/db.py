from neo4j.v1 import GraphDatabase

class neo4jDB(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_rating(self, movieId, userId):
        with self._driver.session() as session:
            rating = session.write_transaction(self._find_rating_of_movie_by_user, userId, movieId)
            print(rating)
    
    @staticmethod
    def _find_rating_of_movie_by_user(tx, userId, movieId):
        result = tx.run("MATCH (u:User {id:userId})-[r:RATED]->(m:Movie {id:movieId}) "
                        "RETURN u.id, r.rating, m.id")
        return result.single()[0]

    """def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]"""