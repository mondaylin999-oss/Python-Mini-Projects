import csv
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# --- PATH LOCKING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "scraped_books.csv")


class BookScraper:
    """Scrapes book titles, prices, and stock status from a practice catalog site."""

    URL = "https://books.toscrape.com/"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonScraper/1.0"
        }

    def fetch_html(self):
        """Downloads raw HTML from the target page."""
        try:
            response = requests.get(self.URL, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error while fetching page: {e}")
            return None

    def parse_books(self, html):
        """Uses BeautifulSoup to locate book cards and extract fields."""
        soup = BeautifulSoup(html, "html.parser")
        book_cards = soup.select("article.product_pod")

        books = []
        scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for card in book_cards:
            title_tag = card.select_one("h3 a")
            price_tag = card.select_one("p.price_color")
            stock_tag = card.select_one("p.instock.availability")

            # 'title' attribute holds the full book title (h3 text can be truncated)
            title = title_tag["title"].strip() if title_tag and title_tag.has_attr("title") else "Unknown"
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            stock = stock_tag.get_text(strip=True) if stock_tag else "Unknown"

            books.append({
                "title": title,
                "price": price,
                "stock": stock,
                "scraped_at": scraped_at
            })

        return books

    def save_to_csv(self, books):
        """Appends scraped records to a CSV file."""
        file_exists = os.path.exists(CSV_FILE)

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "price", "stock", "scraped_at"])
            if not file_exists:
                writer.writeheader()
            writer.writerows(books)

        print(f"💾 Saved {len(books)} books to {CSV_FILE}")


def main():
    print("=== 🕷️ PYTHON WEB SCRAPER: BOOK CATALOG ===")
    scraper = BookScraper()

    print("📡 Fetching webpage...")
    html = scraper.fetch_html()
    if not html:
        return

    print("🔍 Parsing HTML elements...")
    books = scraper.parse_books(html)

    print(f"\n--- TOP {min(5, len(books))} EXTRACTED BOOKS ---")
    for idx, book in enumerate(books[:5], start=1):
        print(f"{idx}. {book['title']} | {book['price']} | {book['stock']}")

    scraper.save_to_csv(books)


if __name__ == "__main__":
    main()