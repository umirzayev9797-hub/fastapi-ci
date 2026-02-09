import asyncio
import aiohttp
from pathlib import Path


CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
SAVE_DIR = Path("cats")
SAVE_DIR.mkdir(exist_ok=True)


async def fetch_cat_url(session: aiohttp.ClientSession) -> str:
    """Получаем ссылку на случайную картинку кота"""
    async with session.get(CAT_API_URL) as resp:
        data = await resp.json()
        return data[0]["url"]


async def download_image(session: aiohttp.ClientSession, url: str) -> bytes:
    """Скачиваем картинку"""
    async with session.get(url) as resp:
        return await resp.read()


def save_file_sync(filename: Path, data: bytes):
    """
    Синхронная запись файла (обычный open).
    Будет вызвана в отдельном потоке.
    """
    with open(filename, "wb") as f:
        f.write(data)


async def save_file(filename: Path, data: bytes):
    """
    Асинхронная обёртка над open.
    Переносим блокирующую операцию в поток.
    """
    await asyncio.to_thread(save_file_sync, filename, data)


async def download_one_cat(session: aiohttp.ClientSession, idx: int):
    """Полный цикл: получить ссылку → скачать → сохранить"""
    try:
        cat_url = await fetch_cat_url(session)
        image_bytes = await download_image(session, cat_url)

        filename = SAVE_DIR / f"cat_{idx}.jpg"
        await save_file(filename, image_bytes)

        print(f"✅ Сохранён {filename}")

    except Exception as e:
        print(f"❌ Ошибка при загрузке кота {idx}: {e}")


async def main():
    count = 5  # сколько котов качаем

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_one_cat(session, i)
            for i in range(1, count + 1)
        ]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
