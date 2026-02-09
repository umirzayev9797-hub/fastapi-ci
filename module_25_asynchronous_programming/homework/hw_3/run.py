import asyncio
from crawler import AsyncCrawler


START_URLS = [
    "https://example.com",
]

crawler = AsyncCrawler(
    max_depth=3,
    concurrency=10,
    output_file="links.txt",
)

asyncio.run(crawler.run(START_URLS))

print("Готово. Ссылки записаны в links.txt")
