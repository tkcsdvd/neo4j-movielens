import unittest

from ingestion import parseRowMovie, parseRowGenreMovieRelationships, parseRowRatingRelationships, parseRowTagRelationships

class ParserTests(unittest.TestCase):

    def test_parse_row_movie(self):

        row = "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy".split(",")
        self.assertEquals (parseRowMovie(row), ("1", "Toy Story", "1995"))

    def test_parse_row_genre_movie_relationship(self):

        row = "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy".split(",")
        self.assertEquals (parseRowGenreMovieRelationships(row), ('1', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']))

    def test_parse_row_rating_relationship(self):

        row = "1,29,3.5,1112484676".split(",")
        self.assertEquals (parseRowRatingRelationships(row), ("User 1", "29", "3.5", "1112484676"))

    def test_parse_row_tag_relationship(self):

        row = "65,1617,neo-noir,1368150217".split(",")
        self.assertEquals (parseRowTagRelationships(row), ("User 65", "1617", "neo-noir", "1368150217"))