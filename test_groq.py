import requests

API_KEY = "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"  # Replace this with your actual key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {"role": "user", "content": "Write a 500-word blog on current AI trends in recruitment."}
    ],
    "model": "llama3-70b-8192"
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
print("Raw response:", response.status_code, response.text)
print(response.status_code)
print(response.json())