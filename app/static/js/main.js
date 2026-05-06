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
    }
});
