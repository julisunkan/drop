import random
from datetime import datetime, timedelta
import hashlib
import requests
from functools import lru_cache

def generate_product_image(product_name):
    """Generate a placeholder image URL based on product name"""
    # Use a hash of the product name to generate a consistent color
    hash_obj = hashlib.md5(product_name.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Create a demo placeholder image with the product name
    # Using placehold.co which is a reliable placeholder service
    encoded_name = product_name[:30].replace(' ', '%20')
    # Return a reliable placeholder service URL with background and text color
    return f"https://placehold.co/400x400/{hash_hex[0:6]}/ffffff?text={encoded_name}"

@lru_cache(maxsize=500)
def validate_image_url(url, timeout=3):
    """Validate if an image URL is accessible. Cached to avoid repeated requests."""
    if not url or url == '':
        return False
    
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        # Check if status is OK and content-type is an image
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            return 'image' in content_type or response.status_code == 200
        return False
    except (requests.RequestException, Exception):
        return False

def get_validated_image(image_url, fallback_name):
    """Get validated image URL or generate fallback"""
    # Always return a valid image - either the original if it works, or a demo image
    if image_url and validate_image_url(image_url):
        return image_url
    else:
        # Use placehold.co for demo images when validation fails or URL is empty
        return generate_product_image(fallback_name)

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
    },
    {
        "id": "temu_003",
        "name": "Smart Watch Fitness Tracker Heart Rate Monitor",
        "marketplace": "Temu",
        "price": 29.99,
        "original_price": 99.99,
        "discount": 70,
        "image": "https://m.media-amazon.com/images/I/61ZjlKh7SQL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=smart+watch+fitness",
        "free_shipping": True,
        "rating": 4.3,
        "reviews": 8932,
        "delivery_days": 12,
        "description": "Track your fitness goals with heart rate monitoring, step counter, and sleep tracking."
    },
    {
        "id": "amz_005",
        "name": "Samsung 65-inch 4K Smart TV QLED",
        "marketplace": "Amazon",
        "price": 1299.99,
        "original_price": 1799.99,
        "discount": 28,
        "image": "https://m.media-amazon.com/images/I/81fhyKQu0sL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=Samsung+65+inch+QLED+TV",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 6543,
        "delivery_days": 2,
        "description": "Stunning 4K QLED display with smart features and voice control."
    },
    {
        "id": "ebay_003",
        "name": "Nintendo Switch OLED Console Bundle",
        "marketplace": "eBay",
        "price": 349.99,
        "original_price": 449.99,
        "discount": 22,
        "image": "https://m.media-amazon.com/images/I/61YtEUkt4FL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=nintendo+switch+oled",
        "free_shipping": True,
        "rating": 4.9,
        "reviews": 4321,
        "delivery_days": 3,
        "description": "Nintendo Switch with vibrant OLED screen. Includes 2 games and carrying case."
    },
    {
        "id": "ali_003",
        "name": "Webcam 1080P HD with Microphone for Streaming",
        "marketplace": "AliExpress",
        "price": 39.99,
        "original_price": 89.99,
        "discount": 56,
        "image": "https://m.media-amazon.com/images/I/61wkxbe6NFL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-1080p-webcam.html",
        "free_shipping": True,
        "rating": 4.4,
        "reviews": 7654,
        "delivery_days": 14,
        "description": "HD webcam perfect for video calls, streaming, and online meetings."
    },
    {
        "id": "amz_006",
        "name": "Bose QuietComfort 45 Wireless Headphones",
        "marketplace": "Amazon",
        "price": 279.00,
        "original_price": 329.00,
        "discount": 15,
        "image": "https://m.media-amazon.com/images/I/51MRYCdk6lL._AC_SL1000_.jpg",
        "url": "https://www.amazon.com/s?k=Bose+QuietComfort+45",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 9876,
        "delivery_days": 1,
        "description": "Premium noise-cancelling headphones with exceptional comfort and sound quality."
    },
    {
        "id": "temu_004",
        "name": "USB LED Strip Lights 16.4ft RGB Color Changing",
        "marketplace": "Temu",
        "price": 12.99,
        "original_price": 39.99,
        "discount": 68,
        "image": "https://m.media-amazon.com/images/I/71EhHW+JJPL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=led+strip+lights",
        "free_shipping": True,
        "rating": 4.2,
        "reviews": 12345,
        "delivery_days": 9,
        "description": "Colorful LED strip lights with remote control. Perfect for room decoration."
    },
    {
        "id": "jumia_003",
        "name": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
        "marketplace": "Jumia",
        "price": 89.99,
        "original_price": 129.99,
        "discount": 31,
        "image": "https://m.media-amazon.com/images/I/71Yfv3KQ9XL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=instant+pot",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 23456,
        "delivery_days": 4,
        "description": "Multi-functional pressure cooker that replaces 7 kitchen appliances."
    },
    {
        "id": "ebay_004",
        "name": "Canon EOS Rebel T7 DSLR Camera with Lens Kit",
        "marketplace": "eBay",
        "price": 549.99,
        "original_price": 749.99,
        "discount": 27,
        "image": "https://m.media-amazon.com/images/I/71EWRyqzw0L._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=canon+eos+rebel+t7",
        "free_shipping": False,
        "rating": 4.7,
        "reviews": 3456,
        "delivery_days": 5,
        "description": "Entry-level DSLR camera perfect for beginners. Includes 18-55mm lens."
    },
    {
        "id": "ali_004",
        "name": "Bluetooth Speaker Portable Waterproof 20W",
        "marketplace": "AliExpress",
        "price": 34.99,
        "original_price": 79.99,
        "discount": 56,
        "image": "https://m.media-amazon.com/images/I/71PW1NsCqrL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-bluetooth-speaker-waterproof.html",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 5678,
        "delivery_days": 13,
        "description": "Powerful portable speaker with deep bass and 12-hour battery life."
    },
    {
        "id": "amz_007",
        "name": "Ring Video Doorbell Pro 2",
        "marketplace": "Amazon",
        "price": 229.99,
        "original_price": 279.99,
        "discount": 18,
        "image": "https://m.media-amazon.com/images/I/51hP0R9f7qL._AC_SL1000_.jpg",
        "url": "https://www.amazon.com/s?k=ring+doorbell+pro+2",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 8765,
        "delivery_days": 2,
        "description": "Smart doorbell with HD video, motion detection, and two-way audio."
    },
    {
        "id": "temu_005",
        "name": "Ergonomic Office Chair with Lumbar Support",
        "marketplace": "Temu",
        "price": 129.99,
        "original_price": 299.99,
        "discount": 57,
        "image": "https://m.media-amazon.com/images/I/71Z1w0x5WfL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=ergonomic+office+chair",
        "free_shipping": True,
        "rating": 4.4,
        "reviews": 4567,
        "delivery_days": 11,
        "description": "Comfortable office chair with adjustable armrests and breathable mesh back."
    },
    {
        "id": "jumia_004",
        "name": "Dyson V11 Cordless Vacuum Cleaner",
        "marketplace": "Jumia",
        "price": 499.99,
        "original_price": 699.99,
        "discount": 29,
        "image": "https://m.media-amazon.com/images/I/61J9BmCCJxL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=dyson+vacuum",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 3456,
        "delivery_days": 3,
        "description": "Powerful cordless vacuum with intelligent suction and long battery life."
    },
    {
        "id": "ebay_005",
        "name": "GoPro HERO11 Black Action Camera",
        "marketplace": "eBay",
        "price": 399.99,
        "original_price": 499.99,
        "discount": 20,
        "image": "https://m.media-amazon.com/images/I/61CJWyLM2vL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=gopro+hero11+black",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 2345,
        "delivery_days": 4,
        "description": "5.3K video action camera with waterproof design and image stabilization."
    },
    {
        "id": "ali_005",
        "name": "Electric Standing Desk Adjustable Height",
        "marketplace": "AliExpress",
        "price": 299.99,
        "original_price": 599.99,
        "discount": 50,
        "image": "https://m.media-amazon.com/images/I/71H8t1cW5KL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-standing-desk-electric.html",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 1234,
        "delivery_days": 16,
        "description": "Electric standing desk with memory presets and sturdy steel frame."
    },
    {
        "id": "amz_008",
        "name": "Kindle Paperwhite Signature Edition",
        "marketplace": "Amazon",
        "price": 139.99,
        "original_price": 189.99,
        "discount": 26,
        "image": "https://m.media-amazon.com/images/I/51QCk82iGsL._AC_SL1000_.jpg",
        "url": "https://www.amazon.com/s?k=kindle+paperwhite+signature",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 15678,
        "delivery_days": 1,
        "description": "Premium e-reader with adjustable warm light and wireless charging."
    },
    {
        "id": "temu_006",
        "name": "Air Fryer 6 Quart Digital Touch Screen",
        "marketplace": "Temu",
        "price": 59.99,
        "original_price": 149.99,
        "discount": 60,
        "image": "https://m.media-amazon.com/images/I/71OQBm7u8tL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=air+fryer",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 9876,
        "delivery_days": 10,
        "description": "Large capacity air fryer with 8 preset cooking programs and easy cleanup."
    },
    {
        "id": "jumia_005",
        "name": "Nespresso Coffee Machine with Milk Frother",
        "marketplace": "Jumia",
        "price": 179.99,
        "original_price": 249.99,
        "discount": 28,
        "image": "https://m.media-amazon.com/images/I/71i1Z0MJNSL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=nespresso+coffee+machine",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 4321,
        "delivery_days": 3,
        "description": "Premium coffee machine with automatic milk frother for perfect cappuccinos."
    },
    {
        "id": "ebay_006",
        "name": "Xbox Series S Console 512GB",
        "marketplace": "eBay",
        "price": 279.99,
        "original_price": 349.99,
        "discount": 20,
        "image": "https://m.media-amazon.com/images/I/61M-a0F58qL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=xbox+series+s",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 6789,
        "delivery_days": 3,
        "description": "Compact next-gen gaming console with fast load times and 1440p gaming."
    },
    {
        "id": "ali_006",
        "name": "Robot Vacuum Cleaner with Mopping Function",
        "marketplace": "AliExpress",
        "price": 199.99,
        "original_price": 449.99,
        "discount": 56,
        "image": "https://m.media-amazon.com/images/I/61aDHH5pLjL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-robot-vacuum-mop.html",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 8765,
        "delivery_days": 15,
        "description": "Smart robot vacuum with automatic mopping and app control."
    },
    {
        "id": "amz_009",
        "name": "Apple AirPods Pro 2nd Generation",
        "marketplace": "Amazon",
        "price": 199.99,
        "original_price": 249.99,
        "discount": 20,
        "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=airpods+pro+2nd+generation",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 34567,
        "delivery_days": 1,
        "description": "Active noise cancellation with adaptive transparency and spatial audio."
    },
    {
        "id": "temu_007",
        "name": "Portable Power Station 300W Solar Generator",
        "marketplace": "Temu",
        "price": 179.99,
        "original_price": 399.99,
        "discount": 55,
        "image": "https://m.media-amazon.com/images/I/71MqXqNNW6L._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=portable+power+station",
        "free_shipping": True,
        "rating": 4.3,
        "reviews": 2345,
        "delivery_days": 12,
        "description": "Portable power station for camping and emergency backup. Multiple charging ports."
    },
    {
        "id": "jumia_006",
        "name": "LG 27-Inch UltraGear Gaming Monitor 144Hz",
        "marketplace": "Jumia",
        "price": 349.99,
        "original_price": 499.99,
        "discount": 30,
        "image": "https://m.media-amazon.com/images/I/81lUQ2kfSvL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=lg+ultragear+monitor",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 3456,
        "delivery_days": 4,
        "description": "High refresh rate gaming monitor with 1ms response time and FreeSync."
    },
    {
        "id": "ebay_007",
        "name": "DJI Mini 3 Pro Drone with 4K Camera",
        "marketplace": "eBay",
        "price": 759.99,
        "original_price": 999.99,
        "discount": 24,
        "image": "https://m.media-amazon.com/images/I/61zAjw4bqPL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=dji+mini+3+pro",
        "free_shipping": False,
        "rating": 4.9,
        "reviews": 1234,
        "delivery_days": 5,
        "description": "Compact drone with 4K HDR video and 34-minute flight time."
    },
    {
        "id": "ali_007",
        "name": "Laptop Cooling Pad RGB with 6 Fans",
        "marketplace": "AliExpress",
        "price": 29.99,
        "original_price": 69.99,
        "discount": 57,
        "image": "https://m.media-amazon.com/images/I/71zmqH9xgcL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-laptop-cooling-pad.html",
        "free_shipping": True,
        "rating": 4.4,
        "reviews": 6789,
        "delivery_days": 14,
        "description": "Powerful laptop cooling pad with RGB lighting and adjustable height."
    },
    {
        "id": "amz_010",
        "name": "Fitbit Charge 6 Fitness Tracker",
        "marketplace": "Amazon",
        "price": 139.99,
        "original_price": 179.99,
        "discount": 22,
        "image": "https://m.media-amazon.com/images/I/61S+-gKHjaL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=fitbit+charge+6",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 8765,
        "delivery_days": 2,
        "description": "Advanced fitness tracker with heart rate monitoring and GPS."
    },
    {
        "id": "temu_008",
        "name": "Electric Toothbrush with 8 Brush Heads",
        "marketplace": "Temu",
        "price": 24.99,
        "original_price": 79.99,
        "discount": 69,
        "image": "https://m.media-amazon.com/images/I/61hqJX9rr8L._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=electric+toothbrush",
        "free_shipping": True,
        "rating": 4.3,
        "reviews": 7654,
        "delivery_days": 9,
        "description": "Rechargeable electric toothbrush with multiple cleaning modes."
    },
    {
        "id": "jumia_007",
        "name": "Philips Hue Smart Lights Starter Kit",
        "marketplace": "Jumia",
        "price": 149.99,
        "original_price": 199.99,
        "discount": 25,
        "image": "https://m.media-amazon.com/images/I/61KO9+AV7HL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=philips+hue+lights",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 5432,
        "delivery_days": 3,
        "description": "Smart LED bulbs with millions of colors and voice control support."
    },
    {
        "id": "ebay_008",
        "name": "Oculus Quest 3 VR Headset 128GB",
        "marketplace": "eBay",
        "price": 479.99,
        "original_price": 599.99,
        "discount": 20,
        "image": "https://m.media-amazon.com/images/I/61kYqQ0RqHL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=oculus+quest+3",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 3456,
        "delivery_days": 4,
        "description": "Next-gen VR headset with mixed reality capabilities and powerful processor."
    },
    {
        "id": "ali_008",
        "name": "Mechanical Keyboard 60% Compact RGB Hot-Swap",
        "marketplace": "AliExpress",
        "price": 69.99,
        "original_price": 149.99,
        "discount": 53,
        "image": "https://m.media-amazon.com/images/I/71KxjJ5GLQL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-60-mechanical-keyboard.html",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 4567,
        "delivery_days": 13,
        "description": "Compact 60% mechanical keyboard with hot-swappable switches and RGB."
    },
    {
        "id": "amz_011",
        "name": "Anker PowerCore 20000mAh Portable Charger",
        "marketplace": "Amazon",
        "price": 49.99,
        "original_price": 69.99,
        "discount": 29,
        "image": "https://m.media-amazon.com/images/I/61V3l5vz5cL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=anker+powercore+20000",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 23456,
        "delivery_days": 1,
        "description": "High-capacity portable charger with fast charging for multiple devices."
    },
    {
        "id": "temu_009",
        "name": "Resistance Bands Set with Door Anchor",
        "marketplace": "Temu",
        "price": 19.99,
        "original_price": 59.99,
        "discount": 67,
        "image": "https://m.media-amazon.com/images/I/71PRscKcRpL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=resistance+bands",
        "free_shipping": True,
        "rating": 4.4,
        "reviews": 5678,
        "delivery_days": 11,
        "description": "Complete resistance band set for home workouts with carrying bag."
    },
    {
        "id": "jumia_008",
        "name": "Ninja Foodi 11-in-1 SmartLid Multi-Cooker",
        "marketplace": "Jumia",
        "price": 249.99,
        "original_price": 349.99,
        "discount": 29,
        "image": "https://m.media-amazon.com/images/I/71CbqHdQSFL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=ninja+foodi+multi+cooker",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 6789,
        "delivery_days": 3,
        "description": "Versatile multi-cooker with pressure cooking, air frying, and more."
    },
    {
        "id": "ebay_009",
        "name": "Razer DeathAdder V3 Pro Wireless Gaming Mouse",
        "marketplace": "eBay",
        "price": 129.99,
        "original_price": 179.99,
        "discount": 28,
        "image": "https://m.media-amazon.com/images/I/51O6ECSL6NL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=razer+deathadder+v3+pro",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 2345,
        "delivery_days": 4,
        "description": "Professional wireless gaming mouse with 30K DPI sensor and 90-hour battery."
    },
    {
        "id": "ali_009",
        "name": "Studio Microphone USB Condenser with Stand",
        "marketplace": "AliExpress",
        "price": 44.99,
        "original_price": 99.99,
        "discount": 55,
        "image": "https://m.media-amazon.com/images/I/61Mu1EgHJYL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-usb-condenser-microphone.html",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 7890,
        "delivery_days": 14,
        "description": "Professional USB microphone for podcasting, streaming, and recording."
    },
    {
        "id": "amz_012",
        "name": "ASUS ROG Strix Gaming Laptop RTX 4070 32GB",
        "marketplace": "Amazon",
        "price": 1799.99,
        "original_price": 2299.99,
        "discount": 22,
        "image": "https://m.media-amazon.com/images/I/81bc8mA3nKL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=asus+rog+strix+rtx+4070",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 1234,
        "delivery_days": 2,
        "description": "High-performance gaming laptop with RTX 4070, 32GB RAM, and 1TB SSD."
    },
    {
        "id": "temu_010",
        "name": "Wireless Earbuds with Charging Case",
        "marketplace": "Temu",
        "price": 24.99,
        "original_price": 79.99,
        "discount": 69,
        "image": "https://m.media-amazon.com/images/I/61GsPIkVqNL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=wireless+earbuds",
        "free_shipping": True,
        "rating": 4.2,
        "reviews": 9876,
        "delivery_days": 10,
        "description": "True wireless earbuds with touch controls and 24-hour battery life."
    },
    {
        "id": "jumia_009",
        "name": "Keurig K-Elite Coffee Maker Single Serve",
        "marketplace": "Jumia",
        "price": 139.99,
        "original_price": 189.99,
        "discount": 26,
        "image": "https://m.media-amazon.com/images/I/71Pnk7kmC3L._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=keurig+coffee+maker",
        "free_shipping": True,
        "rating": 4.6,
        "reviews": 12345,
        "delivery_days": 3,
        "description": "Single-serve coffee maker with multiple cup sizes and iced coffee option."
    },
    {
        "id": "ebay_010",
        "name": "Apple iPad 10th Generation 64GB WiFi",
        "marketplace": "eBay",
        "price": 329.99,
        "original_price": 449.99,
        "discount": 27,
        "image": "https://m.media-amazon.com/images/I/61NGnpjoRDL._AC_SL1500_.jpg",
        "url": "https://www.ebay.com/sch/i.html?_nkw=ipad+10th+generation",
        "free_shipping": True,
        "rating": 4.8,
        "reviews": 6789,
        "delivery_days": 3,
        "description": "Latest iPad with 10.9-inch Liquid Retina display and A14 Bionic chip."
    },
    {
        "id": "ali_010",
        "name": "Electric Scooter 350W Motor 25 Mile Range",
        "marketplace": "AliExpress",
        "price": 299.99,
        "original_price": 599.99,
        "discount": 50,
        "image": "https://m.media-amazon.com/images/I/61QYUL7AOHL._AC_SL1500_.jpg",
        "url": "https://www.aliexpress.com/w/wholesale-electric-scooter.html",
        "free_shipping": True,
        "rating": 4.4,
        "reviews": 3456,
        "delivery_days": 16,
        "description": "Portable electric scooter with long range and foldable design."
    },
    {
        "id": "amz_013",
        "name": "Shark Navigator Lift-Away Vacuum Cleaner",
        "marketplace": "Amazon",
        "price": 179.99,
        "original_price": 249.99,
        "discount": 28,
        "image": "https://m.media-amazon.com/images/I/71H95C9YFEL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/s?k=shark+navigator+vacuum",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 34567,
        "delivery_days": 2,
        "description": "Powerful upright vacuum with HEPA filter and pet hair tools."
    },
    {
        "id": "temu_011",
        "name": "Yoga Mat Extra Thick Non-Slip with Carry Strap",
        "marketplace": "Temu",
        "price": 19.99,
        "original_price": 49.99,
        "discount": 60,
        "image": "https://m.media-amazon.com/images/I/81LHHBM1kAL._AC_SL1500_.jpg",
        "url": "https://www.temu.com/search_result.html?search_key=yoga+mat",
        "free_shipping": True,
        "rating": 4.5,
        "reviews": 8765,
        "delivery_days": 9,
        "description": "Premium yoga mat with extra cushioning for comfort during workouts."
    },
    {
        "id": "jumia_010",
        "name": "Samsung Galaxy Tab S9 11-inch 128GB",
        "marketplace": "Jumia",
        "price": 649.99,
        "original_price": 799.99,
        "discount": 19,
        "image": "https://m.media-amazon.com/images/I/71MnMmWvQVL._AC_SL1500_.jpg",
        "url": "https://www.jumia.com.ng/catalog/?q=samsung+galaxy+tab+s9",
        "free_shipping": True,
        "rating": 4.7,
        "reviews": 2345,
        "delivery_days": 4,
        "description": "Premium Android tablet with S Pen and stunning AMOLED display."
    }
]

def search_products(query, filters=None, page=1, per_page=50):
    """Search products based on query and filters with pagination"""
    query_lower = query.lower()
    results = []

    for product in MOCK_PRODUCTS:
        if query_lower in product['name'].lower() or query_lower in product['description'].lower():
            product_copy = product.copy()
            # Validate and get working image URL
            product_copy['image'] = get_validated_image(
                product_copy.get('image', ''),
                product_copy['name']
            )
            results.append(product_copy)

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

    # Calculate pagination
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page  # Ceiling division
    
    # Get current page results
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_results = results[start_idx:end_idx]
    
    return {
        'products': paginated_results,
        'total': total_results,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages
    }

def get_product_by_id(product_id):
    """Get a single product by ID"""
    for product in MOCK_PRODUCTS:
        if product['id'] == product_id:
            product_copy = product.copy()
            # Validate and get working image URL
            product_copy['image'] = get_validated_image(
                product_copy.get('image', ''),
                product_copy['name']
            )
            return product_copy
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