# nyt_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NYT_BOOKS_API_KEY = os.getenv("NYT_BOOKS_API_KEY")
NYT_BOOKS_API_URL = "https://api.nytimes.com/svc/books/v3/lists/current/"

def fetch_books_from_nyt(list_name="hardcover-fiction"):
    url = f"{NYT_BOOKS_API_URL}{list_name}.json"
    params = {"api-key": NYT_BOOKS_API_KEY}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        books = response.json().get("results", {}).get("books", [])
        return books
    else:
        print(f"Failed to fetch books: {response.status_code}")
        return []

