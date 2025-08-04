import requests
import os
import time
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()

def get_unsplash_image(query: str) -> str:
    response = requests.get(f"https://source.unsplash.com/1600x900/?{query}")
    return response.url if response.status_code == 200 else ""

def generate_blog(prompt: str, filename: str) -> None:
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
                break
            elif response.status_code == 503:
                print("⚠️ Service Unavailable. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Groq API Error: {res_json}")
                return
        except RequestException as e:
            print(f"🚫 Request failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    else:
        print("❌ Failed to get response from Groq API after 3 attempts.")
        return

    # Generate images
    thumbnail = get_unsplash_image("AI recruitment")
    section_img = get_unsplash_image("interview AI")

    formatted_content = blog_content.replace('\n\n', '</p><p>').replace('\n', '<br>')

    html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{prompt[:50]}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: auto; line-height: 1.6; padding: 2rem; }}
        h1 {{ color: #222; }}
        img {{ max-width: 100%; margin: 1rem 0; border-radius: 8px; }}
        p {{ margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <h1>{prompt}</h1>
    <img src="{thumbnail}" alt="Blog Thumbnail">
    <p>{formatted_content}</p>
    <img src="{section_img}" alt="Supporting Visual">
</body>
</html>
"""
    with open(filename, "w") as f:
        f.write(html_output)

    print(f"✅ Blog generated as {filename}")
    
if __name__ == "__main__":
    from datetime import date
    generate_blog(
        "Write a 500-word blog on current AI trends in recruitment.",
        f"blogs/test_ai_blog_{date.today()}.html"
    )