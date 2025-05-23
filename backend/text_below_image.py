import os
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

def add_text_below_image(image_path, text, output_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # 👉 Crop 60px from the bottom
    cropped_img = img.crop((0, 0, width, height - 60))
    cropped_height = height - 60

    # Font setup
    font_path = "static/Montserrat-Bold.ttf"
    font_size = 45
    try:
        font = ImageFont.truetype(font_path, font_size)
        print("🎉 Custom font loaded.")
    except IOError:
        print("⚠️ Font not found. Using default.")
        font = ImageFont.load_default()

    # 👉 Wrap the text into lines that fit the image width
    wrapper = textwrap.TextWrapper(width=40)
    lines = wrapper.wrap(text)

    # Recalculate new text height
    line_spacing = 15
    total_text_height = sum([font.getbbox(line)[3] for line in lines]) + (len(lines) - 1) * line_spacing

    # Create new image with space below
    padding_top = 40
    padding_bottom = 40
    new_height = cropped_height + total_text_height + padding_top + padding_bottom
    new_img = Image.new("RGB", (width, new_height), color=(0, 0, 20))
    new_img.paste(cropped_img, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(new_img)
    y = cropped_height + padding_top
    for line in lines:
        line_width = font.getbbox(line)[2]
        x = (width - line_width) // 2
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += font.getbbox(line)[3] + line_spacing

    new_img.save(output_path)
    print(f"✅ Saved: {output_path}")

def process_selected_titles_and_images(json_path, image_dir, output_dir):
    with open(json_path, "r", encoding="utf-8") as f:
        selected_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    for idx, entry in enumerate(selected_data):
        image_filename = entry["image"]
        title = entry["title"]

        image_path = os.path.join(image_dir, image_filename)
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            continue

        output_path = os.path.join(output_dir, f"final_post_{idx + 1}.jpg")
        add_text_below_image(image_path, title, output_path)

if __name__ == "__main__":
    process_selected_titles_and_images(
        json_path="static/selected_titles.json",
        image_dir="static/images",
        output_dir="static/outputs"
    )
