// Modern Profile Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Navigation
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const contentSections = document.querySelectorAll('.content-section');

    sidebarItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            sidebarItems.forEach(link => link.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding content section
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Filter Tabs
    const filterTabs = document.querySelectorAll('.filter-tab');
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            filterTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Here you would typically filter the bookings based on the selected tab
            // This would require backend integration
        });
    });

    // Mobile Menu Toggle (if needed)
    const menuToggle = document.querySelector('.menu-toggle');
    const navbar = document.querySelector('#navbar');
    
    if (menuToggle && navbar) {
        menuToggle.addEventListener('click', function() {
            navbar.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (!this.classList.contains('sidebar-item')) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Initialize login notification
    const bookButtons = document.querySelectorAll('.book-btn');
    bookButtons.forEach(button => {
        if (button.tagName === 'BUTTON') {
            button.addEventListener('click', showLoginNotification);
        }
    });
    
    // Close button for login notification
    const closeButton = document.querySelector('.close-notification');
    if (closeButton) {
        closeButton.addEventListener('click', closeLoginNotification);
    }
});

// Login Notification Functions
function showLoginNotification() {
    const notification = document.getElementById('loginNotification');
    if (notification) {
        notification.classList.add('show');
        
        // Auto hide after 10 seconds
        setTimeout(function() {
            closeLoginNotification();
        }, 10000);
    }
}

function closeLoginNotification() {
    const notification = document.getElementById('loginNotification');
    if (notification) {
        notification.classList.remove('show');
    }
} 