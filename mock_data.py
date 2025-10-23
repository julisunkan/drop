import random
from datetime import datetime, timedelta

# Mock marketplace data
MOCK_PRODUCTS = [
    {
        "id": "amz_001",
        "name": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones",
        "marketplace": "Amazon",
        "price": 348.00,
        "original_price": 399.99,
        "discount": 13,
        "image": "https://m.media-amazon.com/images/I/61vFO3CCBCL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 12453,
        "delivery_days": 2,
        "description": "Industry-leading noise cancellation with premium sound quality and 30-hour battery life."
    },
    {
        "id": "amz_ps5",
        "name": "PlayStation 5 Console (PS5) - Digital Edition",
        "marketplace": "Amazon",
        "price": 449.99,
        "original_price": 499.99,
        "discount": 10,
        "image": "https://m.media-amazon.com/images/I/51JqjP3KzWL._SL1024_.jpg",
        "url": "https://www.amazon.com/PlayStation-5-Console/dp/B0BCNKKZ91",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 28432,
        "delivery_days": 2,
        "description": "Experience lightning-fast loading with ultra-high speed SSD, stunning graphics with 4K gaming, and immersive haptic feedback."
    },
    {
        "id": "ebay_ps5",
        "name": "Sony PlayStation 5 PS5 Disc Version Gaming Console",
        "marketplace": "eBay",
        "price": 479.99,
        "original_price": 549.99,
        "discount": 13,
        "image": "https://m.media-amazon.com/images/I/51JqjP3KzWL._SL1024_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=playstation+5+console",
        "free_shipping": False,
        "rating": 4.7,
        "reviews": 5421,
        "delivery_days": 4,
        "description": "PS5 with disc drive - play both physical and digital games. Includes DualSense wireless controller."
    },
    {
        "id": "amz_desktop",
        "name": "HP Desktop Computer, Intel Core i7, 16GB RAM, 512GB SSD",
        "marketplace": "Amazon",
        "price": 649.99,
        "original_price": 899.99,
        "discount": 28,
        "image": "https://m.media-amazon.com/images/I/71h-vHSRmJL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/HP-Desktop-Computer-i7-Windows/dp/B0C1JK7PQP",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 3245,
        "delivery_days": 3,
        "description": "Powerful desktop computer with Intel Core i7 processor, 16GB RAM, 512GB SSD storage. Perfect for work and entertainment."
    },
    {
        "id": "ali_computer",
        "name": "Gaming Desktop PC Computer Intel i5, 32GB RAM, RTX 3060",
        "marketplace": "AliExpress",
        "price": 799.99,
        "original_price": 1299.99,
        "discount": 38,
        "image": "https://m.media-amazon.com/images/I/71R7qZ3EJPL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-gaming-desktop-computer.html",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 1876,
        "delivery_days": 15,
        "description": "High-performance gaming computer with RGB lighting, Intel i5 processor, 32GB RAM, and NVIDIA RTX 3060 graphics card."
    },
    {
        "id": "ali_001",
        "name": "Sony WH-1000XM4 Wireless Headphones (Similar)",
        "marketplace": "AliExpress",
        "price": 289.99,
        "original_price": 349.99,
        "discount": 17,
        "image": "https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-sony-wireless-headphones.html",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 3421,
        "delivery_days": 15,
        "description": "Premium wireless headphones with active noise cancellation. Great battery life and comfort for extended listening sessions."
    },
    {
        "id": "ebay_001",
        "name": "Sony WH-1000XM5 Headphones - Certified Refurbished",
        "marketplace": "eBay",
        "price": 299.99,
        "original_price": 399.99,
        "discount": 25,
        "image": "https://m.media-amazon.com/images/I/61vFO3XUFtL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=Sony+WH-1000XM5+refurbished",
        "free_shipping": False,
        "rating": 4.6,
        "reviews": 892,
        "delivery_days": 5,
        "description": "Certified refurbished Sony headphones with 90-day warranty. Tested and verified to work like new."
    },
    {
        "id": "amz_002",
        "name": "Apple iPhone 15 Pro Max 256GB",
        "marketplace": "Amazon",
        "price": 1099.99,
        "original_price": 1199.99,
        "discount": 8,
        "image": "https://m.media-amazon.com/images/I/81SigpJN1KL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=Apple+iPhone+15+Pro+Max+256GB",
        "free_shipping": True,
        "rating": 4.9,
        "reviews": 8765,
        "delivery_days": 1,
        "description": "Latest iPhone with A17 Pro chip, titanium design, and advanced camera system. 256GB storage."
    },
    {
        "id": "temu_001",
        "name": "iPhone 15 Pro Max Case with Screen Protector",
        "marketplace": "Temu",
        "price": 8.99,
        "original_price": 29.99,
        "discount": 70,
        "image": "https://m.media-amazon.com/images/I/71yzONA87BL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=iphone+15+pro+max+case",
        "free_shipping": True,
        "rating": 4.2,
        "reviews": 5432,
        "delivery_days": 10,
        "description": "Protective case for iPhone 15 Pro Max with tempered glass screen protector included."
    },
    {
        "id": "jumia_001",
        "name": "Samsung Galaxy S24 Ultra 512GB",
        "marketplace": "Jumia",
        "price": 1049.99,
        "original_price": 1299.99,
        "discount": 19,
        "image": "https://m.media-amazon.com/images/I/71lD7eGdW-L._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=Samsung+Galaxy+S24+Ultra",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 2341,
        "delivery_days": 3,
        "description": "Premium Samsung flagship with S Pen, 200MP camera, and AI-powered features. 512GB storage."
    },
    {
        "id": "amz_003",
        "name": "MacBook Air M3 15-inch 16GB 512GB",
        "marketplace": "Amazon",
        "price": 1449.99,
        "original_price": 1599.99,
        "discount": 9,
        "image": "https://m.media-amazon.com/images/I/71f5Eu5lJNL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=MacBook+Air+M3+15+inch",
        "free_shipping": True,
        "rating": 4.9,
        "reviews": 4521,
        "delivery_days": 2,
        "description": "Latest MacBook Air with M3 chip. Perfect for professionals and students. All-day battery life."
    },
    {
        "id": "ali_002",
        "name": "Mechanical Gaming Keyboard RGB Hot-Swappable",
        "marketplace": "AliExpress",
        "price": 59.99,
        "original_price": 129.99,
        "discount": 54,
        "image": "https://m.media-amazon.com/images/I/61rthTT3+NL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-mechanical-gaming-keyboard-rgb.html",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 9876,
        "delivery_days": 12,
        "description": "Customizable mechanical keyboard with hot-swappable switches and RGB backlighting."
    },
    {
        "id": "temu_002",
        "name": "Wireless Gaming Mouse 16000 DPI RGB",
        "marketplace": "Temu",
        "price": 19.99,
        "original_price": 59.99,
        "discount": 67,
        "image": "https://m.media-amazon.com/images/I/61MPEgAHshL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=wireless+gaming+mouse+rgb",
        "free_shipping": True,
        "rating": 4.3,
        "reviews": 6754,
        "delivery_days": 8,
        "description": "High-precision wireless gaming mouse with customizable DPI settings and RGB lighting."
    },
    {
        "id": "ebay_002",
        "name": "Dell UltraSharp 27\" 4K Monitor",
        "marketplace": "eBay",
        "price": 449.99,
        "original_price": 699.99,
        "discount": 36,
        "image": "https://m.media-amazon.com/images/I/81Y98yS+MYL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=Dell+UltraSharp+27+4K+Monitor",
        "free_shipping": False,
        "rating": 4.7,
        "reviews": 1234,
        "delivery_days": 4,
        "description": "Professional 4K monitor with excellent color accuracy. Perfect for creative work."
    },
    {
        "id": "amz_004",
        "name": "Logitech MX Master 3S Wireless Mouse",
        "marketplace": "Amazon",
        "price": 89.99,
        "original_price": 99.99,
        "discount": 10,
        "image": "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=Logitech+MX+Master+3S",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 7654,
        "delivery_days": 1,
        "description": "Premium wireless mouse designed for productivity. Ergonomic design with customizable buttons."
    },
    {
        "id": "jumia_002",
        "name": "HP Pavilion Gaming Laptop RTX 4060 16GB",
        "marketplace": "Jumia",
        "price": 899.99,
        "original_price": 1199.99,
        "discount": 25,
        "image": "https://m.media-amazon.com/images/I/81bc8mA3nKL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=HP+Pavilion+Gaming+Laptop",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 876,
        "delivery_days": 3,
        "description": "Powerful gaming laptop with RTX 4060 graphics card. 16GB RAM and 512GB SSD."
    }
]

