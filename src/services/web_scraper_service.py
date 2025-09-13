import requests
from bs4 import BeautifulSoup


class WebScraperService:
    """
    A reusable service class for fetching and parsing web content.
    """
    def __init__(self, parser='html.parser'):
        """Initializes the service with a specific HTML parser."""
        self.parser = parser
        self.session = requests.Session()

    def get_html(self, url: str) -> str:
        """Fetches the raw HTML content from a URL."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    def parse_text(self, html_content: str) -> str:
        """Parses HTML content and extracts the plain text."""
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, self.parser)
        return soup.get_text(separator='\n', strip=True)

    def scrape_plain_text(self, url: str) -> str:
        """Fetches a URL and returns the plain text content."""
        html_content = self.get_html(url)
        return self.parse_text(html_content)


# The following code runs only if you execute web_scraper.py directly
# So that this file can be imported into other Python files without
# triggering the execution of this block of code.
if __name__ == '__main__':
    scraper = WebScraperService()
    url_to_scrape = 'https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models'
    
    # Use the combined method
    text_content = scraper.scrape_plain_text(url_to_scrape)
    if text_content:
        print("--- Plain text content ---")
        print(text_content)
