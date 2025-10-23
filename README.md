# 🏷️ Market PriceDrop Tracker

A universal price comparison and deal-finder web application that helps you find the best deals across major marketplaces (Amazon, AliExpress, eBay, Jumia, Temu) without requiring login or registration.

## ✨ Features

### Core Features
- **🌍 Global Product Search**: Search across all major marketplaces with a single query
- **📊 Price Tracking**: SQLite-based watchlist system with historical price tracking
- **📈 Interactive Charts**: Chart.js visualizations showing 30-day price trends with color-coded changes
- **🤖 AI Insights**: 
  - Product summary generator
  - Smart "Buy Now" recommendation engine based on price trends
  - Review authenticity checker with trust scores
- **🔥 Community Deals**: Curated deals section with local upvote system
- **📄 PDF Export**: Generate professional PDF reports of your watchlist
- **🔍 Advanced Filtering**: 
  - Filter by marketplace
  - Free shipping only
  - Discount-only items
  - Sort by price, discount, or delivery speed
- **⚖️ Product Comparison**: Side-by-side comparison of up to 4 products
- **🌓 Light/Dark Mode**: Theme toggle with localStorage persistence
- **📱 Responsive Design**: Mobile-friendly Bootstrap 5 interface

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **PDF Export**: reportlab
- **AI**: HuggingFace API (optional)

## 📦 Installation

The application is already set up and ready to run!

### Dependencies
All required dependencies are installed:
- Flask
- requests
- reportlab
- beautifulsoup4
- matplotlib
- pandas
- pillow
- huggingface-hub

## 🚀 Running the Application

The Flask server is configured to run automatically. Simply click the **Run** button or the application will start on port 5000.

Access the application at: `http://localhost:5000`

## 🔑 Environment Variables (Optional)

### SESSION_SECRET
Used for Flask session management. Already configured with a default value.

### HUGGINGFACE_TOKEN
Optional token for enhanced AI features. The app works perfectly without it using intelligent fallbacks.

To add your HuggingFace token:
1. Get a free token from [HuggingFace](https://huggingface.co/settings/tokens)
2. Add it to Replit Secrets as `HUGGINGFACE_TOKEN`

## 📖 Usage Guide

### Searching for Products
1. Enter a product name in the search bar on the homepage
2. Click "Search All Stores" or use the quick category badges
3. Apply filters for marketplace, free shipping, discounts, etc.

### Tracking Prices
1. Search for a product
2. Click "Track Price" on any product card
3. View your watchlist by clicking the Watchlist icon in the navigation

### Viewing Price History
1. Click on any product to see its detail page
2. View the interactive price trend chart
3. See current, average, lowest, and highest prices

### Using AI Insights
On any product detail page, click:
- **Product Summary**: Get an AI-generated summary
- **Buy Advice**: Receive smart buying recommendations based on price trends
- **Review Check**: Analyze review authenticity with a trust score

### Comparing Products
1. On search results, click "Compare" on multiple products (2-4)
2. Click "Compare Selected" at the bottom
3. View side-by-side comparison table

### Community Deals
1. Click "Community Deals" in navigation
2. Browse curated deals from the community
3. Upvote your favorite deals

### Exporting to PDF
1. Open your watchlist
2. Click "Export to PDF"
3. Download a professional report with your tracked products

## 📁 Project Structure

```
/
├── app.py                    # Main Flask application
├── database.py               # SQLite database helpers
├── mock_data.py             # Mock marketplace data (12 products)
├── community-deals.json     # Curated deals data
├── database.db              # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       ├── main.js          # Theme toggle & watchlist
│       └── search.js        # Search interactions
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Homepage
    ├── search_results.html  # Search results
    ├── product_detail.html  # Product details
    ├── community.html       # Community deals
    └── compare.html         # Product comparison
```

## 🎨 Features in Detail

### Marketplace Support
- **Amazon** (Orange badge)
- **eBay** (Blue badge)
- **AliExpress** (Red badge)
- **Jumia** (Orange badge)
- **Temu** (Orange/Red badge)

### Database Schema
- **price_history**: Tracks all price changes over time
- **watchlist**: Stores user's tracked products
- **deal_upvotes**: Local upvote counts for community deals

### AI Features (with Graceful Fallbacks)
All AI features work even without a HuggingFace token:
- **No token**: Intelligent rule-based analysis
- **With token**: Enhanced AI-powered insights

## 🔐 Security Features
- Environment variable support for sensitive data
- Session secret management
- No hardcoded credentials
- SQL injection protection via parameterized queries

## 🚧 Future Enhancements (Not Yet Implemented)

- **PWA Features**: manifest.json and service worker for offline access
- **Real API Integration**: Connect to actual marketplace APIs
- **Currency Conversion**: Multi-currency support via exchangerate.host
- **Voice Search**: Voice-activated product search
- **Price Alerts**: Local notifications for price drops
- **CSV Export**: Alternative export format

## 🐛 Known Limitations

- Uses mock data (12 sample products) instead of real marketplace APIs
- Price history is simulated for demonstration purposes
- Community deals are static from JSON file

## 💡 Tips

1. **Dark Mode**: Click the moon/sun icon in the top-right corner
2. **Quick Search**: Use category badges for instant searches
3. **Price Trends**: Green indicates price drops, red indicates increases
4. **Trust Scores**: 80+ is excellent, 60-79 is good, below 60 needs caution

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

This is a demo application. Feel free to fork and enhance with:
- Real marketplace API integrations
- More sophisticated AI models
- Additional features from the roadmap

---

**Built with Flask, Bootstrap 5, and Chart.js** | **No login required** | **Privacy-focused**
