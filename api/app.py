from flask import Flask, jsonify, request
from py2neo import Graph, Node, NodeMatcher

app = Flask(__name__)

@app.route('/api/movie/<title>')
def getMovieData(title):
    movie = matcher.match("Movie", title={title}).first()

    return jsonify(movie)

@app.route('/api/genres/<title>')
def getMovieGenres(title):
    genres = graph.run('MATCH (genres)-[:IS_GENRE_OF]->(m:Movie {title: {title}}) RETURN genres', title=title)

    return jsonify(list(genres))


@app.route('/api/user/ratings/<userId>')
def getUserRatings(userId):
    ratedMovies = graph.run('MATCH (u:User {id: {userId}})-[:RATED ]->(movies) RETURN movies', userId=userId)

    return jsonify(ratedMovies.data())


if __name__ == '__main__':

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    matcher = NodeMatcher(graph)

    app.run(port=5000, host='0.0.0.0', debug=True)