import unittest
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of websites to crawl
websites = ["https://www.example1.com", "https://www.example2.com", "https://www.example3.com"]

class TestWebCrawler(unittest.TestCase):
    def test_logo_url(self):
        for website in websites:
            # Send a request to the website
            response = requests.get(website)

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the logo image tag and get the source URL
            logo_url = soup.find('img', {'class': 'logo'})['src']

            # Assert that the logo URL is not None
            self.assertIsNotNone(logo_url)

    def test_phone_numbers(self):
        for website in websites:
            # Send a request to the website
            response = requests.get(website)

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all phone numbers in the website content
            phone_numbers = []
            for element in soup.find_all('p'):
                if "phone" in element.text.lower():
                    phone_numbers.append(element.text)

            # Assert that at least one phone number was found
            self.assertGreater(len(phone_numbers), 0)

    def test_concurrency(self):
        def process_website(website):
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

        # Use a ThreadPoolExecutor to process the URLs concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit each website to the executor and store the future object in a list
            future_to_website = {executor.submit(process_website, website): website for website in websites}

            # Iterate over the completed futures as they complete
            for future in concurrent.futures.as_completed(future_to_website):
                website = future_to_website[future]
                try:
                    # Get the result of the future
                    result = future.result()
                    logo_url = result[1]
                    phone_numbers = result[2]

                    # Assert that the logo URL is not None
                    self.assertIsNotNone(logo_url)

                    # Assert that at least one phone number was found
                    self.assertGreater(len(phone_numbers), 0)
                except Exception as exc:
                    self.fail("Website %s generated an exception: %s" % (website, exc))

if __name__ == '__main__':
    unittest.main()