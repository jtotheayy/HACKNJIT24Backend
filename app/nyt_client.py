import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

NYT_BOOKS_API_KEY = os.getenv("NYT_BOOKS_API_KEY")
NYT_BOOKS_API_URL = "https://api.nytimes.com/svc/books/v3/lists/"
MAX_RETRIES = 1
INITIAL_DELAY = 1  # Starting delay in seconds

def fetch_all_list_names():
    url = f"{NYT_BOOKS_API_URL}names.json"
    params = {"api-key": NYT_BOOKS_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        lists = response.json().get("results", [])
        return [lst["list_name_encoded"] for lst in lists]
    else:
        print(f"Failed to fetch list names: {response.status_code}")
        return []

def fetch_books_from_nyt(list_name):
    # Corrected URL construction
    url = f"{NYT_BOOKS_API_URL}current/{list_name}.json"
    params = {"api-key": NYT_BOOKS_API_KEY}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        books = response.json().get("results", {}).get("books", [])
        return books
    else:
        print(f"Failed to fetch books: {response.status_code}")
        return []
