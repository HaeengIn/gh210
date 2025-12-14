document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const toggleBtn = document.getElementById("theme-toggle");

    const serverTheme = html.dataset.theme;
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        html.dataset.theme = savedTheme;
    } else if (serverTheme) {
        html.dataset.theme = serverTheme;
        localStorage.setItem("theme", serverTheme);
    } else {
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
            html.dataset.theme = "dark";
        } else {
            html.dataset.theme = "light";
        }
    }

    toggleBtn.addEventListener("click", async () => {
        const newTheme = html.dataset.theme === "dark" ? "light" : "dark";
        html.dataset.theme = newTheme;
        localStorage.setItem("theme", newTheme);
        try {
            const res = await fetch("/set_theme", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme: newTheme }),
            });
            if (!res.ok) {
                console.error("서버에 테마 저장 중 오류:", res.status);
            }
        } catch (err) {
            console.error("테마 저장 요청 실패:", err);
        }
    });
});

document.getElementById("error-complain").addEventListener("click", function (e) {
    e.preventDefault();
    alert("현재 민원창구와 연결된 데이터베이스가 멈춰있는 상태일 수 있습니다.\n관리자에게 문의해주세요.");
  });