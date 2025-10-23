import sqlite3
from datetime import datetime
import json

DB_NAME = 'database.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Price tracking table
    c.execute('''CREATE TABLE IF NOT EXISTS price_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_id TEXT NOT NULL,
                  product_name TEXT NOT NULL,
                  marketplace TEXT NOT NULL,
                  price REAL NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Watchlist table
    c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_id TEXT UNIQUE NOT NULL,
                  product_name TEXT NOT NULL,
                  marketplace TEXT NOT NULL,
                  current_price REAL NOT NULL,
                  original_price REAL,
                  image_url TEXT,
                  product_url TEXT,
                  added_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Community deals upvotes (stored locally)
    c.execute('''CREATE TABLE IF NOT EXISTS deal_upvotes
                 (deal_id INTEGER PRIMARY KEY,
                  upvotes INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()

def add_to_watchlist(product_id, product_name, marketplace, current_price, original_price=None, image_url=None, product_url=None):
    """Add a product to the watchlist"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO watchlist (product_id, product_name, marketplace, current_price, original_price, image_url, product_url)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (product_id, product_name, marketplace, current_price, original_price, image_url, product_url))
        
        # Also add to price history
        c.execute('''INSERT INTO price_history (product_id, product_name, marketplace, price)
                     VALUES (?, ?, ?, ?)''',
                  (product_id, product_name, marketplace, current_price))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_from_watchlist(product_id):
    """Remove a product from the watchlist"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM watchlist WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

def get_watchlist():
    """Get all products in the watchlist"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM watchlist ORDER BY added_date DESC')
    items = c.fetchall()
    conn.close()
    return items

def is_in_watchlist(product_id):
    """Check if a product is in the watchlist"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM watchlist WHERE product_id = ?', (product_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_price_history(product_id, product_name, marketplace, price):
    """Add a price point to the history"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO price_history (product_id, product_name, marketplace, price)
                 VALUES (?, ?, ?, ?)''',
              (product_id, product_name, marketplace, price))
    conn.commit()
    conn.close()

def get_price_history(product_id):
    """Get price history for a specific product"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT price, timestamp FROM price_history 
                 WHERE product_id = ? 
                 ORDER BY timestamp ASC''', (product_id,))
    history = c.fetchall()
    conn.close()
    return history

def update_watchlist_price(product_id, new_price):
    """Update the current price for a watchlist item"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE watchlist SET current_price = ? WHERE product_id = ?', (new_price, product_id))
    conn.commit()
    conn.close()

def upvote_deal(deal_id):
    """Upvote a community deal"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if deal already has upvotes
    c.execute('SELECT upvotes FROM deal_upvotes WHERE deal_id = ?', (deal_id,))
    result = c.fetchone()
    
    if result:
        c.execute('UPDATE deal_upvotes SET upvotes = upvotes + 1 WHERE deal_id = ?', (deal_id,))
    else:
        c.execute('INSERT INTO deal_upvotes (deal_id, upvotes) VALUES (?, 1)', (deal_id,))
    
    conn.commit()
    conn.close()

def get_deal_upvotes(deal_id):
    """Get upvote count for a deal"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT upvotes FROM deal_upvotes WHERE deal_id = ?', (deal_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0
