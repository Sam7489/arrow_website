from flask import Flask, render_template , request , redirect, url_for , jsonify, session
import json
from backend.fetchnews import fetch_and_save_news
from backend.virality import generate_viral_news    # importing to rank the news for virality
from backend.prompt_for_image import image_prompts
from backend.image_genertion import image_final
import os
from backend.generate_viral_titles import generate_viral_titles     # take the viral titles
from backend.text_below_image  import process_selected_titles_and_images
from backend.fetch_news_url import fetch_and_store_article
from backend.image_download_from_news import download_from_url

app = Flask(__name__)
app.secret_key = 'shivam'

# main page
@app.route('/')
def home():
    return render_template("index.html")

# fetch news page
@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    topic = request.form['topic']    # data for the news fetcher ai
    print("Topic selected:", topic)
    # Here you can call your cnews API using the topic value
    fetch_and_save_news(topic=topic, file_name="static\\news_raw.json")
    generate_viral_news()     # ranking virality
        
    return redirect(url_for('show_news'))

# fetch news by url
@app.route('/upload-article', methods=['POST'])
def upload_article():
    url_recv = request.form['news_url']
    fetch_and_store_article(url=url_recv, json_path="static\\news_raw.json")
    return redirect(url_for('prompts'))  # You can create this new HTML page


# show news on the webpage
@app.route('/show-news')
def show_news():
    with open('static/news_raw.json', 'r', encoding='utf-8') as file:
        news_data = json.load(file)
    
    return render_template('news.html', news=news_data)

# delete unwanted news
@app.route('/delete-news', methods=['POST'])
def delete_news():
    data = request.get_json()
    title_to_delete = data.get('title')

    if not title_to_delete:
        return jsonify({'success': False, 'error': 'No title provided'})

    with open('static/news_raw.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)

    for i, article in enumerate(news_data['articles']):
        if article.get('title') == title_to_delete:
            del news_data['articles'][i]

            with open('static/news_raw.json', 'w', encoding='utf-8') as f_out:
                json.dump(news_data, f_out, indent=4)

            return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Article not found'})


# generate prompts for image generation
@app.route('/generating-prompts')
def prompts():
      
    image_prompts()
    
    image_final()    # generates images for the title in news_raw.json
    
    return redirect(url_for('show_images'))

# image generation
@app.route('/show_images')
def show_images():
    download_from_url()    # downloads image from the url given in the news.json
    image_folder = os.path.join('static', 'images')
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    return render_template('images.html', images=image_files)

@app.route('/final', methods=['POST'])
def final():
    selected_images = request.form.getlist('selected_images')
    session['selected_images'] = selected_images  # store in session for download page

    image_folder = os.path.join('static', 'images')
    all_images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    for image in all_images:
        if image not in selected_images:
            image_path = os.path.join(image_folder, image)
            try:
                os.remove(image_path)
                print(f"🗑️ Deleted: {image}")
            except Exception as e:
                print(f"❌ Error deleting {image}: {e}")

    return redirect(url_for('choose_title'))    # choose title page pe redirect karna hai

# CHOOSE title for the post
@app.route('/choose_title')
def choose_title():
    # Read the news data
    with open('static/news_raw.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    # Create one big text string with all news titles and URLs (not clickable)
    news_texts = []
    for article in news_data.get('articles', []):
        title = article.get('title', 'No Title')
        url = article.get('url', 'No URL')
        news_texts.append(f"{title} - {url}")
    combined_news_text = "\n".join(news_texts)
    
    # Pass this text along with images to the template
    selected_images = session.get('selected_images', [])
    return render_template('choose_title.html', image_files=selected_images, news_text=combined_news_text)


@app.route('/save_selected_titles', methods=['POST'])
def save_selected_titles():
    results = []

    for key in request.form:
        if key.startswith("title_"):
            index = key.split("_")[-1]
            title = request.form[key]
            image_name = request.form.get(f"image_name_{index}")

            if title and image_name:
                results.append({
                    "image": image_name,
                    "title": title.strip()
                })

    output_path = os.path.join("static", "selected_titles.json")
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=2, ensure_ascii=False)

    return redirect(url_for('download_page'))


# download the image
@app.route('/download')
def download_page():
    process_selected_titles_and_images(json_path="static/selected_titles.json",
        image_dir="static/images",
        output_dir="static/outputs")
    
    output_folder = 'static/outputs'
    image_files = [f for f in os.listdir(output_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Generate relative paths like "outputs/final_post_1.jpg"
    image_paths = [f"outputs/{filename}" for filename in sorted(image_files)]
    
    return render_template('download.html', images=image_paths)

@app.route('/about-us')
def about():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)