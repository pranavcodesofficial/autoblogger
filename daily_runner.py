from autoblogger.generator import generate_blog
from autoblogger.scraper import get_trending_topics
from datetime import date

brands = [
    {
        "brand": "abex.work",
        "search_query": "enterprise productivity AI tools abex.work"
    },
    {
        "brand": "hiringday.ai",
        "search_query": "AI in recruitment hiringday.ai"
    },
    {
        "brand": "libingo",
        "search_query": "automated LinkedIn outreach AI libingo"
    },
]

for topic in brands:
    print(f"🔍 Fetching trending topics for {topic['brand']}…")
    trending = get_trending_topics(topic["search_query"], max_results=1)
    image_query = topic["search_query"].split()[0] + " " + trending[0]['title'].split()[0] if trending else topic["search_query"]

    if trending:
        headline = trending[0]['title']
        snippet = trending[0].get('snippet', '')

        prompt = f"""
Act as a professional tech content writer. Write an engaging and high-quality 500-word blog post targeted at startup founders, product managers, and SaaS professionals.

Topic: "{headline}"

Context from current news: "{snippet}"

The blog must:
- Begin with a strong hook, stat, or quote
- Use subheadings or bullet points to break down the core idea
- Include real-world analogies or examples relevant to the brand
- Incorporate insights or implications for the industry
- End with a powerful takeaway or call to action
- Use an informative, modern, and slightly witty tone
- Avoid fluff, filler, or repeating generic facts

Ensure SEO-friendly structure and originality. This should read like something you'd publish on TechCrunch or HackerNoon.
""".strip()
    else:
        prompt = f"""
Act as a professional tech content writer. Write a unique, in-depth 500-word blog post targeted at startup founders and SaaS operators.

Topic: "{topic['search_query']}"

The blog should:
- Begin with a strong hook or question
- Use examples or analogies to explain technical ideas
- Cover current challenges and future implications
- Be formatted cleanly with subheadings or bullet points
- Include an original insight or controversial POV in the conclusion
- Sound natural, confident, and informative — like a blog from a top founder

Avoid fluff. Give value.
""".strip()

    filename = f"blogs/{topic['brand']}.{date.today()}.html"
    print(f"📝 Generating blog for {topic['brand']} → {filename}")
    generate_blog(prompt, filename, image_query)