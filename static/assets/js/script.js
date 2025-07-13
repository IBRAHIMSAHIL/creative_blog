document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ blog.js loaded");

  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  )?.value;

  // ❤️ Like Button
  const likeBtn = document.getElementById("likeBtn");
  if (likeBtn) {
    const blogId = likeBtn.dataset.postId;

    likeBtn.addEventListener("click", function () {
      fetch(`/post/${blogId}/like/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          likeBtn.innerHTML = `${
            data.liked ? "❤️ Unlike" : "🤍 Like"
          } (<span id="likeCount">${data.totalLikes}</span>)`;
        })
        .catch((err) => console.error("❌ Like request failed:", err));
    });
  }

  // 🔖 Bookmark Button
  const bookmarkBtn = document.getElementById("bookmarkBtn");
  const bookmarkForm = document.getElementById("bookmarkForm");
  if (bookmarkBtn && bookmarkForm) {
    const blogId = bookmarkForm.dataset.postId;

    bookmarkBtn.addEventListener("click", function () {
      fetch(`/post/${blogId}/bookmark/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          const icon = document.getElementById("bookmarkIcon");
          const text = document.getElementById("bookmarkText");

          if (icon && text) {
            icon.textContent = data.bookmarked ? "🔖" : "📑";
            text.textContent = data.bookmarked ? "Bookmarked" : "Bookmark";
          }
        })
        .catch((err) => console.error("❌ Bookmark request failed:", err));
    });
  }

  // 📊 Admin Chart Logic
  const chartEl = document.getElementById("postsChart");
  const chartDataScript = document.getElementById("monthsData");

  if (chartEl && chartDataScript) {
    console.log("📊 Chart rendering initiated");

    const monthlyData = JSON.parse(chartDataScript.textContent);
    const labels = monthlyData.map((item) => item.month);
    const counts = monthlyData.map((item) => item.count);

    new Chart(chartEl, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Monthly Posts",
            data: counts,
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.1)",
            tension: 0.4,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
            },
          },
        },
      },
    });
  }
});
