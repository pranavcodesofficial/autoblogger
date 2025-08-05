
from autoblogger.generator import generate_blog
from autoblogger.scraper import get_trending_topics
from datetime import date

brands = [
    {
        "brand": "abex.work",
        "search_query": "Abex.work enterprise AI tools"
    },
    {
        "brand": "hiringday.ai",
        "search_query": "AI in recruitment hiringday.ai"
    },
    {
        "brand": "libingo",
        "search_query": "AI in education libingo"
    },
]

for topic in brands:
    print(f"🔍 Fetching trending topics for {topic['brand']}…")
    trending = get_trending_topics(topic["search_query"], max_results=1)

    if trending:
        headline = trending[0]['title']
        prompt = f"Write a 500-word blog post based on this headline: '{headline}'"
    else:
        prompt = f"Write a 500-word blog about {topic['search_query']}"

    filename = f"blogs/{topic['brand']}.{date.today()}.html"
    print(f"📝 Generating blog for {topic['brand']} → {filename}")
    generate_blog(prompt, filename)