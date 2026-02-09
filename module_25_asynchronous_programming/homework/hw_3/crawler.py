import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class AsyncCrawler:
    def __init__(
        self,
        max_depth: int = 3,
        concurrency: int = 10,
        output_file: str = "links.txt",
    ):
        self.max_depth = max_depth
        self.visited: set[str] = set()
        self.found_links: set[str] = set()

        self.sem = asyncio.Semaphore(concurrency)
        self.output_file = output_file

    # ----------- utils -----------

    def is_external(self, base: str, link: str) -> bool:
        """Проверка: ссылка внешняя или нет"""
        base_domain = urlparse(base).netloc
        link_domain = urlparse(link).netloc

        return link_domain and link_domain != base_domain

    def normalize(self, base: str, link: str) -> str:
        """Относительная → абсолютная"""
        return urljoin(base, link)

    # ----------- network -----------

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str | None:
        try:
            async with self.sem:
                async with session.get(url, timeout=10) as r:
                    if "text/html" not in r.headers.get("Content-Type", ""):
                        return None
                    return await r.text()
        except Exception:
            return None

    # ----------- parsing -----------

    def extract_links(self, base: str, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")

        links = []

        for a in soup.find_all("a", href=True):
            href = a["href"]

            abs_link = self.normalize(base, href)

            if self.is_external(base, abs_link):
                links.append(abs_link)

        return links

    # ----------- crawling -----------

    async def crawl(
        self,
        session: aiohttp.ClientSession,
        url: str,
        depth: int,
    ):
        if depth > self.max_depth:
            return

        if url in self.visited:
            return

        self.visited.add(url)

        html = await self.fetch(session, url)
        if not html:
            return

        links = self.extract_links(url, html)

        for link in links:
            if link not in self.found_links:
                self.found_links.add(link)

        tasks = [
            self.crawl(session, link, depth + 1)
            for link in links
        ]

        await asyncio.gather(*tasks)

    # ----------- save -----------

    def save(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            for link in sorted(self.found_links):
                f.write(link + "\n")

    # ----------- entrypoint -----------

    async def run(self, start_urls: list[str]):
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [
                self.crawl(session, url, 1)
                for url in start_urls
            ]

            await asyncio.gather(*tasks)

        self.save()
