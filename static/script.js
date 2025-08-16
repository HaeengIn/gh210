if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}

window.addEventListener('DOMContentLoaded', () => {
    const fadeEls = document.querySelectorAll('.fade-up');
    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('show');
                    obs.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.2
        }
    );
    fadeEls.forEach(el => observer.observe(el));
    const scrollBottomLink = document.getElementById('scroll_bottom');
    if (scrollBottomLink) {
        scrollBottomLink.addEventListener('click', function(e) {
            e.preventDefault();
            const bottom = document.getElementById('page_bottom');
            if (bottom) {
                bottom.scrollIntoView({ behavior: 'smooth' });
            } else {
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }
        });
    }
});

window.addEventListener('load', () => {
    window.scrollTo(0, 0);
});