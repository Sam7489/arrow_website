import requests
import os
import json
from PIL import Image
from io import BytesIO

def download_and_resize_image(image_url, save_path, size=(1080, 1080)):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        resized_img.save(save_path)

        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Error processing {image_url}: {e}")

def download_from_url(json_path="static/news_raw.json", image_folder="static/images"):
    # Ensure the image folder exists
    os.makedirs(image_folder, exist_ok=True)

    # Load the news JSON
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print("❌ Failed to load JSON file:", e)
        return

    articles = data.get("articles", [])

    for idx, article in enumerate(articles):
        image_url = article.get("image", "") or article.get("image_url", "")
        if not image_url:
            print(f"⚠️ No image URL for article {idx + 1}")
            continue

        filename = f"image_{idx + 1}.jpg"
        save_path = os.path.join(image_folder, filename)

        download_and_resize_image(image_url, save_path)

if __name__ == "__main__":
    download_from_url()
