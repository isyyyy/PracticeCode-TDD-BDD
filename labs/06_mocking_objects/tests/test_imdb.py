"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

IMDB_DATA = {}


class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """ Load imdb responses needed by tests """
        global IMDB_DATA
        with open('tests/fixtures/imdb_responses.json') as json_data:
            IMDB_DATA = json.load(json_data)

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    @patch('test_imdb.IMDb.search_titles')
    def test_search_by_title(self, imdb_mock):
        """Test search by title"""
        imdb_mock.return_value = IMDB_DATA['GOOD_SEARCH']
        imdb = IMDb('k_12345678')
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["title"], "Babmi")
        self.assertEqual(results["results"][0]["id"], "tt1375666")

    # Mock 404
    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, imdb_mock):
        """Test search with no results"""
        imdb_mock.return_value = Mock(status_code=404)
        imdb = IMDb('k_12345678')
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results, {})

    # Mock: 200, INVALID_API
    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, imdb_mock):
        """Test search by title failed"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA['INVALID_API'])
        )
        imdb = IMDb('bad_key')
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["errorMessage"], "Invalid API Key")

    # Mock: 200, GOOD_RATING
    @patch('models.imdb.requests.get')
    def test_movie_search_ratings(self, imdb_mock):
        """Test movie ratings"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA['GOOD_RATING'])
        )
        imdb = IMDb('k_12345678')
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["filmAffinity"], 3)
        self.assertEqual(results["rottenTomatoes"], 5)

    # Mock: 200, GOOD_REVIEW
    @patch('models.imdb.requests.get')
    def test_movie_review(self, imdb_mock):
        """Test movie reviews"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA['GOOD_REVIEW'])
        )
        imdb = IMDb('k_12345678')
        results = imdb.movie_reviews("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["year"],'1942')

    @patch('models.imdb.requests.get')
    def test_movie_review_invalid(self, imdb_mock):
        """Test movie reviews"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=404,
            json=Mock(return_value=IMDB_DATA['MOVIE_INVALID'])
        )
        imdb = IMDb('k_12345678')
        results = imdb.movie_reviews("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results, {})

    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, imdb_mock):
        """Test movie ratings"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA['GOOD_RATING'])
        )
        imdb = IMDb('k_12345678')
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)


    @patch('models.imdb.requests.get')
    def test_movie_ratings_invalid(self, imdb_mock):
        """Test movie ratings"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=404,
            json=Mock(return_value=IMDB_DATA['MOVIE_INVALID'])
        )
        imdb = IMDb('k_12345678')
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results, {})
