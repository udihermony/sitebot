import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sitebot.crawlers.web_crawler import WebCrawler

def test_web_crawler():
    # Use a small, stable website for testing
    test_url = "https://github.com/udihermony/sitebot/tree/main"
    crawler = WebCrawler(test_url, max_pages=5)
    
    print(f"Starting crawl of {test_url}")
    for page_info in crawler.crawl():
        print(f"Crawled: {page_info['url']}")
        print(f"  Links found: {len(page_info['links'])}")
        print(f"  Text length: {len(page_info['text'])} characters")
        print("----")
    
    print("\nCrawl completed.")
    print(f"Total pages crawled: {len(crawler.get_sitemap())}")
    print("Sitemap:")
    for url in crawler.get_sitemap():
        print(f"  {url}")

if __name__ == "__main__":
    test_web_crawler()