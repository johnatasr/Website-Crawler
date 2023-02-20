import requests
from bs4 import BeautifulSoup
import concurrent.futures
from typing import List
import json
import re
from app.domain import ScrapedWebsite
from uuid import uuid4


class ScraperExecutor(object):

    def __init__(self, urls_list: List, input_file):
        self.data = []
        self.urls_list = urls_list
        self.regex_pattern = re.compile(r'^\+?\d{1,3}[\s\d-()]*\d{3}[\s-]?\d{4}$')
        self.failure_file = {}
        self.executor_id = uuid4()

    def process_website(self, website):
        # Send a request to the website
        response = requests.get(website)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the logo image tag and get the source URL
        logo_url = soup.find('img', {'class': 'logo'})['src']

        # Find all phone numbers in the website content
        phone_numbers = []
        for element in soup.find_all('p'):
            if "phone" in element.text.lower():
                phone_numbers.append(element.text)

        # Return the logo URL and phone numbers for the website
        return website, logo_url, phone_numbers

    def execute(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit each website to the executor and store the future object in a list
            future_to_website = {executor.submit(self.process_website, website): website for website in self.urls_list}

            # Iterate over the completed futures as they complete
            for future in concurrent.futures.as_completed(future_to_website):
                website = future_to_website[future]
                try:
                    # Get the result of the future and print it
                    result = future.result()
                    scraped_obj = ScrapedWebsite(
                        website=result[0], logo=result[1], phones=result[2], regex_pattern=self.regex_pattern
                    )
                    self.data.append(scraped_obj.as_a_dict())
                    print("Website: ", result[0])
                    print("Logo URL: ", result[1])
                    print("Phone numbers: ", result[2])
                except Exception as exc:
                    print("%r generated an exception: %s" % (website, exc))

    def export_to_json(self):
        with open(f"../exports/scraper_data_{self.executor_id}.json", "w") as f:
            # Write the JSON data to the file
            json.dump(self.data, f)

    def _export_failure(self, exception):
        with open(f"../exports/scraper_exceptions_{self.executor_id}.json", "w") as f:
            self.failure_file.update({"name_exp": str(exception)})
            json.dump(self.failure_file, f)

    def _get_input_file(self, input_file):
        with open(input_file, 'r') as f:
            self.urls_list = f.read().splitlines()
