import csv
from py2neo import Graph, Node

N_MOVIES = 1000
N_RATINGS = 1000
N_TAGS = 1000
N_LINKS = 1000

USERNAME = "neo4j"
PASS = "123456" #default

graph = Graph("bolt://jaja:7687", auth = (USERNAME, PASS))


def main():

    createGenreNodes()

    print("Step 1 out of 4: loading movie nodes")
    loadMovies()

    print("Step 2 out of 4: loading rating relationships")
    loadRatings()

    print("Step 3 out of 4: loading tag relationships")
    loadTags()

    print("Step 4 out of 4: updating links to movie nodes")
    loadLinks()

def createGenreNodes():
    allGenres = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
                 "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
                 "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    for genre in allGenres:
        gen = Node("Genre", name=genre)
        graph.create(gen)


def loadMovies():
    with open('data/movies.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        for i, row in enumerate(readCSV):

            createMovieNodes(row)
            createGenreMovieRelationships(row)

            if (i % 100 == 0):
                print(f"{i}/{N_MOVIES} Movie nodes created")

            # break after N_MOVIES movies

            if i >= N_MOVIES:
                break

def createMovieNodes(row):
    movieData = parseRowMovie(row)
    id = movieData[0]
    title = movieData[1]
    year = movieData[2]
    mov = Node("Movie", id=id, title=title, year=year)
    graph.create(mov)

def parseRowMovie(row):
        id = row[0]
        year = row[1][-5:-1]
        title = row[1][:-7]

        return (id, title, year)


def createGenreMovieRelationships(row):
    movieId = row[0]
    movieGenres = row[2].split("|")

    for movieGenre in movieGenres:
        graph.run('MATCH (g:Genre {name: {genre}}), (m:Movie {id: {movieId}}) CREATE (g)-[:IS_GENRE_OF]->(m)',
            genre=movieGenre, movieId=movieId)

def parseRowGenreMovieRelationships(row):
    movieId = row[0]
    movieGenres = row[2].split("|")

    return (movieId, movieGenres)

def loadRatings():
    with open('data/ratings.csv') as csvfile:
         readCSV = csv.reader(csvfile, delimiter=',')
         next(readCSV, None) #skip header
         for i,row in enumerate(readCSV):
             createUserNodes(row)
             createRatingRelationship(row)

             if (i % 100 == 0):
                 print(f"{i}/{N_RATINGS} Rating relationships created")

             if (i >= N_RATINGS):
                 break

def createUserNodes(row):
    user = Node("User", id="User " + row[0])
    graph.merge(user, "User", "id")

def createRatingRelationship(row):
    ratingData = parseRowRatingRelationships(row)

    graph.run(
        'MATCH (u:User {id: {userId}}), (m:Movie {id: {movieId}}) CREATE (u)-[:RATED { rating: {rating}, timestamp: {timestamp} }]->(m)',
        userId=ratingData[0], movieId=ratingData[1], rating=ratingData[2], timestamp=ratingData[3])

def parseRowRatingRelationships(row):
    userId = "User " + row[0]
    movieId = row[1]
    rating = float(row[2])
    timestamp = row[3]

    return (userId, movieId, rating, timestamp)

def loadTags():
    with open('data/tags.csv') as csvfile:
         readCSV = csv.reader(csvfile, delimiter=',')
         next(readCSV, None) #skip header
         for i,row in enumerate(readCSV):
             createTagRelationship(row)

             if (i % 100 == 0):
                 print(f"{i}/{N_TAGS} Tag relationships created")

             if (i >= N_TAGS):
                 break

def createTagRelationship(row):
    tagData = parseRowTagRelationships(row)

    graph.run(
        'MATCH (u:User {id: {userId}}), (m:Movie {id: {movieId}}) CREATE (u)-[:TAGGED { tag: {tag}, timestamp: {timestamp} }]->(m)',
        userId=tagData[0], movieId=tagData[1], tag=tagData[2], timestamp=tagData[3])

def parseRowTagRelationships(row):
    userId = "User " + row[0]
    movieId = row[1]
    tag = row[2]
    timestamp = row[3]

    return (userId, movieId, tag, timestamp)

def loadLinks():
    with open('data/links.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        for i, row in enumerate(readCSV):

            updateMovieNodeWithLinks(row)

            if (i % 100 == 0):
                print(f"{i}/{N_LINKS} Movie nodes updated with links")

            # break after N_LINKS movies

            if i >= N_LINKS:
                break

def updateMovieNodeWithLinks(row):
    linkData = parseRowLinks(row)

    graph.run(
        'MATCH (m:Movie {id: {movieId}}) SET m += { imdbId: {imdbId} , tmdbId: {tmdbId} }',
        movieId=linkData[0], imdbId=linkData[1], tmdbId=linkData[2])

def parseRowLinks(row):
    movieId = row[0]
    imdbId = row[1]
    tmdbId = row[2]

    return (movieId, imdbId, tmdbId)


if __name__ == '__main__':
    main()