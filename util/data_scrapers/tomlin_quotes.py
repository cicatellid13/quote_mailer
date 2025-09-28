from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_quotes():
    # Configure Chrome options
    chrome_options = Options()
    # Removed headless mode for debugging
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")

    all_quotes = []

    with webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    ) as driver:
        try:
            url = "https://www.brainyquote.com/authors/mike-tomlin-quotes"
            print(f"Accessing URL: {url}")
            driver.get(url)
            print(f"Page title: {driver.title}")

            # Wait for the content to load
            wait = WebDriverWait(driver, 10)

            # Try multiple selectors to find quotes
            selectors = [
                "div.grid-item.qb",  # Main quote container
                "span.text",  # Quote text span
                ".clearfix.quote",  # Alternative quote container
            ]

            page_num = 1
            while True:
                print(f"Scraping page {page_num}")

                # Try each selector until we find quotes
                quotes_found = False
                for selector in selectors:
                    try:
                        quotes_elements = wait.until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, selector)
                            )
                        )
                        if quotes_elements:
                            quotes_found = True
                            print(f"Found quotes using selector: {selector}")
                            break
                    except TimeoutException:
                        continue

                if not quotes_found:
                    print("No quotes found with any selector")
                    break

                # Add quotes from current page
                page_quotes = []
                for q in quotes_elements:
                    try:
                        # Try to get text directly or from nested elements
                        quote_text = q.text.strip()
                        if not quote_text:
                            # Try finding nested text element
                            text_element = q.find_element(
                                By.CSS_SELECTOR, "span.text, a.b-qt"
                            )
                            quote_text = text_element.text.strip()

                        if quote_text:
                            print(
                                f"Found quote: {quote_text[:50]}..."
                            )  # Print first 50 chars
                            page_quotes.append(quote_text)
                    except Exception as e:
                        print(f"Error extracting quote: {str(e)}")
                        continue

                print(f"Found {len(page_quotes)} quotes on page {page_num}")
                all_quotes.extend(page_quotes)

                try:
                    # Look for next button with multiple possible selectors
                    next_button = None
                    for next_selector in [
                        'a.page-link[title="next"]',
                        ".next-page",
                        "li.next a",
                    ]:
                        try:
                            next_button = wait.until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, next_selector)
                                )
                            )
                            if next_button:
                                break
                        except:
                            continue

                    if not next_button:
                        print("No next button found")
                        break

                    next_button.click()
                    time.sleep(3)  # Increased wait time
                    page_num += 1
                except Exception as e:
                    print(f"Navigation error: {str(e)}")
                    break

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        print(f"Total quotes collected: {len(all_quotes)}")

        return dict(author="Mike Tomlin", quotes=all_quotes)
