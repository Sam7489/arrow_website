import cohere
import json
import difflib
import os
from dotenv import load_dotenv
load_dotenv()

def generate_viral_news():
    # Load JSON data
    json_path = 'static\\news_raw.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract all titles
    titles = [article['title'] for article in data['articles']]

    # Cohere API setup
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    print(COHERE_API_KEY)
    co = cohere.Client(COHERE_API_KEY)

    # Build prompt
    preamble = """
You are a viral content rating model that evaluates news headlines or short news titles based on their potential to go viral on Instagram.

You consider:
- Celebrity involvement
- Controversy or drama
- Emotional appeal
- Humor or shock value
- Relevance to youth culture or trends
- Visual storytelling potential

Rate each news title on a scale from 1 to 10, where:
1 = Not viral at all
5 = Moderately viral
10 = Extremely viral and likely to trend

Respond in this format:
"[news title]" virality score: X
Do not explain the rating.
"""

    full_prompt = preamble + "\n\nRate the following news titles:\n"
    for idx, title in enumerate(titles, 1):
        full_prompt += f"{idx}. {title}\n"

    # Call Cohere
    response = co.generate(
        model="command-r-plus",
        prompt=full_prompt,
        temperature=0.5,
        max_tokens=800
    )

    print("✅ Response from Cohere received.")
    output = response.generations[0].text.strip()

    # Parse and update JSON
    updated_count = 0
    lines = output.splitlines()

    for line in lines:
        if 'virality score' in line:
            try:
                parts = line.rsplit('virality score:', 1)
                raw_title = parts[0].strip().strip('"')
                score = int(parts[1].strip())

                # Match title with fuzzy logic
                match = difflib.get_close_matches(raw_title, titles, n=1, cutoff=0.5)
                if match:
                    matched_title = match[0]
                    for article in data['articles']:
                        if article['title'] == matched_title:
                            article['virality_score'] = score
                            updated_count += 1
                            break
                else:
                    print(f"⚠️ Could not match: {raw_title[:50]}...")

            except Exception as e:
                print(f"⚠️ Error parsing line: {line} | {e}")

    # Save the updated file
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ {updated_count} articles updated using titles.")
    else:
        print("❌ No articles were updated.")

if __name__ == "__main__":
    generate_viral_news()
