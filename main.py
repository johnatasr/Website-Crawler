from app.worker import ScraperExecutor
import argparse

if __name__ == '__main__':
    websites = ["https://www.illion.com.au", "https://www.phosagro.com/contacts", "https://www.cialdnb.com"]

    parser = argparse.ArgumentParser(description='Crawl websites and extract logo URL and phone numbers')
    parser.add_argument('input_file', type=str, help='Path to input file')
    # parser.add_argument('output_file', type=str, help='Path to output file')
    args = parser.parse_args()

    executor = ScraperExecutor(urls_list=websites)



