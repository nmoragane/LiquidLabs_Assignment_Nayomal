import requests
import os
from datetime import datetime

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def fetch_monthly_data(api_key, symbol):
    
    params = {
        'function': 'TIME_SERIES_MONTHLY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'full'
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check for API errors
        if 'Error Message' in data:
            raise Exception(f"Alpha Vantage API error: {data['Error Message']}")
        
        if 'Note' in data:
            raise Exception(f"Alpha Vantage API rate limit: {data['Note']}")
        
        if 'Time Series (Monthly)' not in data:
            raise ValueError(f"Invalid response format or symbol '{symbol}' not found")
        
        return data
    
    except requests.exceptions.Timeout:
        raise Exception("Alpha Vantage API request timed out")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch from Alpha Vantage API: {str(e)}")

def parse_monthly_data(symbol, api_response):
    monthly_data = []
    
    if 'Time Series (Monthly)' not in api_response:
        return monthly_data
    
    time_series = api_response['Time Series (Monthly)']
    
    for date_str, values in time_series.items():
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            year = date.year
            month = date.month
            
            open_price = float(values.get('1. open', 0))
            high = float(values.get('2. high', 0))
            low = float(values.get('3. low', 0))
            close = float(values.get('4. close', 0))
            volume = int(values.get('5. volume', 0))
            
            monthly_data.append((symbol, year, month, open_price, high, low, close, volume))
        except (ValueError, KeyError) as e:
            # Skip invalid records
            continue
    
    return monthly_data
