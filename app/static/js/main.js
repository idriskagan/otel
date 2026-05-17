/* ========================================
   StayFinder — Main JavaScript
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const toggle = document.getElementById('navbar-toggle');
    const menu = document.getElementById('navbar-menu');
    const auth = document.getElementById('navbar-auth');

    if (toggle) {
        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
            auth.classList.toggle('active');
        });
    }

    // Auto-dismiss flash messages
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });

    // Set minimum date for date inputs
    const today = new Date().toISOString().split('T')[0];
    const checkin = document.getElementById('search-checkin');
    const checkout = document.getElementById('search-checkout');

    if (checkin) checkin.min = today;
    if (checkout) checkout.min = today;

    if (checkin && checkout) {
        checkin.addEventListener('change', () => {
            checkout.min = checkin.value;
            if (checkout.value && checkout.value < checkin.value) {
                checkout.value = checkin.value;
            }
        });
    // 4. Navbar scroll efekti
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 5. Scroll ile beliren elementler (fade-in)
    const fadeElements = document.querySelectorAll('.stat-card, .city-card, .hotel-card');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    }
});
