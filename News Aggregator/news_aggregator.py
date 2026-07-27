import os
import requests
import xml.etree.ElementTree as ET

class NewsAggregator:
    """Class to fetch and parse live RSS feeds from major publishers."""

    # Dictionary of free public RSS feed URLs
    FEEDS = {
        "1": ("World News (BBC)", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        "2": ("Technology (TechCrunch)", "https://techcrunch.com/feed/"),
        "3": ("Science (ScienceDaily)", "https://www.sciencedaily.com/rss/top/science.xml")
    }

    def fetch_headlines(self, url):
        """Downloads the RSS XML payload and extracts headline titles and links."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonNewsApp/1.0"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            # Parse the XML string using Python's ElementTree library
            root = ET.fromstring(response.content)
            
            headlines = []
            # In RSS standards, articles are nested inside <channel> -> <item>
            for item in root.findall(".//item")[:7]:  # Fetch top 7 headlines
                title = item.find("title").text if item.find("title") is not None else "No Title"
                link = item.find("link").text if item.find("link") is not None else "No Link"
                headlines.append({"title": title, "link": link})
                
            return headlines

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch news feed: {e}")
            return []
        except ET.ParseError:
            print("❌ Failed to parse the RSS XML structure.")
            return []

    def display_news(self, category_name, headlines):
        """Formats and prints the headlines to the terminal."""
        print("\n" + "=" * 60)
        print(f" TOP HEADLINES: {category_name.upper()}")
        print("=" * 60)

        if not headlines:
            print("No headlines found at this time.")
            return

        for index, article in enumerate(headlines, start=1):
            print(f"\n{index}. {article['title']}")
            print(f"    Link: {article['link']}")
            
        print("\n" + "=" * 60)


def main():
    aggregator = NewsAggregator()

    while True:
        print("\n=== 📡 LIVE NEWS AGGREGATOR ===")
        print("Choose a category to fetch current news:")
        
        for key, (name, _) in aggregator.FEEDS.items():
            print(f"{key}. {name}")
            
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice in aggregator.FEEDS:
            category_name, feed_url = aggregator.FEEDS[choice]
            print(f"\n📡 Connecting to feed for '{category_name}'...")
            
            headlines = aggregator.fetch_headlines(feed_url)
            aggregator.display_news(category_name, headlines)

        elif choice == "4":
            print("Closing News Aggregator. Have a productive day!")
            break
        else:
            print("Invalid choice! Please select a valid option.")


if __name__ == "__main__":
    main()