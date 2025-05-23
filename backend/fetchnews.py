import requests   # import request module to send request
import json       # to handle the data
import os
from dotenv import load_dotenv
load_dotenv()

# "breaking-news" "world" "nation" "business" "technology" "entertainment" "sports" "science" "health"

def fetch_and_save_news(topic="breaking-news", file_name="data\\news_raw.json"):
    api_key = os.getenv("GNEWS_API_KEY")  # Replace with your actual GNews API key
    url = f"https://gnews.io/api/v4/top-headlines?topic={topic}&lang=en&country=in&token={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(news_data, file, indent=4, ensure_ascii=False)
        print(f"✅ News for topic '{topic}' saved to {file_name}")
    else:
        print(f"❌ Failed to fetch news for topic '{topic}':", response.status_code)

# Example usage:
if __name__ == "__main__":
    
    fetch_and_save_news("world", "static\\news_raw.json")
    #fetch_and_save_news("politics", "politics_news.json")
