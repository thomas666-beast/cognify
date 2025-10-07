// Main JavaScript file for Cognify
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Set active menu item based on current page
    function setActiveMenu() {
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.menu-link');

        menuLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href && currentPath.startsWith(href) && href !== '/') {
                link.classList.add('active');
            }
        });

        // Special case for dashboard home
        if (currentPath === '/' || currentPath === '/dashboard/') {
            const dashboardLink = document.querySelector('a[href*="dashboard"]');
            if (dashboardLink) dashboardLink.classList.add('active');
        }
    }

    setActiveMenu();
});
