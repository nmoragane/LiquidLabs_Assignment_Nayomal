# Market Data API

A REST API for fetching and aggregating annual market data from Alpha Vantage with SQLite caching.

## Why These Libraries?

### FastAPI

We're using FastAPI because it's modern and actually fast. It's async by default, so we handle multiple requests without blocking each other. Plus it automatically generates interactive documentation at `/docs` which is super useful for testing. The built-in validation means we don't have to write a bunch of validation code ourselves.

### Uvicorn

This is the server that runs the FastAPI app. It's lightweight and designed specifically for async Python apps, so it pairs perfectly with FastAPI. It works great both locally and in production.

### Requests

Simple library for making HTTP calls to Alpha Vantage. We could use anything for this, but `requests` is straightforward. No overcomplicated dependencies.

### python-dotenv

Keeps our API key and config out of the code. Load environment variables from a `.env` file instead of hardcoding them. Standard practice and makes it safe to share code without accidentally leaking secrets.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root. This file holds your configuration:

```
ALPHA_VANTAGE_API_KEY=your_api_key_here
DATABASE_PATH=market_data.db
```

### 3. Run the Application

```bash
python app/main.py
```

Or if you prefer explicit uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

Check interactive docs: `http://localhost:8000/docs`
