from app.worker import CrawlerExecutor
import asyncio
import sys

if __name__ == '__main__':
    crawler = CrawlerExecutor(urls_list=[line.strip() for line in sys.stdin])
    asyncio.run(crawler.execute())

