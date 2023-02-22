import asyncio
import json
import logging
import re
from http.client import HTTPException
from pprint import pprint
from typing import List, Union
from uuid import uuid4

import aiohttp
from bs4 import BeautifulSoup

from app.domain import ScrapedWebsite

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class CrawlerExecutor(object):
    """
    Class that represents an executor for scraping multiple websites asynchronously.

    Attributes:
        urls_list (List[str]): A list of URLs to scrape.
        executor_id (uuid): An unique identifier for each executor instance.
    """

    def __init__(self, urls_list: List[str]):
        """
        Constructor method for CrawlerExecutor.

        Args:
            urls_list (List[str]): A list of URLs to scrape.
        """
        self.urls_list = urls_list
        self.executor_id = uuid4()

    async def execute(self) -> None:
        """
        Crawl a list of websites asynchronously and export the results to a JSON file.
        """
        async with aiohttp.ClientSession() as session:
            pprint("Starting process...")
            tasks = []
            for url in self.urls_list:
                tasks.append(asyncio.ensure_future(self._process_website(url, session)))
            results = await asyncio.gather(*tasks)
        pprint(results)
        self._export_to_json(results)

    async def _process_website(
        self, url: str, session: aiohttp.ClientSession
    ) -> Union[dict, None]:
        """
        Process a single website asynchronously.

        Args:
          url (str): The URL of the website to scrape.
          session (aiohttp.ClientSession): An instance of aiohttp.ClientSession.

        Returns:
          Union[dict, None]: A dictionary containing the scraped data or None if an error occurred.
        """
        try:
            async with session.get(
                url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
            ) as response:
                response.raise_for_status()
                content: str = await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError, HTTPException):
            logger.error(f"Request Error crawling website: {url}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error crawling website: {url} exp {e}")
            return {}

        soup = BeautifulSoup(content, "html.parser")

        scraped_obj = ScrapedWebsite(
            website=url,
            logo=soup.find_all("img", {"class": re.compile(r".*logo.*")}),
            phones=soup.find_all("a", href=re.compile(r"tel:")),
        )
        return scraped_obj.as_a_dict()

    def _export_to_json(self, data: List[dict]) -> None:
        """
        Export the data to a JSON file.

        Args:
            data (List[dict]): A list of dictionaries containing the scraped data.
        """
        with open(f"exports/scraper_data_{self.executor_id}.json", "w") as f:
            pprint("Exporting file ...")
            pprint("Please take a look at exports path to see all exported files")
            json.dump(data, f)
