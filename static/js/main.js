// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-bs-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggle.addEventListener('click', function() {
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'bi bi-sun-fill';
    } else {
        icon.className = 'bi bi-moon-fill';
    }
}

// Watchlist Navigation
document.getElementById('watchlistNav').addEventListener('click', function(e) {
    e.preventDefault();
    loadWatchlistModal();
});

function loadWatchlistModal() {
    fetch('/api/watchlist')
        .then(res => res.json())
        .then(data => {
            showWatchlistModal(data);
        });
}

function showWatchlistModal(items) {
    const modalHtml = `
        <div class="modal fade" id="watchlistModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-bookmark-fill"></i> Your Watchlist
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${items.length === 0 ? 
                            '<p class="text-center text-muted">Your watchlist is empty. Start tracking products!</p>' :
                            generateWatchlistHTML(items)
                        }
                    </div>
                    <div class="modal-footer">
                        ${items.length > 0 ? 
                            '<a href="/export/pdf?type=watchlist" class="btn btn-primary"><i class="bi bi-file-pdf"></i> Export to PDF</a>' : 
                            ''
                        }
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('watchlistModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('watchlistModal'));
    modal.show();
}

function generateWatchlistHTML(items) {
    let html = '<div class="list-group">';
    
    items.forEach(item => {
        const discount = item.original_price ? 
            Math.round(((item.original_price - item.current_price) / item.original_price) * 100) : 0;
        
        html += `
            <div class="list-group-item">
                <div class="row align-items-center">
                    <div class="col-md-2">
                        <img src="${item.image_url}" class="img-fluid rounded" alt="${item.product_name}">
                    </div>
                    <div class="col-md-6">
                        <h6>${item.product_name}</h6>
                        <span class="badge marketplace-${item.marketplace.toLowerCase()}">${item.marketplace}</span>
                    </div>
                    <div class="col-md-3 text-end">
                        <div class="fw-bold text-success fs-5">$${item.current_price.toFixed(2)}</div>
                        ${item.original_price ? 
                            `<small class="text-muted text-decoration-line-through">$${item.original_price.toFixed(2)}</small>` : 
                            ''
                        }
                    </div>
                    <div class="col-md-1">
                        <button class="btn btn-sm btn-danger remove-watchlist" data-product-id="${item.product_id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Add event listeners after modal is shown
    setTimeout(() => {
        document.querySelectorAll('.remove-watchlist').forEach(btn => {
            btn.addEventListener('click', function() {
                removeFromWatchlist(this.dataset.productId);
            });
        });
    }, 100);
    
    return html;
}

function removeFromWatchlist(productId) {
    fetch('/api/watchlist/remove', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({product_id: productId})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadWatchlistModal();
            
            // Update watchlist buttons on the page
            document.querySelectorAll(`.watchlist-btn[data-product-id="${productId}"]`).forEach(btn => {
                btn.dataset.inWatchlist = 'False';
                btn.innerHTML = '<i class="bi bi-bookmark"></i> Track Price';
                btn.classList.remove('btn-danger');
                btn.classList.add('btn-outline-primary');
            });
        }
    });
}

// Toast notification helper
function showToast(message, type = 'success') {
    const toastHtml = `
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.querySelector('.toast:last-child');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove after hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.parentElement.remove();
    });
}
