document.addEventListener("DOMContentLoaded", () => {
    // Set up the Intersection Observer for smooth scrolling fade-ins
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Triggers when 15% of the element is visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the smooth 'show' class which triggers the CSS transition
                entry.target.classList.add('show');
                // Unobserve after showing so it doesn't animate again if scrolling up
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Grab all elements we want to fade in and observe them
    const hiddenElements = document.querySelectorAll('.hidden');
    hiddenElements.forEach((el) => {
        observer.observe(el);
    });
});
