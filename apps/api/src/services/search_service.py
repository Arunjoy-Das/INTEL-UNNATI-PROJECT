import requests
from bs4 import BeautifulSoup
import time

class SearchTools:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def web_search(self, query):
        """
        Performs a Deep Search using DuckDuckGo (no API key needed for demo)
        """
        print(f"[SEARCHING] Deep scan for: {query}")
        try:
            # Using DuckDuckGo HTML version for easier scraping
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                 return []

            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # Extract top 3 result snippets
            for result in soup.find_all("div", class_="result")[:3]:
                title = result.find("a", class_="result__a")
                snippet = result.find("a", class_="result__snippet")
                
                if title and snippet:
                     results.append({
                         "text": snippet.get_text().strip(),
                         "source": title.get_text().strip(),
                         "url": title['href']
                     })
            
            return results
        except Exception as e:
            print(f"[SEARCH ERROR] {e}")
            return []

search_tool = SearchTools()

def get_search_tool():
    return search_tool
