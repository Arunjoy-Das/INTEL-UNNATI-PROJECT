import requests
from bs4 import BeautifulSoup
import time
import random

class SearchTools:
    def __init__(self):
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        ]

    def web_search(self, query):
        """
        Hyper-Resilient Search - Using DDG Lite with session-mimicry
        """
        print(f"[SEARCHING] Universal deep scan for: {query}")
        try:
            # Using a Session to maintain cookies/headers consistency
            session = requests.Session()
            headers = {
                "User-Agent": random.choice(self.ua_list),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://duckduckgo.com/",
                "Connection": "keep-alive"
            }
            
            # Use the "HTML" version which is sometimes less restricted than Lite for cloud IPs
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            
            # Adding a tiny delay to simulate human timing
            time.sleep(random.uniform(0.5, 1.2))
            
            response = session.get(search_url, headers=headers, timeout=12)
            
            if response.status_code != 200:
                 print(f"[SEARCH BLOCKED] Code: {response.status_code}")
                 return []

            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # The HTML version uses "result" divs
            divs = soup.find_all("div", class_="result")
            for div in divs[:3]:
                title_tag = div.find("a", class_="result__a")
                snippet_tag = div.find("a", class_="result__snippet")
                
                if title_tag and snippet_tag:
                     results.append({
                         "text": snippet_tag.get_text().strip(),
                         "source": title_tag.get_text().strip(),
                         "url": title_tag['href']
                     })
                     
            # FALLBACK to Lite if HTML version fails to find divs
            if not results:
                print("[FALLBACK] Trying Lite endpoint...")
                lite_response = session.get(f"https://duckduckgo.com/lite/?q={query}", headers=headers)
                lite_soup = BeautifulSoup(lite_response.text, "html.parser")
                rows = lite_soup.find_all("tr")
                for i in range(0, len(rows) - 1, 3):
                    title_link = rows[i].find("a", class_="result-link")
                    snippet_td = rows[i+1].find("td", class_="result-snippet")
                    if title_link and snippet_td:
                         results.append({
                             "text": snippet_td.get_text().strip(),
                             "source": title_link.get_text().strip(),
                             "url": title_link['href']
                         })
                    if len(results) >= 3: break
            
            return results
        except Exception as e:
            print(f"[SEARCH ERROR] {e}")
            return []

search_tool = SearchTools()

def get_search_tool():
    return search_tool
