import requests
from bs4 import BeautifulSoup
import re

class SearchTools:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

    def web_search(self, query):
        """
        Multi-Source Knowledge Retrieval: DDG -> Wikipedia
        Returns a list of {'text': ..., 'source': ..., 'url': ...}
        """
        print(f"[SEARCH] Querying: {query}")
        results = []

        # --- 1. DUCKDUCKGO HTML ---
        try:
            resp = requests.get(
                f"https://html.duckduckgo.com/html/?q={query}",
                headers=self.headers, timeout=10
            )
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for div in soup.find_all("div", class_="result")[:5]:
                    t = div.find("a", class_="result__a")
                    s = div.find("a", class_="result__snippet")
                    if t and s:
                        results.append({
                            "text": s.get_text().strip(),
                            "source": t.get_text().strip(),
                            "url": t.get('href', '')
                        })
        except Exception as e:
            print(f"[DDG ERROR] {e}")

        if results:
            return results

        # --- 2. WIKIPEDIA FAILOVER ---
        print("[FALLBACK] Using Wikipedia Knowledge API...")
        try:
            api = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&srlimit=5&format=json"
            data = requests.get(api, headers=self.headers, timeout=10).json()
            if "query" in data and data["query"]["search"]:
                for item in data["query"]["search"][:5]:
                    title = item['title']
                    snippet = BeautifulSoup(item['snippet'], "html.parser").get_text()
                    results.append({
                        "text": snippet,
                        "source": f"Wikipedia: {title}",
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
        except Exception as e:
            print(f"[WIKI ERROR] {e}")

        return results

    def wikipedia_summary(self, topic):
        """
        Get the first paragraph summary of a Wikipedia page.
        Used for deep fact extraction.
        """
        try:
            api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            data = requests.get(api, headers=self.headers, timeout=8).json()
            return data.get("extract", "")
        except:
            return ""

search_tool = SearchTools()

def get_search_tool():
    return search_tool
