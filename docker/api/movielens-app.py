from flask import Flask, jsonify, request
from py2neo import Graph, Node, NodeMatcher, Database
import connexion
import os
import time

app = Flask(__name__)

# wait for Neo4j in Docker
# time.sleep(15)

# NEO4J_HOST will be provided by Docker, otherwise localhost

HOST = os.environ.get("NEO4J_HOST", "localhost")
PORT = 7687
USER = "neo4j"
PASS = "neo4j" #default

graph = Graph("bolt://" + HOST + ":7687", auth=(USER, PASS))

# Get the available deatils of a given movie
@app.route('/api/movie/details/<title>')
def getMovieData(title):
    matcher = NodeMatcher(graph)
    movie = matcher.match("Movie", title={title}).first()

    return jsonify(movie)

# Get the genres associated with a given movie
@app.route('/api/movie/genres/<title>')
def getMovieGenres(title):
    genres = graph.run('MATCH (genres)-[:IS_GENRE_OF]->(m:Movie {title: {title}}) RETURN genres', title=title)

    return jsonify(list(genres))

# Get the submitted ratings of a given movie
@app.route('/api/movie/ratings/<title>')
def getMovieRatings(title):
    ratings = graph.run('MATCH (u: User)-[r:RATED]->(m:Movie {title: {title}}) RETURN u.id AS user, r.rating AS rating', title=title)

    return jsonify(ratings.data())

# Get the submitted tags of a given movie
@app.route('/api/movie/tags/<title>')
def getMovieTags(title):
    tags = graph.run('MATCH (u: User)-[t:TAGGED]->(m:Movie {title: {title}}) RETURN u.id AS user, t.tag AS tag', title=title)

    return jsonify(tags.data())


# Get list of movies from a given year
@app.route('/api/movie/year/<year>')
def getMoviesByYear(year):
    movies = graph.run('MATCH (m:Movie) where m.year = {year} RETURN m.title AS title, m.year AS year', year=year)

    return jsonify(movies.data())

# Get the average rating for a given movie
@app.route('/api/movie/average-rating/<title>')
def getMovieAverageRating(title):
    avg = graph.run('MATCH (u: User)-[r:RATED]->(m:Movie {title: {title}}) RETURN m.title AS title, avg(toFloat(r.rating)) AS averageRating', title=title)

    return jsonify(avg.data())

# Get top N highest rated movies
@app.route('/api/top/movie/top-n/<n>')
def getMovieTopN(n):
    mvs = graph.run('MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, avg(r.rating) AS averageRating order by averageRating desc limit toInt({n})', n=n)

    return mvs.data()

# Get top N most rated movies
@app.route('/api/top/movie/n-most-rated/<n>')
def getMovieNMostRated(n):
    mvs = graph.run('MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, count(r.rating) as NumberOfRatings order by NumberOfRatings desc limit toInt({n})', n=n)

    return mvs.data()




# Get the submitted ratings by a given user
@app.route('/api/user/ratings/<userId>')
def getUserRatings(userId):
    ratings = graph.run('MATCH (u:User {id: {userId}})-[r:RATED ]->(movies) RETURN movies.title AS movie, r.rating AS rating', userId=userId)

    return jsonify(ratings.data())

# Get the submitted tags by a given user
@app.route('/api/user/tags/<userId>')
def getUserTags(userId):
    tags = graph.run('MATCH (u:User {id: {userId}})-[t:TAGGED ]->(movies) RETURN movies.title AS title, t.tag AS tag', userId=userId)

    return jsonify(tags.data())

# Get the average rating by a given user
@app.route('/api/user/average-rating/<userId>')
def getUserAverageRating(userId):
    avg = graph.run('MATCH (u: User {id: {userId}})-[r:RATED]->(m:Movie) RETURN u.id AS user, avg(toFloat(r.rating)) AS averageRating', userId=userId)

    return jsonify(avg.data())


##### Recommender Enginer

# Content based
@app.route('/api/rec_engine/content/<title>/<n>')

def getRecContent(title,n):
    avg = graph.run('MATCH (m:Movie)<-[:IS_GENRE_OF]-(g:Genre)-[:IS_GENRE_OF]->(rec:Movie) '
                    'WHERE m.title = {title} '
                    'WITH rec, COLLECT(g.name) AS genres, COUNT(*) AS numberOfSharedGenres '
                    'RETURN rec.title as title, genres, numberOfSharedGenres '
                    'ORDER BY numberOfSharedGenres DESC LIMIT toInt({n});', title=title, n=n)

    return jsonify(avg.data())

if __name__ == '__main__':

    # Create the application instance
    app = connexion.App(__name__, specification_dir='swagger/')

    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yml')

    app.run(port=5001, host='0.0.0.0', debug=True)