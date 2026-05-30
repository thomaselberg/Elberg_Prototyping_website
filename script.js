document.addEventListener('DOMContentLoaded', () => {
    // Image gallery / carousel
    document.querySelectorAll('.gallery').forEach(gallery => {
        const images = Array.from(gallery.querySelectorAll('.gallery-track img'));
        if (images.length === 0) return;

        let current = 0;

        // Generate dots
        const footer = document.createElement('div');
        footer.className = 'gallery-footer';
        const dots = images.map((_, i) => {
            const dot = document.createElement('button');
            dot.className = 'gallery-dot' + (i === 0 ? ' active' : '');
            dot.setAttribute('aria-label', 'Image ' + (i + 1));
            footer.appendChild(dot);
            return dot;
        });

        if (images.length > 1) {
            gallery.appendChild(footer);
        } else {
            gallery.querySelectorAll('.gallery-arrow').forEach(a => a.style.display = 'none');
        }

        function goTo(index) {
            images[current].classList.remove('active');
            dots[current].classList.remove('active');
            current = (index + images.length) % images.length;
            images[current].classList.add('active');
            dots[current].classList.add('active');
        }

        gallery.querySelector('.gallery-prev').addEventListener('click', () => goTo(current - 1));
        gallery.querySelector('.gallery-next').addEventListener('click', () => goTo(current + 1));
        dots.forEach((dot, i) => dot.addEventListener('click', () => goTo(i)));
    });


    // Reveal animations on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => observer.observe(card));

    // Interactive glow effect for expertise items mimicking modern web trends
    const expertiseItems = document.querySelectorAll('.expertise-item');
    
    expertiseItems.forEach(item => {
        item.addEventListener('mousemove', (e) => {
            const rect = item.getBoundingClientRect();
            // Calculate cursor position relative to the element
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Set CSS variables that are used in the ::before pseudo-element
            item.style.setProperty('--mouse-x', `${x}px`);
            item.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});
