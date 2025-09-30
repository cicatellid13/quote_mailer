from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_quotes_by_author(author: str, delay=1) -> dict[str, list[str]]:
    new_author = author.replace(" ", "-").strip()
    all_quotes = []
    page = 1
    base_url = f"https://www.brainyquote.com/authors/{new_author}-quotes"

    while True:
        # Construct paginated URL
        url = base_url if page == 1 else f"{base_url}_{page}"
        print(f"Scraping page {page}: {url}")

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )

        try:
            driver.get(url)
            time.sleep(delay)

            # Check if redirected to first page
            current_url = driver.current_url
            if page > 1 and current_url.rstrip("/") == base_url:
                print(
                    f"Page {page} does not exist (redirected to first page). Stopping."
                )
                driver.quit()
                break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            quotes = [
                q.text.strip() for q in soup.select("a.b-qt") if q.text.strip()
            ]

            if not quotes:
                print(f"No quotes found on page {page}, stopping.")
                driver.quit()
                break

            print(f"Found {len(quotes)} quotes on page {page}")
            all_quotes.extend(quotes)

        finally:
            driver.quit()  # close Chrome

        page += 1
        time.sleep(delay)  # polite delay

    return {
        "author": author,
        "quotes": all_quotes,
    }
