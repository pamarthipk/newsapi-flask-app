from flask import Flask, jsonify, render_template, request  # ✅ Add `request`
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
    categories = ["general", "business", "entertainment", "health", "science", "sports", "technology"]

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # ✅ Clear old news before inserting new ones
    cursor.execute("DELETE FROM trending_news")

    for category in categories:
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"]

            for article in articles[:5]:  # ✅ Store 5 articles per category
                title = article["title"]
                source = article["source"]["name"]
                url = article["url"]

                cursor.execute(
                    "INSERT INTO trending_news (title, source, url, category) VALUES (%s, %s, %s, %s)",
                    (title, source, url, category)
                )

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ News data stored successfully.")

# API to Get News from MySQL
@app.route('/api/news')
def get_news():
    category = request.args.get("category", "general")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trending_news WHERE category = %s ORDER BY id DESC LIMIT 20", (category,))
    
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
