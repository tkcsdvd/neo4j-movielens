from flask import Flask, jsonify, request
from py2neo import Graph, Node, NodeMatcher
import connexion

app = Flask(__name__)

@app.route('/api/movie/details/<title>')
def getMovieData(title):

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    matcher = NodeMatcher(graph)
    movie = matcher.match("Movie", title={title}).first()

    return jsonify(movie)

@app.route('/api/movie/genres/<title>')
def getMovieGenres(title):

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    genres = graph.run('MATCH (genres)-[:IS_GENRE_OF]->(m:Movie {title: {title}}) RETURN genres', title=title)

    return jsonify(list(genres))


@app.route('/api/user/ratings/<userId>')
def getUserRatings(userId):

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    ratedMovies = graph.run('MATCH (u:User {id: {userId}})-[:RATED ]->(movies) RETURN movies', userId=userId)

    return jsonify(ratedMovies.data())


if __name__ == '__main__':


    # Create the application instance
    app = connexion.App(__name__, specification_dir='swagger/')

    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yml')

    app.run(port=5000, host='0.0.0.0', debug=True)