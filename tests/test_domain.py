import unittest
from unittest.mock import MagicMock, patch
from app.domain import ScrapedWebsite


class TestScrapedWebsite(unittest.TestCase):

    def setUp(self):
        self.url = "https://example.com/logo.png"
        self.logo_mock = MagicMock(attrs={"src": self.url}, src=self.url, return_value=[MagicMock(attrs={"src": self.url}, src=self.url)()])

    def test_get_url_logo(self):
        mock_logo = [{'src': 'http://www.example.com/img/logo.png'}]
        with patch('app.domain.ScrapedWebsite._get_url_logo', MagicMock(return_value='http://www.example.com/img/logo.png')):
            self.assertEqual(ScrapedWebsite._get_url_logo(mock_logo, 'http://www.example.com'), 'http://www.example.com/img/logo.png')

    def test_as_a_dict(self):
        expected_dict = {'website': 'https://www.example.com', 'logo': '', 'phones': ['1234567890', '(123) 456', '1234 5678']}
        website = ScrapedWebsite(
            website='https://www.example.com',
            logo=self.logo_mock(),
            phones=[{'href': 'tel:1234567890'}, {'href': 'tel:(123) 456-7890'}, {'href': 'tel:1234 5678'}]
        )
        self.assertEqual(website.as_a_dict(), expected_dict)
