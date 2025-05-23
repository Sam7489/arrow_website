from groq import Groq
import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()

# ✅ Load news articles correctly from updated file
with open("static/news_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ✅ Normalize descriptions from updated format
descriptions = []

if isinstance(data, dict) and "articles" in data:
    for item in data["articles"]:
        if isinstance(item, dict):
            text = item.get("news") or item.get("description") or item.get("title")
            if text:
                descriptions.append(text)
else:
    raise ValueError("news_raw.json should contain a dictionary with an 'articles' list")

# ✅ Initialize Groq client
GroqAPIKey = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GroqAPIKey)

# ✅ System prompt
SystemPrompt = """
Hello, I am Sam, and you are a powerful AI.
You are a creative AI that generates imaginative and descriptive image generation prompts.
Your job is to visualize news in artistic ways for image-generation models like Midjourney or DALL·E.

Rules:
- For each news item, generate 4 creative prompts.
- Each prompt should be vivid, specific, and visually unique.
- Avoid repetition and generic phrases.
- Use detailed scenes, emotions, environments, and characters.
"""

SystemChatBot = [{"role": "system", "content": SystemPrompt}]

def RealtimeInformation():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %d %B %Y')}. Time: {now.strftime('%H:%M:%S')}."

def generate_image_prompts(news_item):
    prompt = f"""News headline: "{news_item}"

Generate 4 unique and imaginative prompts for an AI image generator. Each should reflect the essence of the news, using detailed, artistic, and creative description. Number them like a list."""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [
            {"role": "system", "content": RealtimeInformation()},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.85,
        top_p=1
    )

    return completion.choices[0].message.content.strip()

def process_all_news(news_list):
    prompts_list = []
    for news in news_list:
        print(f"\n📰 Processing: {news}")
        prompts = generate_image_prompts(news)
        prompt_lines = [p.strip().lstrip("1234.:- ") for p in prompts.split("\n") if p.strip()]
        prompts_list.append([news, prompt_lines])
    return prompts_list

def image_prompts():
    with open("static/news_raw.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ Normalize descriptions from updated format
    descriptions = []
    if isinstance(data, dict) and "articles" in data:
        for item in data["articles"]:
            if isinstance(item, dict):
                text = item.get("title") or item.get("description") or item.get("news")
                if text:
                    descriptions.append(text)
    else:
        raise ValueError("news_raw.json should contain a dictionary with an 'articles' list")

    if descriptions:
        all_data = process_all_news(descriptions)

        with open("static/generated_prompts.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)

        print("\n✅ All prompts saved in 'static/generated_prompts.json'")
    else:
        print("⚠️ No news items to process.")


if __name__ == "__main__":
    image_prompts()
