// PropertyScope - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation to buttons on click
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.closest('form')) {
                const originalText = this.innerHTML;
                if (!this.disabled) {
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                        this.disabled = true;
                    }, 100);
                }
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Add animation to cards when they come into view
    const observeCards = () => {
        const cards = document.querySelectorAll('.card, .feature-card, .analysis-category');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    };

    // Initialize card animations
    observeCards();

    // Add counter animation for number displays
    const animateCounters = () => {
        const counters = document.querySelectorAll('.card-body h3');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const text = counter.textContent;
                    const numberMatch = text.match(/[\d,]+/);
                    
                    if (numberMatch) {
                        const finalNumber = parseInt(numberMatch[0].replace(/,/g, ''));
                        const prefix = text.substring(0, text.indexOf(numberMatch[0]));
                        const suffix = text.substring(text.indexOf(numberMatch[0]) + numberMatch[0].length);
                        
                        let currentNumber = 0;
                        const increment = finalNumber / 50;
                        const timer = setInterval(() => {
                            currentNumber += increment;
                            if (currentNumber >= finalNumber) {
                                currentNumber = finalNumber;
                                clearInterval(timer);
                            }
                            counter.textContent = prefix + Math.floor(currentNumber).toLocaleString() + suffix;
                        }, 50);
                    }
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    };

    // Initialize counter animations
    if (document.querySelector('.card-body h3')) {
        animateCounters();
    }

    // Progress bar animation
    const animateProgressBars = () => {
        const progressBars = document.querySelectorAll('.progress-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const width = progressBar.style.width;
                    progressBar.style.width = '0%';
                    
                    setTimeout(() => {
                        progressBar.style.width = width;
                    }, 200);
                    
                    observer.unobserve(progressBar);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => observer.observe(bar));
    };

    // Initialize progress bar animations
    animateProgressBars();

    // Add hover effects to issue items
    document.querySelectorAll('.issue-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.borderLeft = '4px solid #007bff';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.borderLeft = '1px solid #dee2e6';
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Show error message
                const errorMsg = form.querySelector('.error-message') || document.createElement('div');
                errorMsg.className = 'alert alert-danger error-message mt-3';
                errorMsg.textContent = 'Please fill in all required fields.';
                if (!form.querySelector('.error-message')) {
                    form.appendChild(errorMsg);
                }
                
                setTimeout(() => {
                    errorMsg.remove();
                }, 3000);
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });

    // Add search functionality for issues (if needed)
    const searchInput = document.querySelector('#issueSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const issueItems = document.querySelectorAll('.issue-item');
            
            issueItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});

// Utility Functions
const PropertyScope = {
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },

    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    },

    // Copy text to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Copied to clipboard!', 'success');
        }).catch(() => {
            this.showNotification('Failed to copy to clipboard', 'danger');
        });
    },

    // Share results
    shareResults: function(url) {
        if (navigator.share) {
            navigator.share({
                title: 'Property Analysis Results - PropertyScope',
                text: 'Check out this property analysis report',
                url: url
            });
        } else {
            this.copyToClipboard(url);
        }
    }
};

// Make PropertyScope globally available
window.PropertyScope = PropertyScope;