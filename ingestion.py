import csv
from py2neo import Graph, Node, Relationship


graph = Graph("bolt://localhost:7687", auth = ("neo4j", "123456"))

# import movies

def parseMovies():
    with open('data/movies.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        for i, row in enumerate(readCSV):
            id = row[0]
            year = row[1][-5:-1]
            title = row[1][:-6]
            mov = Node("Movie", id=id, title=title, year=year)
            graph.create(mov)
            parseGenres(row)
            if (i % 100 == 0):
                print(str(i) + "/1000 loaded")
            if (i >= 10000):
                break

def createGenres():

    allGenres = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    for genre in allGenres:
        gen = Node("Genre", name=genre)
        graph.create(gen)

def parseGenres(row):

    # create relationships
    movieId = row[0]
    movieGenres = row[2].split("|")

    for movieGenre in movieGenres:
        graph.run('MATCH (g:Genre {name: {genre}}), (m:Movie {id: {movieId}}) CREATE (g)-[:IS_GENRE_OF]->(m)',
            genre=movieGenre, movieId=movieId)

#createGenres()
#parseMovies()


# import ratings

def parseRatings():
    with open('data/ratings.csv') as csvfile:
         readCSV = csv.reader(csvfile, delimiter=',')
         next(readCSV, None) #skip header
         for i,row in enumerate(readCSV):
             if(i % 100 == 0):
                 print(i)
             user= Node("User", id= row[0])
             graph.merge(user, "User","id")
             graph.run('MATCH (u:User {id: {userId}}), (m:Movie {id: {movieId}}) CREATE (u)-[:RATED { rating: {rating}, timestamp: {timestamp} }]->(m)',
                       userId = row[0],movieId = row[1],rating = row[2],timestamp =row[3])
             if (i >= 10000):
                 break

parseRatings()