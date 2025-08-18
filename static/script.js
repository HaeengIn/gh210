(() => {
    'use strict';

    // 브라우저에서 사용자의 모션 선호를 확인
    const prefersReducedMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // 스크롤 복원 제어
    if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
    }

    // 페이드 업 요소 관찰자 초기화
    function initFadeUpObserver() {
        const fadeEls = document.querySelectorAll('.fade-up');
        if (!fadeEls || fadeEls.length === 0) return;

        // IntersectionObserver가 없으면 즉시 표시
        if (!('IntersectionObserver' in window)) {
            fadeEls.forEach(el => el.classList.add('show'));
            return;
        }

        const observerOptions = { threshold: 0.2 };
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('show');
                    obs.unobserve(entry.target);
                }
            });
        }, observerOptions);

        fadeEls.forEach(el => observer.observe(el));
    }

    // 페이지 하단으로 스크롤하는 링크 초기화
    function initScrollBottomLink() {
        const scrollBottomLink = document.getElementById('scroll_bottom');
        if (!scrollBottomLink) return;

        scrollBottomLink.addEventListener('click', (e) => {
            e.preventDefault();
            const bottom = document.getElementById('page_bottom');
            const behavior = prefersReducedMotion ? 'auto' : 'smooth';
            if (bottom) {
                // scrollIntoView 옵션은 객체 지원이 보편적이므로 사용
                bottom.scrollIntoView({ behavior });
            } else {
                window.scrollTo({ top: document.body.scrollHeight, behavior });
            }
        }, { passive: false });
    }

    window.addEventListener('DOMContentLoaded', () => {
        initFadeUpObserver();
        initScrollBottomLink();
    });

    // 로드 완료 시 맨 위로 정렬 (reduced-motion 사용자 고려)
    window.addEventListener('load', () => {
        if (prefersReducedMotion) {
            window.scrollTo(0, 0);
        } else {
            // 즉시 위치를 0으로 설정 (부드러운 애니메이션은 링크에서만 사용)
            window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
        }
    });
})();