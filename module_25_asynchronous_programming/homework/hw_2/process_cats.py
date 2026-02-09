import requests
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
SAVE_DIR = Path("cats")
SAVE_DIR.mkdir(exist_ok=True)


def get_cat_url():
    for _ in range(5):
        r = requests.get(CAT_API_URL, timeout=10)

        if r.status_code == 429:
            time.sleep(1)
            continue

        r.raise_for_status()
        return r.json()[0]["url"]

    raise RuntimeError("Rate limit exceeded")


def download_one(i):
    try:
        url = get_cat_url()

        img = requests.get(url, timeout=10).content

        with open(SAVE_DIR / f"proc_cat_{i}.jpg", "wb") as f:
            f.write(img)

    except Exception as e:
        print(f"Proc error {i}: {e}")


def run_processes(count):
    with ProcessPoolExecutor(max_workers=6) as ex:
        list(ex.map(download_one, range(count)))
