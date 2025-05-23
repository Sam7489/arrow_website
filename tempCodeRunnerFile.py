from flask import Flask, render_template , request , redirect, url_for
import json
from backend.fetchnews import fetch_and_save_news

app = Flask(__name__)

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
    # news_data = get_news_from_api(topic)
    # return render_template('news.html', news=news_data)
    return redirect(url_for('show_news'))


@app.route('/show-news')
def show_news():
    with open('static/news_raw.json', 'r', encoding='utf-8') as file:
        news_data = json.load(file)
    
    return render_template('news.html', news=news_data)
@app.route('/show-news1')
def show_news1():
    with open('static/news_raw.json', 'r', encoding='utf-8') as file:
        news_data = json.load(file)
    
    return render_template('news1.html', news=news_data)

@app.route('/test')
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)