import csv
from py2neo import Graph, Node, Relationship


graph = Graph("bolt://localhost:7687", auth = ("neo4j", "123456"))

# import movies

def parseMovies():
    with open('movies.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        for row in readCSV:
            id = row[0]
            year = row[1][-5:-1]
            title = row[1][:-6]
            mov = Node("Movie", id=id, title=title, year=year)
            graph.create(mov)