def search_products(query, filters=None):
    """Search products based on query and filters"""
    query_lower = query.lower()
    results = []

    for product in MOCK_PRODUCTS:
        if query_lower in product['name'].lower() or query_lower in product['description'].lower():
            results.append(product.copy())

    # Apply filters
    if filters:
        if filters.get('free_shipping'):
            results = [p for p in results if p['free_shipping']]

        if filters.get('discount_only'):
            results = [p for p in results if p['discount'] > 0]

        if filters.get('marketplace'):
            marketplace = filters['marketplace']
            if marketplace != 'all':
                results = [p for p in results if p['marketplace'] == marketplace]

    # Sort results
    sort_by = filters.get('sort_by', 'relevance') if filters else 'relevance'
    if sort_by == 'price_low':
        results.sort(key=lambda x: x['price'])
    elif sort_by == 'price_high':
        results.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'discount':
        results.sort(key=lambda x: x['discount'], reverse=True)
    elif sort_by == 'delivery':
        results.sort(key=lambda x: x['delivery_days'])

    return results

def get_product_by_id(product_id):
    """Get a single product by ID"""
    for product in MOCK_PRODUCTS:
        if product['id'] == product_id:
            return product.copy()
    return None

def generate_price_history(current_price, days=30):
    """Generate realistic price history for visualization"""
    history = []
    base_price = current_price * 1.1  # Start slightly higher

    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        # Add some random variation
        variation = random.uniform(-0.05, 0.05)
        price = base_price * (1 + variation)

        # Occasional drops
        if random.random() < 0.15:
            price = price * random.uniform(0.85, 0.95)

        # Trend towards current price
        price = price * (1 - (i / days) * 0.1)

        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(price, 2)
        })

    # Ensure last price is current price
    history[-1]['price'] = current_price

    return history