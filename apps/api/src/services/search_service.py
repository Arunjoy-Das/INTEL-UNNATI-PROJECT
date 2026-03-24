import requests
from bs4 import BeautifulSoup
import time
import random

class SearchTools:
    def __init__(self):
        # Rotating User-Agents to prevent Cloud blocking (Chrome 122/123)
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]

    def web_search(self, query):
        """
        Resilient "Deep Search" - Uses DDG Lite to bypass cloud throttlers
        """
        print(f"[SEARCHING] Deep scan (Lite) for: {query}")
        try:
            # Shift to DuckDuckGo LITE - Better for server-side scraping
            # Lite version is pure HTML, very robust against cloud-IP detection
            search_url = f"https://duckduckgo.com/lite/?q={query}"
            
            headers = {"User-Agent": random.choice(self.ua_list)}
            response = requests.get(search_url, headers=headers, timeout=12)
            
            if response.status_code != 200:
                 print(f"[SEARCH BLOCKED] Code: {response.status_code}")
                 return []

            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # DDG Lite uses a table-based layout
            # <tr> for each result
            rows = soup.find_all("tr")
            
            # The pattern in DDG Lite:
            # row 1: result title/link
            # row 2: result snippet
            # We iterate and combine
            for i in range(0, len(rows) - 1, 3):
                title_row = rows[i]
                snippet_row = rows[i+1]
                
                title_link = title_row.find("a", class_="result-link")
                snippet_text = snippet_row.find("td", class_="result-snippet")
                
                if title_link and snippet_text:
                     results.append({
                         "text": snippet_text.get_text().strip(),
                         "source": title_link.get_text().strip(),
                         "url": title_link['href']
                     })
                
                if len(results) >= 3:
                     break
            
            return results
        except Exception as e:
            print(f"[SEARCH ERROR] {e}")
            return []

search_tool = SearchTools()

def get_search_tool():
    return search_tool
