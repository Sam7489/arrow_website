import json
import os
from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse

def fetch_and_store_article(url, json_path="static\\news_raw.json"):
    try:
        # Step 1: Parse the article
        article = Article(url)
        article.download()
        article.parse()

        # Step 2: Generate article data
        article_data = {
            "title": article.title or "",
            "description": article.meta_description or article.title or "",
            "content": article.text or "",
            "url": url,
            "image": article.top_image or "",
            "publishedAt": datetime.utcnow().isoformat() + "Z",
            "source": {
                "name": urlparse(url).netloc.replace("www.", "").title(),
                "url": f"https://{urlparse(url).netloc}"
            },
            "virality_score": 0  # You can calculate based on shares/comments later
        }
        # Step 3: Create new data structure with just this article
        data = {
            "totalArticles": 1,
            "articles": [article_data]
        }

        # Step 4: Save it to the file (overwrite mode)
        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print("✅ Article saved (overwritten) successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

# 🔥 Example usage
if __name__ == "__main__":
    url = input("Enter a news article URL: ").strip()
    fetch_and_store_article(url)
