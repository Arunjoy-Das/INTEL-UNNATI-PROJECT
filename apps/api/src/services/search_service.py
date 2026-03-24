import requests
from bs4 import BeautifulSoup
import time
import random

class SearchTools:
    def __init__(self):
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
        ]

    def web_search(self, query):
        """
        Production-Grade Search: DDG Failover -> Wikipedia REST API
        Wikipedia is the #1 source for world-leader, scientific, and historical facts 
        and is highly resilient to cloud-IP blocking.
        """
        print(f"[SEARCHING] Neural scan for: {query}")
        results = []
        
        # --- PHASE 1: DUCKDUCKGO SCRAMBLE (Standard Search) ---
        try:
            session = requests.Session()
            headers = {"User-Agent": random.choice(self.ua_list)}
            # Standard DDG HTML
            resp = session.get(f"https://html.duckduckgo.com/html/?q={query}", headers=headers, timeout=8)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                divs = soup.find_all("div", class_="result")
                for div in divs[:3]:
                    t = div.find("a", class_="result__a")
                    s = div.find("a", class_="result__snippet")
                    if t and s:
                        results.append({"text": s.get_text().strip(), "source": t.get_text().strip(), "url": t['href']})
        except: pass

        if results: return results

        # --- PHASE 2: WIKIPEDIA FAILOVER (High-Reliability for Cloud IPs) ---
        # If DDG is blocked on Render, we use Wikipedia's official REST API 
        print("[FALLBACK] Initializing Wikipedia Knowledge Retrieval...")
        try:
            # Search for the most relevant page titles
            search_api = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json&origin=*"
            wiki_res = requests.get(search_api, timeout=8).json()
            
            if "query" in wiki_res and wiki_res["query"]["search"]:
                for item in wiki_res["query"]["search"][:3]:
                    title = item['title']
                    snippet = BeautifulSoup(item['snippet'], "html.parser").get_text()
                    results.append({
                        "text": f"Wikipedia Report: {snippet}...",
                        "source": f"Wikipedia: {title}",
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
        except Exception as e:
            print(f"[WIKI ERROR] {e}")

        return results

search_tool = SearchTools()

def get_search_tool():
    return search_tool
