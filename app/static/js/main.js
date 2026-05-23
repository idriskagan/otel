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

    // 6. Favorite Toggle AJAX
    const favoriteButtons = document.querySelectorAll('.favorite-toggle');
    if (favoriteButtons.length > 0) {
        const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
        const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';

        favoriteButtons.forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const hotelId = btn.getAttribute('data-hotel-id');
                if (!hotelId) return;
                
                try {
                    const response = await fetch(`/dashboard/favorite/${hotelId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        if (data.success) {
                            if (data.is_favorited) {
                                btn.style.color = '#e11d48';
                                const textSpan = btn.querySelector('.favorite-text');
                                if (textSpan) textSpan.textContent = 'Favorilerden Çıkar';
                            } else {
                                btn.style.color = 'var(--text-muted)';
                                const textSpan = btn.querySelector('.favorite-text');
                                if (textSpan) textSpan.textContent = 'Favorilere Ekle';
                            }
                            
                            if (window.location.pathname === '/dashboard/favorites' && !data.is_favorited) {
                                window.location.reload();
                            }
                        }
                    }
                } catch (error) {
                    console.error('Error toggling favorite:', error);
                }
            });
        });
    }

    // 7. Helpful Button AJAX
    const helpfulButtons = document.querySelectorAll('.helpful-btn');
    if (helpfulButtons.length > 0) {
        const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
        const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';

        helpfulButtons.forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                const reviewId = btn.getAttribute('data-review-id');
                if (!reviewId) return;
                
                try {
                    const response = await fetch(`/hotels/review/${reviewId}/helpful`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        if (data.success) {
                            const countSpan = btn.querySelector('.helpful-count');
                            if (countSpan) {
                                countSpan.textContent = parseInt(countSpan.textContent) + 1;
                            }
                            btn.disabled = true;
                            btn.style.color = 'var(--primary)';
                            btn.style.borderColor = 'var(--primary)';
                        }
                    }
                } catch (error) {
                    console.error('Error voting helpful:', error);
                }
            });
        });
    }
});

// Global functions for review forms
window.toggleEditForm = function(reviewId) {
    const form = document.getElementById(`edit-form-${reviewId}`);
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
};

window.toggleReplyForm = function(reviewId) {
    const form = document.getElementById(`reply-form-${reviewId}`);
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
};
