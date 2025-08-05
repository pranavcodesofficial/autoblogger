import requests
import os
import time
from datetime import date
from dotenv import load_dotenv
from requests.exceptions import RequestException
import markdown  # ✅ Markdown parser

load_dotenv()

def get_unsplash_image(query: str) -> str:
    try:
        response = requests.get(f"https://source.unsplash.com/1600x900/?{query}", allow_redirects=True)
        if response.status_code == 200:
            return response.url
    except:
        pass
    # 🔁 Fallback to a default image if Unsplash fails
    return "https://images.unsplash.com/photo-1498050108023-c5249f4df085"

def format_blog_content(content: str) -> str:
    return markdown.markdown(content)

def generate_blog(prompt: str, filename: str, image_query: str) -> None:
    API_KEY = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-70b-8192"
    }

    for attempt in range(3):
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            res_json = response.json()

            if 'choices' in res_json:
                blog_content = res_json['choices'][0]['message']['content']

                # 🧹 Remove any echoed prompt
                if blog_content.strip().startswith("Act as a professional"):
                    blog_content = "\n".join(blog_content.strip().split('\n')[3:])

                break
            elif response.status_code == 503:
                print("⚠️ Groq Service Unavailable. Retrying...")
                time.sleep(5)
            else:
                print("❌ Groq API error:", res_json)
                return
        except RequestException as e:
            print(f"🚫 Request failed: {e}")
            time.sleep(5)
    else:
        print("❌ Failed after 3 attempts.")
        return

    # 🎯 Get real images
    thumbnail = get_unsplash_image(image_query)
    support_img = get_unsplash_image(image_query + " tech")

    # 🏷 Extract first line as title
    first_line = blog_content.strip().split('\n')[0].replace("*", "").replace('"', '')
    html_title = first_line if len(first_line) < 100 else "Latest AI Blog"

    # ✨ Format the content
    formatted_content = format_blog_content(blog_content)

    # 🧾 Build HTML
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{html_title}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: auto; line-height: 1.6; padding: 2rem; }}
        h1 {{ color: #222; }}
        img {{ max-width: 100%; margin: 1rem 0; border-radius: 8px; }}
        p {{ margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <h1>{html_title}</h1>
    <img src="{thumbnail}" alt="Blog Thumbnail">
    {formatted_content}
    <img src="{support_img}" alt="Supporting Visual">
</body>
</html>
"""

    with open(filename, "w") as f:
        f.write(html_output)
    print(f"✅ Blog generated as {filename}")