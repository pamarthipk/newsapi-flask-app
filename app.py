from flask import Flask, jsonify, render_template
import mysql.connector
import requests
import threading
import time

app = Flask(__name__)

# MySQL Connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "groot",
    "database": "trends_data"
}

# NewsAPI Configuration (Replace with your API key)
API_KEY = "bc94220d58b3403c8ea280b3e541f05b"

# Fetch Trending News from NewsAPI
def fetch_trending_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"]

        # ✅ Store in MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # ✅ Clear old news before inserting new ones (optional)
        cursor.execute("DELETE FROM trending_news")

        for article in articles[:200]:  # ✅ Store top 20 articles
            title = article["title"]
            source = article["source"]["name"]
            url = article["url"]

            cursor.execute(
                "INSERT INTO trending_news (title, source, url) VALUES (%s, %s, %s)",
                (title, source, url)
            )

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ News data stored successfully.")

    else:
        print("❌ Error fetching news:", data)

# API to Get News from MySQL
@app.route('/api/news')
def get_news():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trending_news ORDER BY id DESC LIMIT 200")  # ✅ Fetch 20 articles
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# Load HTML Page
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Automatically fetch news every hour
def auto_update_news():
    while True:
        fetch_trending_news()
        time.sleep(3600)  # ✅ Fetch news every hour (3600 seconds)

# ✅ Run the auto-update function in a separate thread
threading.Thread(target=auto_update_news, daemon=True).start()

if __name__ == '__main__':
    fetch_trending_news()  # Fetch news on startup
    app.run(debug=True)
