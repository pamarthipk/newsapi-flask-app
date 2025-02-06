document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/news')  // ✅ Fetch news instead of trends
        .then(response => response.json())
        .then(data => {
            let newsContainer = document.getElementById("newsContainer");
            newsContainer.innerHTML = "";  // Clear old content

            data.forEach(news => {
                let newsItem = `
                    <div class="news-card">
                        <h3>${news.title}</h3>
                        <p><strong>Source:</strong> ${news.source}</p>
                        <a href="${news.url}" target="_blank">Read More</a>
                    </div>
                `;
                newsContainer.innerHTML += newsItem;
            });
        })
        .catch(error => console.error("Error fetching news:", error));
});
