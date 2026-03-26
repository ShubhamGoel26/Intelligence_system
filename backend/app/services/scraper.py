from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re

def search_company(company_name):
    query = f"{company_name} company contact website"

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(r["href"])

    return results


def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        return text[:5000]  # limit size

    except Exception:
        return ""


def extract_contacts(text):
    # Email regex
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

    # Phone regex (India-focused)
    phones = re.findall(r"\+?\d[\d\s\-]{8,15}", text)

    return {
        "emails": list(set(emails)),
        "phones": list(set(phones))
    }

def get_company_data(company_name):
    urls = search_company(company_name)

    all_text = ""
    source_url = None

    for url in urls:
        text = scrape_website(url)

        if text:
            all_text += text
            source_url = url

    contacts = extract_contacts(all_text)

    return {
        "source": source_url,
        "emails": contacts["emails"],
        "phones": contacts["phones"],
        "raw_text": all_text[:2000]
    }

