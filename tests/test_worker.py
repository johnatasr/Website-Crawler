import unittest
from unittest.mock import Mock, patch

from app.worker import CrawlerExecutor


class TestCrawlerExecutor(unittest.TestCase):
    def setUp(self):
        self.urls = [
            "https://www.google.com",
            "https://www.apple.com",
            "https://www.microsoft.com",
        ]
        self.executor = CrawlerExecutor(self.urls)

    @patch("worker.aiohttp.ClientSession.get")
    async def test__process_website(self, mock_get):
        mock_response = Mock()
        mock_response.text.return_value = "<html><body><h1>Test</h1></body></html>"
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await self.executor._process_website(self.urls[0], Mock())
        self.assertIsInstance(result, dict)
        self.assertEqual(result["website"], self.urls[0])

    @patch("worker.aiohttp.ClientSession.get")
    async def test__process_website_error(self, mock_get):
        mock_get.side_effect = Exception("Test error")
        result = await self.executor._process_website(self.urls[0], Mock())
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    @patch("worker.aiohttp.ClientSession.get")
    async def test__process_website_timeout_error(self, mock_get):
        mock_get.side_effect = asyncio.TimeoutError()
        result = await self.executor._process_website(self.urls[0], Mock())
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    @patch("worker.aiohttp.ClientSession.get")
    async def test__process_website_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await self.executor._process_website(self.urls[0], Mock())
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test__export_to_json(self):
        data = [{"website": "https://www.google.com", "logo": [], "phones": []}]
        with patch("builtins.open", create=True) as mock_open:
            self.executor._export_to_json(data)
            mock_open.assert_called_with(
                f"exports/scraper_data_{self.executor.executor_id}.json", "w"
            )
            mock_open.return_value.__enter__.return_value.write.assert_called()
