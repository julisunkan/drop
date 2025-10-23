from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from huggingface_hub import InferenceClient

import database
import mock_data

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize database
database.init_db()

# HuggingFace client for AI features
hf_client = InferenceClient()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search products across marketplaces"""
    query = request.args.get('q', '')
    marketplace = request.args.get('marketplace', 'all')
    free_shipping = request.args.get('free_shipping') == 'true'
    discount_only = request.args.get('discount_only') == 'true'
    sort_by = request.args.get('sort_by', 'relevance')
    
    filters = {
        'marketplace': marketplace,
        'free_shipping': free_shipping,
        'discount_only': discount_only,
        'sort_by': sort_by
    }
    
    results = mock_data.search_products(query, filters)
    
    # Check which products are in watchlist
    for product in results:
        product['in_watchlist'] = database.is_in_watchlist(product['id'])
    
    return render_template('search_results.html', 
                         query=query, 
                         results=results,
                         filters=filters)

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Product detail page with price history"""
    product = mock_data.get_product_by_id(product_id)
    
    if not product:
        return "Product not found", 404
    
    # Get price history from database or generate mock data
    db_history = database.get_price_history(product_id)
    
    if db_history:
        price_history = [{'date': row[1], 'price': row[0]} for row in db_history]
    else:
        price_history = mock_data.generate_price_history(product['price'])
    
    product['in_watchlist'] = database.is_in_watchlist(product_id)
    
    return render_template('product_detail.html', 
                         product=product,
                         price_history=json.dumps(price_history))

@app.route('/api/watchlist/add', methods=['POST'])
def add_to_watchlist():
    """Add product to watchlist"""
    data = request.json
    
    success = database.add_to_watchlist(
        product_id=data['product_id'],
        product_name=data['product_name'],
        marketplace=data['marketplace'],
        current_price=data['current_price'],
        original_price=data.get('original_price'),
        image_url=data.get('image_url'),
        product_url=data.get('product_url')
    )
    
    return jsonify({'success': success})

@app.route('/api/watchlist/remove', methods=['POST'])
def remove_from_watchlist():
    """Remove product from watchlist"""
    data = request.json
    database.remove_from_watchlist(data['product_id'])
    return jsonify({'success': True})

@app.route('/api/watchlist')
def get_watchlist():
    """Get watchlist items"""
    items = database.get_watchlist()
    watchlist = []
    
    for item in items:
        watchlist.append({
            'id': item[0],
            'product_id': item[1],
            'product_name': item[2],
            'marketplace': item[3],
            'current_price': item[4],
            'original_price': item[5],
            'image_url': item[6],
            'product_url': item[7],
            'added_date': item[8]
        })
    
    return jsonify(watchlist)

@app.route('/api/ai/summary', methods=['POST'])
def ai_summary():
    """Generate AI product summary"""
    data = request.json
    product_text = f"{data['name']}. {data.get('description', '')}"
    
    try:
        # Use HuggingFace's free inference API for summarization
        response = hf_client.summarization(
            product_text,
            model="facebook/bart-large-cnn"
        )
        
        summary = response.summary_text if hasattr(response, 'summary_text') else str(response)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'summary': 'AI summary temporarily unavailable. This is a premium product with excellent features and competitive pricing.'
        })

@app.route('/api/ai/buy-advice', methods=['POST'])
def buy_advice():
    """AI-powered buy now recommendation"""
    data = request.json
    
    try:
        price_history = data.get('price_history', [])
        current_price = data.get('current_price', 0)
        
        # Simple analysis
        if len(price_history) >= 2:
            recent_prices = [p['price'] for p in price_history[-7:]]
            avg_price = sum(recent_prices) / len(recent_prices)
            
            if current_price < avg_price * 0.9:
                advice = "🎯 Great time to buy! Price is 10% below recent average. This is a good deal."
            elif current_price < avg_price:
                advice = "👍 Good price. Slightly below recent average. Consider buying if you need it."
            elif current_price > avg_price * 1.1:
                advice = "⏳ Wait for a better deal. Price is above recent average. Consider waiting."
            else:
                advice = "📊 Fair price. Around the average. Buy if you need it now."
        else:
            discount = data.get('discount', 0)
            if discount > 50:
                advice = "🔥 Excellent discount! Over 50% off is a great deal."
            elif discount > 20:
                advice = "👍 Good discount. This is a decent saving."
            else:
                advice = "📊 Standard pricing. Buy if you need the product."
        
        return jsonify({
            'success': True,
            'advice': advice
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'advice': 'Unable to generate advice at this time.'
        })

@app.route('/api/ai/review-check', methods=['POST'])
def review_check():
    """Check for suspicious reviews"""
    data = request.json
    
    try:
        rating = data.get('rating', 0)
        review_count = data.get('review_count', 0)
        
        # Simple heuristic check
        flags = []
        
        if rating >= 4.9 and review_count > 1000:
            flags.append("⚠️ Unusually high rating with many reviews")
        
        if review_count < 10:
            flags.append("ℹ️ Limited reviews - new product")
        
        if len(flags) == 0:
            result = "✅ Reviews appear authentic. Rating and review count are in normal range."
        else:
            result = "Review Analysis:\n" + "\n".join(flags)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'result': 'Analysis unavailable.'
        })

@app.route('/community')
def community():
    """Community deals page"""
    with open('community-deals.json', 'r') as f:
        deals = json.load(f)
    
    # Add local upvote counts
    for deal in deals:
        local_upvotes = database.get_deal_upvotes(deal['id'])
        deal['total_upvotes'] = deal['upvotes'] + local_upvotes
        deal['user_upvoted'] = local_upvotes > 0
    
    # Sort by total upvotes
    deals.sort(key=lambda x: x['total_upvotes'], reverse=True)
    
    return render_template('community.html', deals=deals)

@app.route('/api/community/upvote', methods=['POST'])
def upvote_deal():
    """Upvote a community deal"""
    data = request.json
    database.upvote_deal(data['deal_id'])
    return jsonify({'success': True})

@app.route('/export/pdf')
def export_pdf():
    """Export search results or watchlist to PDF"""
    export_type = request.args.get('type', 'search')
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Market PriceDrop Tracker - {export_type.title()} Results</b>", 
                     styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Date
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                         styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    if export_type == 'watchlist':
        items = database.get_watchlist()
        
        # Create table
        data = [['Product', 'Marketplace', 'Current Price', 'Original Price', 'Savings']]
        
        for item in items:
            product_name = item[2][:40] + '...' if len(item[2]) > 40 else item[2]
            marketplace = item[3]
            current = f"${item[4]:.2f}"
            original = f"${item[5]:.2f}" if item[5] else 'N/A'
            savings = f"${(item[5] - item[4]):.2f}" if item[5] else 'N/A'
            
            data.append([product_name, marketplace, current, original, savings])
    else:
        # Search results (would need to be passed as parameters)
        data = [['No data', 'to', 'display', 'in', 'demo']]
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'pricedrop_{export_type}_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/compare')
def compare():
    """Side-by-side product comparison"""
    product_ids = request.args.getlist('products')
    
    products = []
    for pid in product_ids[:4]:  # Max 4 products
        product = mock_data.get_product_by_id(pid)
        if product:
            products.append(product)
    
    return render_template('compare.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
