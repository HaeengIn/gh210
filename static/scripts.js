document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const toggleBtn = document.getElementById("theme-toggle");

    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        html.dataset.theme = savedTheme;
    } else if (!html.dataset.theme) {
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
