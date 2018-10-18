import csv
from py2neo import Graph, Node, Relationship


graph = Graph("bolt://localhost:7687", auth = ("neo4j", "123456"))

