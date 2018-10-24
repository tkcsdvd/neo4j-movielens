from flask import Flask, jsonify, request
from py2neo import Graph, Node, NodeMatcher
import connexion

app = Flask(__name__)

USERNAME = "neo4j"
PASS = "neo4j" #default

graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))

####### Movie #######

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

####### Top #######

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

####### User #######

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

# Collaborative Filtering
@app.route('/api/rec_engine/collab/<userid>/<n>')

def getRecCollab(userid,n):
    rec = graph.run('MATCH (u1:User {id:{userid}})-[r:RATED]->(m:Movie) '
                    'WITH u1, avg(r.rating) AS u1_mean '
                    'MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2) '
                    'WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) '
                    'WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings '
                    'UNWIND ratings AS r '
                    'WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom, '
                    'sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom, u1, u2 WHERE denom <> 0 '
                    'WITH u1, u2, nom/denom AS pearson '
                    'ORDER BY pearson DESC LIMIT 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) ) '
                    'RETURN m.title AS title, SUM( pearson * r.rating) AS score '
                    'ORDER BY score DESC LIMIT toInt({n});', userid=userid, n=n)

    return jsonify(rec.data())

if __name__ == '__main__':

    # Create the application instance
    app = connexion.App(__name__, specification_dir='swagger/')

    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yml')

    app.run(port=5000, host='0.0.0.0', debug=True)