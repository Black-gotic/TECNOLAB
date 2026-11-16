document.addEventListener('DOMContentLoaded', () => {
    // Destacar o link da navegação conforme a URL atual
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    const menuToggle = document.querySelector('.menu-toggle');
    const navigation = document.querySelector('.nav-links');
    if (menuToggle && navigation) {
        menuToggle.addEventListener('click', () => {
            const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', String(!isOpen));
            menuToggle.setAttribute('aria-label', isOpen ? 'Abrir menu' : 'Fechar menu');
            navigation.classList.toggle('is-open', !isOpen);
        });

        navigation.addEventListener('click', event => {
            if (event.target.closest('a')) {
                navigation.classList.remove('is-open');
                menuToggle.setAttribute('aria-expanded', 'false');
                menuToggle.setAttribute('aria-label', 'Abrir menu');
            }
        });
    }

    // Fechar automaticamente os alertas após 5 segundos
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(() => msg.remove(), 500);
            });
        }, 5000);
    }
});
