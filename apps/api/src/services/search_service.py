import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
import time


class SearchTools:
    """
    Multi-Source News & Fact-Check Scraper
    
    When DuckDuckGo blocks us (Render cloud IP), we don't just fall back 
    to Wikipedia snippets. We DIRECTLY scrape major authoritative sources:
    
    1. DuckDuckGo HTML (first attempt)
    2. Google News RSS Feed (free, no API key)
    3. Reuters search
    4. BBC News search
    5. Snopes fact-check search
    6. AP News search
    7. Wikipedia search API (always works)
    8. Wikipedia Summary API (deep context)
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    # ================================================================
    #  INDIVIDUAL SOURCE SCRAPERS
    # ================================================================

    def _search_duckduckgo(self, query: str) -> list:
        """DuckDuckGo HTML search (often blocked on cloud IPs)."""
        results = []
        try:
            resp = requests.get(
                f"https://html.duckduckgo.com/html/?q={quote_plus(query)}",
                headers=self.headers, timeout=12, verify=False
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
            if results:
                print(f"  [DDG] Found {len(results)} results")
        except Exception as e:
            print(f"  [DDG] Blocked or error: {e}")
        return results

    def _search_google_news_rss(self, query: str) -> list:
        """Google News RSS feed — free, no API key, usually not blocked."""
        results = []
        try:
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
            resp = requests.get(url, headers=self.headers, timeout=12, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "xml")
                for item in soup.find_all("item")[:5]:
                    title = item.find("title")
                    desc = item.find("description")
                    link = item.find("link")
                    source = item.find("source")
                    if title:
                        text = desc.get_text().strip() if desc else title.get_text().strip()
                        # Clean HTML from description
                        text = BeautifulSoup(text, "html.parser").get_text()
                        results.append({
                            "text": text[:500],
                            "source": f"Google News: {source.get_text() if source else 'News'}",
                            "url": link.get_text().strip() if link else ""
                        })
                if results:
                    print(f"  [GOOGLE NEWS] Found {len(results)} articles")
        except Exception as e:
            print(f"  [GOOGLE NEWS] Error: {e}")
        return results

    def _search_reuters(self, query: str) -> list:
        """Reuters search — one of the most trusted news sources."""
        results = []
        try:
            url = f"https://www.reuters.com/site-search/?query={quote_plus(query)}&offset=0"
            resp = requests.get(url, headers={
                **self.headers,
                "Referer": "https://www.reuters.com/"
            }, timeout=12, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Reuters uses data-testid for search results
                for article in soup.find_all("li", limit=5):
                    headline = article.find("h3") or article.find("a")
                    snippet = article.find("p")
                    link = article.find("a", href=True)
                    if headline and snippet:
                        href = link['href'] if link else ""
                        if not href.startswith("http"):
                            href = f"https://www.reuters.com{href}"
                        results.append({
                            "text": snippet.get_text().strip()[:400],
                            "source": f"Reuters: {headline.get_text().strip()[:100]}",
                            "url": href
                        })
                if results:
                    print(f"  [REUTERS] Found {len(results)} articles")
        except Exception as e:
            print(f"  [REUTERS] Error: {e}")
        return results

    def _search_bbc(self, query: str) -> list:
        """BBC News search — globally trusted, reliable endpoint."""
        results = []
        try:
            url = f"https://www.bbc.co.uk/search?q={quote_plus(query)}"
            resp = requests.get(url, headers=self.headers, timeout=12, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # BBC search results
                for item in soup.find_all("li", class_=re.compile(r"ssrcss"), limit=5):
                    title_el = item.find("span") or item.find("a")
                    desc_el = item.find("p")
                    link_el = item.find("a", href=True)
                    if title_el and desc_el:
                        results.append({
                            "text": desc_el.get_text().strip()[:400],
                            "source": f"BBC News: {title_el.get_text().strip()[:100]}",
                            "url": link_el['href'] if link_el else ""
                        })
                if results:
                    print(f"  [BBC] Found {len(results)} articles")
        except Exception as e:
            print(f"  [BBC] Error: {e}")
        return results

    def _search_snopes(self, query: str) -> list:
        """Snopes — the internet's premier fact-checking site."""
        results = []
        try:
            url = f"https://www.snopes.com/?s={quote_plus(query)}"
            resp = requests.get(url, headers=self.headers, timeout=12, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for article in soup.find_all("article", limit=5):
                    title_el = article.find("h3") or article.find("a")
                    desc_el = article.find("p")
                    link_el = article.find("a", href=True)
                    if title_el:
                        text = desc_el.get_text().strip() if desc_el else title_el.get_text().strip()
                        results.append({
                            "text": text[:400],
                            "source": f"Snopes: {title_el.get_text().strip()[:100]}",
                            "url": link_el['href'] if link_el else ""
                        })
                if results:
                    print(f"  [SNOPES] Found {len(results)} fact-checks")
        except Exception as e:
            print(f"  [SNOPES] Error: {e}")
        return results

    def _search_wikipedia_api(self, query: str) -> list:
        """Wikipedia Search API — always available, most reliable."""
        results = []
        try:
            api = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(query)}&srlimit=5&format=json"
            data = requests.get(api, headers=self.headers, timeout=12, verify=False).json()
            if "query" in data and data["query"]["search"]:
                for item in data["query"]["search"][:5]:
                    title = item['title']
                    snippet = BeautifulSoup(item['snippet'], "html.parser").get_text()
                    results.append({
                        "text": snippet,
                        "source": f"Wikipedia: {title}",
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
                print(f"  [WIKIPEDIA] Found {len(results)} results")
        except Exception as e:
            print(f"  [WIKIPEDIA] Error: {e}")
        return results

    # ================================================================
    #  MAIN SEARCH (MULTI-SOURCE AGGREGATOR)
    # ================================================================

    def web_search(self, query: str) -> list:
        """
        Multi-source search aggregator.
        Tries multiple sources in parallel-ish fashion and merges results.
        Returns the best evidence from across all sources.
        """
        print(f"[SEARCH] Querying: {query}")
        all_results = []
        seen_texts = set()

        # --- TIER 1: Fast primary sources ---
        ddg = self._search_duckduckgo(query)
        if ddg:
            all_results.extend(ddg)

        # --- TIER 2: News aggregators (work even when DDG is blocked) ---
        gnews = self._search_google_news_rss(query)
        all_results.extend(gnews)

        # --- TIER 3: Direct news site scraping ---
        # Only scrape if we don't have enough results yet
        if len(all_results) < 3:
            reuters = self._search_reuters(query)
            all_results.extend(reuters)

        if len(all_results) < 3:
            bbc = self._search_bbc(query)
            all_results.extend(bbc)

        # --- TIER 4: Fact-check sites (especially useful for "fact check" queries) ---
        if "fact" in query.lower() or "true" in query.lower() or "false" in query.lower():
            snopes = self._search_snopes(query)
            all_results.extend(snopes)

        # --- TIER 5: Wikipedia (always works, guaranteed fallback) ---
        if len(all_results) < 3:
            wiki = self._search_wikipedia_api(query)
            all_results.extend(wiki)

        # Deduplicate by text content
        unique_results = []
        for r in all_results:
            text_key = r["text"][:80].lower()
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                unique_results.append(r)

        print(f"[SEARCH] Total unique results: {len(unique_results)}")
        return unique_results[:8]

    # ================================================================
    #  INDIVIDUAL ARTICLE SCRAPER
    # ================================================================

    def scrape_article(self, url: str) -> str:
        """
        Scrape the full text of a news article from its URL.
        Used for deep verification when we need more context.
        """
        try:
            resp = requests.get(url, headers=self.headers, timeout=15, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                
                # Remove scripts, styles, nav, footer
                for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()

                # Extract main article content
                article = soup.find("article") or soup.find("main") or soup.find("body")
                if article:
                    paragraphs = article.find_all("p")
                    text = " ".join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30)
                    return text[:2000]  # Cap at 2000 chars
        except Exception as e:
            print(f"  [SCRAPE] Error scraping {url}: {e}")
        return ""

    # ================================================================
    #  WIKIPEDIA DEEP SUMMARY
    # ================================================================

    def wikipedia_summary(self, topic: str) -> str:
        """Get the first paragraph summary of a Wikipedia page."""
        try:
            api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            data = requests.get(api, headers=self.headers, timeout=12, verify=False).json()
            return data.get("extract", "")
        except:
            return ""


search_tool = SearchTools()

def get_search_tool():
    return search_tool
