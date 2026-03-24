import requests
from bs4 import BeautifulSoup
import time
import random

class SearchTools:
    def __init__(self):
        # Using a very stable User-Agent for Wikipedia/DDG
        self.headers = {
            "User-Agent": "FactGuard-Verification-Bot/1.0 (Contact: arunjoy.das.official@gmail.com; Research Project)"
        }

    def web_search(self, query):
        """
        Hyper-Resilient Knowledge Retrieval: DDG -> Wikipedia -> Google-Snippet
        Optimized for Scientific and Geopolitical Fact-Checking.
        """
        print(f"[SEARCHING] universal scan: {query}")
        results = []
        
        # --- 1. DUCKDUCKGO ENHANCED ---
        try:
            # We use the HTML version with a direct query
            resp = requests.get(f"https://html.duckduckgo.com/html/?q={query}", headers=self.headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for div in soup.find_all("div", class_="result")[:3]:
                    t, s = div.find("a", class_="result__a"), div.find("a", class_="result__snippet")
                    if t and s:
                         results.append({"text": s.get_text().strip(), "source": t.get_text().strip(), "url": t['href']})
        except: pass

        if results: return results

        # --- 2. WIKIPEDIA REST API (The Ultimate Failover for Cloud IPs) ---
        print("[FALLBACK] Switching to Global Knowledge Graph (Wikipedia)...")
        try:
            # We search and then get a summary directly
            search_api = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
            wiki_search = requests.get(search_api, headers=self.headers, timeout=10).json()
            if "query" in wiki_search and wiki_search["query"]["search"]:
                for item in wiki_search["query"]["search"][:3]:
                    title = item['title']
                    # Get the actual snippet and strip HTML
                    snip = BeautifulSoup(item['snippet'], "html.parser").get_text()
                    results.append({
                        "text": f"OFFICIAL DATA: {snip}...",
                        "source": f"Wikipedia: {title}",
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
        except: pass

        return results

search_tool = SearchTools()

def get_verification_service():
    from src.services.verification_service import service
    return service
