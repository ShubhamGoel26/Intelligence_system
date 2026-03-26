import requests
from bs4 import BeautifulSoup

def simple_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.select("a"):
        href = a.get("href")
        if "http" in href:
            links.append(href)

    return links[:5]