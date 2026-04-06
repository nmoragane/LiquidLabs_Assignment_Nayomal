import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'market_data.db')

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create monthly_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, year, month)
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_symbol_year 
        ON monthly_data(symbol, year)
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def insert_monthly_data(symbol, year, month, open_price, high, low, close, volume):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO monthly_data 
            (symbol, year, month, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (symbol, year, month, open_price, high, low, close, volume))
        conn.commit()

def get_year_data(symbol, year):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM monthly_data 
            WHERE symbol = ? AND year = ?
            ORDER BY month
        ''', (symbol, year))
        return cursor.fetchall()

def data_exists(symbol, year):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count FROM monthly_data 
            WHERE symbol = ? AND year = ?
        ''', (symbol, year))
        result = cursor.fetchone()
        return result['count'] > 0
