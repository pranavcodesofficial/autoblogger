# scraper.py
from duckduckgo_search import DDGS
from datetime import datetime
import logging

def get_trending_topics(query: str, max_results: int = 5):
    results = []
    try:
        with DDGS() as ddgs:
            search_results = ddgs.news(query, max_results=max_results)
            for result in search_results:
                results.append({
                    "title": result.get("title"),
                    "snippet": result.get("body"),
                    "url": result.get("url")
                })
    except Exception as e:
        logging.error(f"[{datetime.now()}] Error while scraping: {e}")
    return results

if __name__ == "__main__":
    tools = ["Libingo language learning AI", "Hiring.ai recruitment trends", "Abex.work productivity AI"]

    for tool in tools:
        print(f"\n🔍 Trending for {tool.split()[0]}:\n")
        topics = get_trending_topics(tool)
        for t in topics:
            print(f"- {t['title']}\n  {t['snippet']}\n  {t['url']}\n")
        