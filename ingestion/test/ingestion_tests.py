import unittest

from ingestion.ingestion import parseRowMovie, parseRowGenreMovieRelationships, parseRowRatingRelationships, parseRowTagRelationships, parseRowLinks

class ParserTests(unittest.TestCase):

    # test the parsing of movies
    def test_parse_row_movie(self):

        row = "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy".split(",")
        self.assertEquals (parseRowMovie(row), ("1", "Toy Story", "1995"))

    # test the parsing of genre-movie relationships
    def test_parse_row_genre_movie_relationship(self):

        row = "1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy".split(",")
        self.assertEquals (parseRowGenreMovieRelationships(row), ('1', ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy']))

    # test the parsing of rating relationships
    def test_parse_row_rating_relationship(self):

        row = "1,29,3.5,1112484676".split(",")
        self.assertEquals (parseRowRatingRelationships(row), ("User 1", "29", 3.5, "1112484676"))

    # test the parsing of tag relationships
    def test_parse_row_tag_relationship(self):

        row = "65,1617,neo-noir,1368150217".split(",")
        self.assertEquals (parseRowTagRelationships(row), ("User 65", "1617", "neo-noir", "1368150217"))

    # test the parsing of links
    def test_parse_row_links(self):

        row = "5,0113041,11862".split(",")
        self.assertEquals (parseRowLinks(row), ("5","0113041", "11862"))