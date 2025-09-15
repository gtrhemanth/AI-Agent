from duckduckgo_search import DDGS
import wikipedia
import requests
from bs4 import BeautifulSoup

def ddg_search(query: str, max_results: int = 5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({"title": r.get("title"), "href": r.get("href"), "body": r.get("body")})
    return results

def wiki_summary(topic: str, sentences: int = 3):
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(topic, sentences=sentences, auto_suggest=False, redirect=True)
    except Exception:
        try:
            return wikipedia.summary(topic, sentences=sentences)
        except Exception as e:
            return f"Could not find a summary for '{topic}': {e}"

def fetch_url(url: str, max_chars: int = 15000):
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script","style","noscript"]): 
            tag.decompose()
        text = "\n".join(t.strip() for t in soup.get_text("\n").splitlines() if t.strip())
        return text[:max_chars]
    except Exception as e:
        return f"Error fetching URL: {e}"
