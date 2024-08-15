import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time

class WebCrawler:
    def __init__(self, root_url, max_pages=100, delay=1):
        self.root_url = root_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.to_visit = [root_url]
        self.domain = urlparse(root_url).netloc
        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(urljoin(root_url, "/robots.txt"))
        self.robot_parser.read()

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return (
            parsed_url.netloc == self.domain
            and self.robot_parser.can_fetch("*", url)
        )

    def crawl(self):
        page_count = 0
        while self.to_visit and page_count < self.max_pages:
            url = self.to_visit.pop(0)
            if url not in self.visited_urls and self.is_valid_url(url):
                try:
                    page_content = self.fetch_page(url)
                    self.visited_urls.add(url)
                    page_count += 1
                    
                    # Process the page content
                    links, text = self.process_page(url, page_content)
                    
                    # Add new links to the to_visit list
                    self.to_visit.extend(link for link in links if link not in self.visited_urls)
                    
                    # Yield the processed page information
                    yield {
                        'url': url,
                        'text': text,
                        'links': links
                    }
                    
                    # Respect the crawl delay
                    time.sleep(self.delay)
                except Exception as e:
                    print(f"Error crawling {url}: {str(e)}")

    def fetch_page(self, url):
        response = requests.get(url, headers={'User-Agent': 'SiteBot Crawler'})
        response.raise_for_status()
        return response.text

    def process_page(self, url, content):
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract links
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            if self.is_valid_url(link):
                links.append(link)
        
        # Extract text content
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        
        return links, text

    def get_sitemap(self):
        return list(self.visited_urls)