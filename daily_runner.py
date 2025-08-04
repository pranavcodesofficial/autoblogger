# daily_runner.py
from autoblogger.generator import generate_blog
from datetime import date

blogs = [
    {
        "brand": "abex.work",
        "prompt": "Write a 500-word blog about automation in enterprise AI tools.",
    },
    {
        "brand": "hiringday.ai",
        "prompt": "Write a 500-word blog about how AI is reshaping the hiring process.",
    },
    {
        "brand": "libingo",
        "prompt": "Write a 500-word blog about AI-powered learning in higher education.",
    },
]

for topic in blogs:
    filename = f"blogs/{topic['brand']}.{date.today()}.html"
    print(f"📝 Generating blog for {topic['brand']} → {filename}")
    generate_blog(topic["prompt"], filename)