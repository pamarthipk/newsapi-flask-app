document.addEventListener("DOMContentLoaded", function () {
    const newsContainer = document.getElementById("newsContainer");
    const categorySelect = document.getElementById("categorySelect");

    function fetchNews(category = "general") {
        fetch(`/api/news?category=${category}`)
            .then(response => response.json())
            .then(data => {
                newsContainer.innerHTML = "";  // Clear old news

                data.forEach(news => {
                    let newsItem = `
                        <div class="col-md-4">
                            <div class="card mb-3 shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title">${news.title}</h5>
                                    <p class="card-text"><strong>Source:</strong> ${news.source}</p>
                                    <a href="${news.url}" target="_blank" class="btn btn-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                    `;
                    newsContainer.innerHTML += newsItem;
                });
            })
            .catch(error => console.error("Error fetching news:", error));
    }

    // Fetch news on page load
    fetchNews();

    // Change news when category is selected
    categorySelect.addEventListener("change", function () {
        fetchNews(this.value);
    });
});
