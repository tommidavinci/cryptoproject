from neo4j.v1 import GraphDatabase
from database.config import config

class neo4jDB(object):

    def __init__(self):
        params = config('database/database.ini', 'neo4j')
        self._driver = GraphDatabase.driver(params['uri'], auth=(params['user'], params['password']))

    def close(self):
        self._driver.close()

    #def test(self):
    #    with self._driver.session() as session:
    #        rating = session.write_transaction(self._find_rating_of_movie_by_user, )

    def test(self):
        with self._driver.session() as session:
            test = session.read_transaction(self._test)
            return test
    @staticmethod
    def _test(tx):
        return tx.run("MATCH (m:Movie {id:1}) RETURN m.id").single()[0]
    
    def get_movies_rated_by_user(self, userId):
        with self._driver.session() as session:
            rating = session.read_transaction(self._get_movies_rated_by_user, userId)
            return rating
    @staticmethod
    def _get_movies_rated_by_user(tx, userId):
        result = tx.run("MATCH (u:User {id:$userId})-[r:RATED]->(m:Movie) "
                        "RETURN r.rating, m.id", userId=userId)
        return result

    def set_movie_rating(self, userId, movieId, rating):
        with self._driver.session() as session:
            rating = session.write_transaction(self._set_movie_rating, userId, movieId, rating)
            return rating
    @staticmethod
    def _set_movie_rating(tx, userId, movieId, rating):
        result = tx.run("MERGE (:User {id:$userId})-[r:RATED]->(m:Movie {id:$movieId}) " + 
                        "ON CREATE SET r.rating = $rating ON MATCH SET r.rating = $rating " + 
                        "RETURN m, r", userId=userId, movieId=movieId, rating=rating)
        return result

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