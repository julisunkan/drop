// Watchlist functionality
document.querySelectorAll('.watchlist-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const productId = this.dataset.productId;
        const inWatchlist = this.dataset.inWatchlist === 'True';
        
        if (inWatchlist) {
            // Remove from watchlist
            fetch('/api/watchlist/remove', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: productId})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.dataset.inWatchlist = 'False';
                    this.innerHTML = '<i class="bi bi-bookmark"></i> Track Price';
                    showToast('Removed from watchlist', 'info');
                    
                    // Update all buttons for this product
                    document.querySelectorAll(`.watchlist-btn[data-product-id="${productId}"]`).forEach(b => {
                        b.dataset.inWatchlist = 'False';
                        b.innerHTML = '<i class="bi bi-bookmark"></i> Track Price';
                    });
                }
            });
        } else {
            // Add to watchlist
            fetch('/api/watchlist/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    product_id: productId,
                    product_name: this.dataset.productName,
                    marketplace: this.dataset.marketplace,
                    current_price: parseFloat(this.dataset.price),
                    original_price: this.dataset.originalPrice ? parseFloat(this.dataset.originalPrice) : null,
                    image_url: this.dataset.image,
                    product_url: '#'
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.dataset.inWatchlist = 'True';
                    this.innerHTML = '<i class="bi bi-bookmark-fill"></i> In Watchlist';
                    showToast('Added to watchlist! We\'ll track price changes for you.', 'success');
                    
                    // Update all buttons for this product
                    document.querySelectorAll(`.watchlist-btn[data-product-id="${productId}"]`).forEach(b => {
                        b.dataset.inWatchlist = 'True';
                        b.innerHTML = '<i class="bi bi-bookmark-fill"></i> In Watchlist';
                    });
                } else {
                    showToast('Product already in watchlist', 'info');
                }
            });
        }
    });
});

// Product comparison
const compareCheckboxes = [];
const compareBar = document.getElementById('compareBar');
const compareBtn = document.getElementById('compareBtn');
const compareCount = document.getElementById('compareCount');

document.querySelectorAll('.compare-label').forEach((label, index) => {
    const productId = label.previousElementSibling.value;
    
    label.addEventListener('click', function(e) {
        e.preventDefault();
        const checkbox = this.previousElementSibling;
        checkbox.checked = !checkbox.checked;
        
        if (checkbox.checked) {
            this.classList.add('active');
            if (!compareCheckboxes.includes(productId)) {
                compareCheckboxes.push(productId);
            }
        } else {
            this.classList.remove('active');
            const idx = compareCheckboxes.indexOf(productId);
            if (idx > -1) {
                compareCheckboxes.splice(idx, 1);
            }
        }
        
        updateCompareBar();
    });
});

function updateCompareBar() {
    if (compareCheckboxes.length > 0) {
        compareBar.style.display = 'block';
        compareCount.textContent = `${compareCheckboxes.length} product${compareCheckboxes.length > 1 ? 's' : ''} selected`;
    } else {
        compareBar.style.display = 'none';
    }
}

if (compareBtn) {
    compareBtn.addEventListener('click', function() {
        if (compareCheckboxes.length < 2) {
            showToast('Please select at least 2 products to compare', 'warning');
            return;
        }
        
        if (compareCheckboxes.length > 4) {
            showToast('You can compare up to 4 products at once', 'warning');
            return;
        }
        
        const url = '/compare?' + compareCheckboxes.map(id => `products=${id}`).join('&');
        window.location.href = url;
    });
}
