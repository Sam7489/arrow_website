import requests
import urllib.parse
import json

# Open the JSON file of the list of image prompts


def generate_and_download_image(prompt, seed=43, model="flux", filename="ai_image1.jpg"):
    # Encode the prompt properly for URLs
    formatted_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?seed={seed}&model={model}"

    print(f"🔍 Fetching image from: {url}")

    try:
        response = requests.get(url, stream=True, timeout=15)

        if response.status_code == 200:
            with open(f"static/images/{filename}", 'wb') as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)
            print(f"✅ Image downloaded successfully as '{filename}'")
        else:
            print(f"❌ Failed to fetch image. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"🚨 Error occurred: {e}")

# 🔧 Example usage:
def image_final():
    with open("static/generated_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in range(len(data)):
        headline = data[i][0]
        prompts = data[i][1][1:]  # skip the first item (it's just a label/description)

        for j, prompt in enumerate(prompts):
            filename = f"{headline[:40].replace('/', '_')}_{j+1}.jpg"  # truncate filename if needed
            generate_and_download_image(prompt=prompt, seed=43, filename=filename)
        
if __name__ == "__main__":
    image_final()