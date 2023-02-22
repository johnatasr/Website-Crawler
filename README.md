# Website Crawler

A Python-based website crawler that scrapes data from a list of websites in a text file and exports the scraped data to a JSON file. The crawler uses asyncio to enable concurrent scraping of websites.

## Installation and Usage

To perform this process, you will need to have Docker installed. Please use the link below to download and install Docker:

https://docs.docker.com/engine/install/

To build an image and run it with the list of URLs in a text file, execute the following commands: 

```commandline
docker build --tag websitesscraper .
```

```commandline
cat websites.txt | docker run -i -v $(pwd)/exports:/app/exports websitesscraper:latest
```

The return will be in console and inside path exports as a json file.

## Documentation
### CrawlerExecutor

The CrawlerExecutor class is responsible for executing the crawling process. It takes a list of website URLs as input, and exposes a single method, execute, to start the crawling process. The scraped data is exported to a JSON file using the _export_to_json method.

### Methods
#### execute()

Crawl a list of websites asynchronously.

#### _process_website(url: str, session)

Process a single website URL. This method is called asynchronously by the execute method for each website URL in the input list. The method returns a dictionary containing the scraped data for the website, or None if an error occurred during scraping.

#### _export_to_json(data)

Export the scraped data to a JSON file.

### ScrapedWebsite

The ScrapedWebsite class represents the scraped data for a single website. It takes the website URL, a list of logo images, and a list of phone number links as input.

### Attributes
_website: str_

The URL of the scraped website.

_logo: Any_

A logo url found on the website.

_phones: Any_

A list of phone number links found on the website.

### Methods

#### as_a_dict() -> Dict

Convert the ScrapedWebsite object to a dictionary.

#### _sanitize_phone_numbers() -> List

Extract and sanitize phone numbers from the phones attribute.

#### _get_url_logo(logos, url) -> str

Extract the URL of the website's logo image.

## License

This project is licensed under the MIT License. See the LICENSE file for more information