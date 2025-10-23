import random
from datetime import datetime, timedelta

# Mock marketplace data
MOCK_PRODUCTS = [
    {
        "id": "amz_001",
        "name": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones",
        "marketplace": "Amazon",
        "price": 349.99,
        "original_price": 399.99,
        "discount": 13,
        "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400&h=400&fit=crop",
        "url": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 12543,
        "delivery_days": 2,
        "description": "Industry-leading noise cancellation with premium sound quality. 30-hour battery life, multipoint connection, and speak-to-chat technology."
    },
    {
        "id": "ali_001",
        "name": "Sony WH-1000XM4 Wireless Headphones (Similar)",
        "marketplace": "AliExpress",
        "price": 289.99,
        "original_price": 349.99,
        "discount": 17,
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=400&fit=crop",
        "url": "https://www.aliexpress.com/item/sony-headphones.html",
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
        "image": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop",
        "url": "https://www.ebay.com/itm/sony-wh1000xm5-refurbished",
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
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
        "url": "https://www.amazon.com/Apple-iPhone-15-Pro-Max/dp/B0CHX1W1XY",
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
        "image": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=400&fit=crop",
        "url": "https://www.temu.com/iphone-case-screen-protector.html",
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
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop",
        "url": "https://www.jumia.com/samsung-galaxy-s24-ultra",
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
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop",
        "url": "https://www.amazon.com/Apple-MacBook-Air-15-inch-M3/dp/B0CX23GFMJD",
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
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop",
        "url": "https://www.aliexpress.com/item/mechanical-keyboard-rgb.html",
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
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
        "url": "https://www.temu.com/wireless-gaming-mouse-rgb.html",
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
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop",
        "url": "https://www.ebay.com/itm/dell-ultrasharp-4k-monitor",
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
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400&h=400&fit=crop",
        "url": "https://www.amazon.com/Logitech-MX-Master-3S-Wireless/dp/B09HM94VDS",
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
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop",
        "url": "https://www.jumia.com/hp-pavilion-gaming-laptop",
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
