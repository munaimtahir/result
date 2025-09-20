// University Result Portal - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancements
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Loading state for form submissions
    var submitButtons = document.querySelectorAll('input[type="submit"], button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var form = button.closest('form');
            if (form && form.checkValidity()) {
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
                button.disabled = true;
            }
        });
    });

    // Table search functionality
    function initTableSearch() {
        var searchInputs = document.querySelectorAll('[data-table-search]');
        searchInputs.forEach(function(input) {
            var tableId = input.getAttribute('data-table-search');
            var table = document.getElementById(tableId);
            if (table) {
                input.addEventListener('keyup', function() {
                    var filter = input.value.toLowerCase();
                    var rows = table.querySelectorAll('tbody tr');
                    
                    rows.forEach(function(row) {
                        var text = row.textContent.toLowerCase();
                        if (text.includes(filter)) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    });
                });
            }
        });
    }
    initTableSearch();

    // Animate cards on scroll
    function animateOnScroll() {
        var cards = document.querySelectorAll('.card');
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(function(card) {
            observer.observe(card);
        });
    }
    animateOnScroll();

    // File upload preview
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var fileName = input.files[0] ? input.files[0].name : 'Choose file...';
            var label = input.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                label.textContent = fileName;
            }
        });
    });

    // Confirmation dialogs for delete actions
    var deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = button.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-resize textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        });
    });

    // Print functionality
    function initPrint() {
        var printButtons = document.querySelectorAll('[data-print]');
        printButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                window.print();
            });
        });
    }
    initPrint();

    // Copy to clipboard functionality
    function initClipboard() {
        var copyButtons = document.querySelectorAll('[data-clipboard]');
        copyButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var text = button.getAttribute('data-clipboard');
                navigator.clipboard.writeText(text).then(function() {
                    // Show success message
                    var originalText = button.textContent;
                    button.textContent = 'Copied!';
                    setTimeout(function() {
                        button.textContent = originalText;
                    }, 2000);
                });
            });
        });
    }
    initClipboard();
});

// Utility functions
function showToast(message, type = 'info') {
    // Create toast element
    var toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(function() {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Export for use in other scripts
window.ResultPortal = {
    showToast: showToast,
    formatNumber: formatNumber,
    formatDate: formatDate
};