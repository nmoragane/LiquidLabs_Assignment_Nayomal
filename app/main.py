from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from app.database import init_db, data_exists, get_year_data, insert_monthly_data
from app.external_api import fetch_monthly_data, parse_monthly_data

# Load environment variables
load_dotenv()

app = FastAPI(title="Market Data API", version="1.0.0")

@app.on_event("startup")
async def startup():
    """Initialize database on application startup."""
    init_db()

@app.get("/symbols/{symbol}/annual/{year}")
async def get_annual_data(symbol: str, year: int):
    # Validate inputs
    if not symbol or len(symbol) > 10:
        raise HTTPException(status_code=400, detail="Invalid symbol")
    
    if year < 1980 or year > 2100:
        raise HTTPException(status_code=400, detail="Invalid year")
    
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="ALPHA_VANTAGE_API_KEY environment variable is not set.")
        
        if not data_exists(symbol, year):
            try:
                api_response = fetch_monthly_data(api_key, symbol)
                monthly_data = parse_monthly_data(symbol, api_response)
                
                if not monthly_data:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No data found for symbol '{symbol}'"
                    )
                
                # Insert all monthly data into database
                for data_row in monthly_data:
                    insert_monthly_data(*data_row)
            
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")
        
        year_data = get_year_data(symbol, year)
        
        if not year_data:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for symbol '{symbol}' in year {year}"
            )
        
        high = max(float(row['high']) for row in year_data)
        low = min(float(row['low']) for row in year_data)
        volume = sum(row['volume'] for row in year_data)
        
        return {
            "high": f"{high:.4f}",
            "low": f"{low:.4f}",
            "volume": str(volume)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
