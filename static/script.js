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
                                <div class="col-lg-4 col-md-6 mb-4">
                                    <div class = "card shadow-sm h-100">
                                        <img src="${news.image_url || 'https://via.placeholder.com/300'}" class="card-img-top" alt="News Image">
                                        <div class="card-body d-flex flex-column">
                                            <h5 class="card-title">${news.title}</h5>
                                            <p class="card-text text-muted">${news.source}</p>
                                            <a href="${news.url}" target="_blank" class="btn btn-primary mt-auto">Read More</a>
                                        </div>
                                    </div>
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
document.addEventListener("DOMContentLoaded", function () {
    const body = document.getElementById("body");
    const toggle = document.getElementById("darkModeToggle");

    toggle.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", body.classList.contains("dark-mode") ? "enabled" : "disabled");
    });

    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
    }
});
