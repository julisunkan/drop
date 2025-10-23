# Market PriceDrop Tracker

## Project Overview
A universal price comparison and deal-finder web application that helps users find the best deals across major marketplaces (Amazon, AliExpress, eBay, Jumia, Temu) without requiring login or registration.

## Tech Stack
- **Backend**: Python 3.11 with Flask
- **Database**: SQLite (local storage)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **PDF Export**: reportlab
- **AI Features**: HuggingFace free API (facebook/bart-large-cnn)

## Key Features Implemented
1. **Global Product Search**: Search across all marketplaces with filtering by marketplace, free shipping, discount-only, and sorting options
2. **Price Tracking**: SQLite-based watchlist system with price history tracking
3. **Interactive Charts**: Chart.js price trend graphs with color-coded price changes
4. **AI Insights**: 
   - Product summary generation
   - Buy now recommendation engine
   - Review authenticity checker
5. **Community Deals**: JSON-based curated deals with local upvote system
6. **PDF Export**: Generate PDF reports of watchlist with reportlab
7. **Responsive UI**: Bootstrap 5 with light/dark mode toggle
8. **Product Comparison**: Side-by-side comparison view for up to 4 products

## Project Structure
```
/
├── app.py                    # Main Flask application
├── database.py               # SQLite database helpers
├── mock_data.py             # Mock marketplace data
├── community-deals.json     # Curated deals data
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles with marketplace themes
│   └── js/
│       ├── main.js          # Theme toggle, watchlist modal
│       └── search.js        # Search page interactions
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Homepage with search
    ├── search_results.html  # Search results page
    ├── product_detail.html  # Product detail with price chart
    ├── community.html       # Community deals page
    └── compare.html         # Product comparison page
```

## Database Schema
- **price_history**: Tracks price changes over time
- **watchlist**: User's tracked products
- **deal_upvotes**: Local upvote counts for community deals

## Current State
- All core features implemented and working
- Mock data with real product images from Unsplash (12 sample products)
- Functional marketplace links to Amazon, eBay, AliExpress, Jumia, Temu
- AI features use HuggingFace free inference API
- **Vibrant colorful UI** with extensive CSS animations:
  - Animated gradient backgrounds
  - Smooth entrance animations (fadeInUp, slideInDown, zoomIn)
  - Interactive hover effects with transforms and shadows
  - Pulsing and glowing effects on key elements
  - Product card animations with image zoom on hover
- **Complete light/dark mode support** with proper gradient overrides
- Mobile-responsive design with Bootstrap 5

## Next Phase (Not Implemented)
- PWA features (manifest.json, service worker)
- Real marketplace API integrations
- Currency conversion API
- Voice search
- Local notifications for price drops
- CSV export option

## Development Notes
- The application uses mock data for product search
- All preferences stored in SQLite and localStorage
- No authentication system (as per requirements)
- Free shipping filter available
- Discount-only filter available
- Multiple sort options (price, discount, delivery speed)
