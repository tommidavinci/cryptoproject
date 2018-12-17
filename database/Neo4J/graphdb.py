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
        return tx.run("""
            MATCH (m:Movie {id:1}) RETURN m.id""").single()[0]
    
    def get_movies_rated_by_user(self, userId):
        with self._driver.session() as session:
            rating = session.read_transaction(self._get_movies_rated_by_user, userId)
            return rating
    @staticmethod
    def _get_movies_rated_by_user(tx, userId):
        result = tx.run("""
            MATCH (u:User {id:$userId})-[r:RATED]->(m:Movie) 
            RETURN r.rating, m.id""", userId=userId)
        return result
    
    def delete_movie_rating(self, userId, movieId):
        with self._driver.session() as session:
            rating = session.write_transaction(self._delete_movie_rating, userId, movieId)
            return rating
    @staticmethod
    def _delete_movie_rating(tx, userId, movieId):
        tx.run("""
            MATCH (:User{id:$userId})-[r:RATED]->(:Movie{id:$movieId})
            DELETE r""", userId=userId, movieId=movieId)
        return ""
    
    def get_movies_from_users_not_rated_by_x(self, userId, resultset):
        userArr = []
        for record in resultset:
            userArr.append(record['to'])
        with self._driver.session() as session:
            result = session.read_transaction(self._get_movies_from_users_not_rated_by_x, userId, userArr)
            return result
    @staticmethod
    def _get_movies_from_users_not_rated_by_x(tx, userId, userArr):
        result = tx.run("""
            MATCH (u:User)-[r:RATED]->(m:Movie)
                WHERE u.id IN $userArr AND r.rating >= 4.5 AND NOT (:User {id:$userId})-[:RATED]->(m)
            RETURN m.id""", userId=userId, userArr=userArr)
        return result
    
    def get_precise_similar_users(self, userId):
        with self._driver.session() as session:
            result = session.read_transaction(self._get_precise_interested_movies, userId)
            return result
    @staticmethod
    def _get_precise_interested_movies(tx, userId):
        result = tx.run("""
            MATCH (u:User {id:$userId})-->(m:Movie)
            WITH u, collect(DISTINCT m.id) as movieIds, toFloat(count(DISTINCT m)) AS movies
            MATCH (u)-[a:RATED]->(m:Movie)<-[b:RATED]-(xu:User) WHERE a.rating > 4 AND b.rating = a.rating
            WITH u, collect(DISTINCT xu.id) + u.id as userIds, movies, movieIds
            MATCH (m:Movie), (x:User) 
                WHERE x.id IN userIds AND m.id IN movieIds AND (size((u)-->(:Movie)<--(x)) > (movies / 10) * 8 OR x.id = 1)
            OPTIONAL MATCH (x)-[r:RATED]->(m)
            WITH x, {item:x.id, weights: collect(coalesce(r.rating,0))} AS userData
            WITH collect(userData) AS data
            CALL algo.similarity.cosine.stream(data)
            YIELD item1, item2, count1, count2, similarity WHERE item1 = $userId OR item2 = $userId
            RETURN item2 AS to, similarity
            ORDER BY similarity DESC LIMIT 10""", userId=userId)
        return result

    def set_movie_rating(self, userId, movieId, rating):
        with self._driver.session() as session:
            rating = session.write_transaction(self._set_movie_rating, userId, movieId, rating)
            return rating
    @staticmethod
    def _set_movie_rating(tx, userId, movieId, rating):
        result = tx.run("""
            MATCH (u:User {id:$userId}), (m:Movie {id:$movieId})
            MERGE (u)-[r:RATED]-(m)
            ON CREATE SET r.rating = $rating ON MATCH SET r.rating = $rating 
            RETURN m.id, r.rating""", userId=userId, movieId=movieId, rating=rating)
        return result


    # Movie & User CRUD
    def create_user(self, userId):
        with self._driver.session() as session:
            result = session.write_transaction(self._create_user, userId)
            return result
    @staticmethod
    def _create_user(tx, userId):
        result = tx.run("""
            CREATE (u:User {id:$userId})
            RETURN u""", userId=userId)
        return result

    def create_movie(self, movieId):
        with self._driver.session() as session:
            result = session.write_transaction(self._create_movie, movieId)
            return result
    @staticmethod
    def _create_movie(tx, movieId):
        result = tx.run("""
            CREATE (m:Movie {id:$movieId})
            RETURN m""", movieId=movieId)
        return result

    def delete_user(self, userId):
        with self._driver.session() as session:
            result = session.write_transaction(self._delete_user, userId)
            return result
    @staticmethod
    def _delete_user(tx, userId):
        result = tx.run("""
            MATCH (u:User {id:$userId})
            DELETE u""", userId=userId)
        return result
    
    def delete_movie(self, movieId):
        with self._driver.session() as session:
            result = session.write_transaction(self._delete_movie, movieId)
            return result
    @staticmethod
    def _delete_movie(tx, movieId):
        result = tx.run("""
            MATCH (m:Movie {id:$movieId})
            DELETE m""", movieId=movieId)
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