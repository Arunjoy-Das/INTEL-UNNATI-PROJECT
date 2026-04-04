import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
url = "https://www.reuters.com/"
print(f"Scraping: {url}")
try:
    resp = requests.get(url, headers=headers, timeout=10, verify=False)
    print(f"Status: {resp.status_code}")
    print(f"Length: {len(resp.text)}")
except Exception as e:
    print(f"Error: {e}")
