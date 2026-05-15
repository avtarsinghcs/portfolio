from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# =========================================
# SEARCH TOOL
# =========================================

def web_search(query: str):

    enhanced_query = f"""
    {query}

    Rules:
    - Return direct article URLs only
    - Avoid homepages
    - Avoid category pages
    - Prefer detailed journalism
    - Return at least 5 article links
    """

    response = tavily.search(
        query=enhanced_query,
        search_depth="advanced",
        max_results=5
    )

    urls = []

    for result in response["results"]:
        urls.append(result["url"])

    return urls


# =========================================
# SCRAPER TOOL
# =========================================

def scrape_url(url: str):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([
            p.get_text()
            for p in paragraphs
        ])

        cleaned_text = text[:5000]

        return f"""
SOURCE:
{url}

CONTENT:
{cleaned_text}
"""

    except Exception as e:

        return f"""
SOURCE:
{url}

ERROR:
{str(e)}
"""