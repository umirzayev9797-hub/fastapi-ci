import asyncio
import aiohttp
from pathlib import Path

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
SAVE_DIR = Path("cats")
SAVE_DIR.mkdir(exist_ok=True)

# Ограничиваем конкурентность
semaphore = asyncio.Semaphore(10)


async def fetch_cat_url(session):
    async with semaphore:
        for _ in range(5):  # retry до 5 раз
            async with session.get(CAT_API_URL) as r:

                if r.status == 429:
                    await asyncio.sleep(1)
                    continue

                r.raise_for_status()
                data = await r.json()
                return data[0]["url"]

        raise RuntimeError("Rate limit exceeded too many times")


async def download_image(session, url):
    async with semaphore:
        async with session.get(url) as r:
            r.raise_for_status()
            return await r.read()


def save_sync(path, data):
    with open(path, "wb") as f:
        f.write(data)


async def save_file(path, data):
    await asyncio.to_thread(save_sync, path, data)


async def download_one(session, i):
    try:
        url = await fetch_cat_url(session)
        img = await download_image(session, url)
        await save_file(SAVE_DIR / f"async_cat_{i}.jpg", img)

    except Exception as e:
        print(f"Error {i}: {e}")


async def run(count):
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [download_one(session, i) for i in range(count)]
        await asyncio.gather(*tasks)


def run_async(count):
    asyncio.run(run(count))
