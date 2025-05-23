from groq import Groq
import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()


# Load the news data
with open("static\\news_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract descriptions from news data
if isinstance(data, list) and isinstance(data[0], str):
    descriptions = data
elif isinstance(data, list) and isinstance(data[0], dict):
    descriptions = [item.get("description") or item.get("news") for item in data if item.get("description") or item.get("news")]
elif isinstance(data, dict) and "articles" in data:
    descriptions = [item.get("description") or item.get("news") for item in data["articles"] if item.get("description") or item.get("news")]
else:
    raise ValueError("Unexpected data format in news_raw.json")

# Initialize Groq client
GroqAPIKey = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GroqAPIKey)

# System prompt for Instagram-style titles
SystemPrompt = """
Hey! You're a viral content wizard ✨. Your job is to take boring news descriptions and turn them into short, scroll-stopping Instagram-friendly titles 🧠💥

Rules:
- Give 4 catchy, unique, and *responsibly exciting* titles for each news description.
- Keep them of 15 words or more.
- Avoid clickbait clichés (like "You won't believe...") but still make them powerful.
- Think viral, short, fun, but *not fake*.
- The vibe is more Insta Reel caption, less news anchor.
- reader should understand what is the news saying , without reading the full news.
- don't build suspence only deliver news
"""

SystemChatBot = [{"role": "system", "content": SystemPrompt}]

def RealtimeInformation():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %d %B %Y')}. Time: {now.strftime('%H:%M:%S')}."

def generate_titles(description):
    user_prompt = f"""News Description:\n\"{description}\"\n\nCreate 4 unique Instagram-style viral titles."""
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [
            {"role": "system", "content": RealtimeInformation()},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=300,
        temperature=0.9,
        top_p=1
    )

    return completion.choices[0].message.content.strip()

# Generate titles for all descriptions
def process_all_titles(descriptions_list):
    final_titles = []
    for desc in descriptions_list:
        print(f"\n📌 Generating titles for:\n{desc}")
        titles_text = generate_titles(desc)
        lines = [line.strip().lstrip("1234.:- ") for line in titles_text.split("\n") if line.strip()]
        final_titles.append({
            "description": desc,
            "titles": lines
        })
    return final_titles

# Main script
def generate_viral_titles():
    if descriptions:
        title_data = process_all_titles(descriptions)

        # Save output
        with open("static\\generated_titles.json", "w", encoding="utf-8") as f:
            json.dump(title_data, f, indent=4, ensure_ascii=False)

        print("\n✅ All titles saved in 'static/generated_titles.json'")
    else:
        print("⚠️ No descriptions found in news_raw.json")

# Entry point
if __name__ == "__main__":
    generate_viral_titles()
