
import os
from datetime import datetime
from textwrap import shorten

import requests
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

API_URL = "https://newsapi.org/v2/top-headlines"

CATEGORIES = {
    "1": "technology",
    "2": "business",
    "3": "health",
}


def validate_api_key():
    """Check whether the API key exists."""
    if not API_KEY or API_KEY == "your_actual_api_key_here":
        print("Error: Add your valid NewsAPI key to the .env file.")
        return False
    return True


def get_category():
    """Ask the user to select a valid news category."""
    print("\nChoose a news category:")
    print("1. Technology")
    print("2. Business")
    print("3. Health")

    while True:
        choice = input("Enter your choice (1-3): ").strip()

        if choice in CATEGORIES:
            return CATEGORIES[choice]

        print("Invalid choice. Please enter 1, 2, or 3.")


def fetch_headlines(category):
    """Fetch headlines from NewsAPI."""
    params = {
        "apiKey": API_KEY,
        "category": category,
        "country": "us",
        "pageSize": 10,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("NewsAPI error:", data.get("message", "Unknown error"))
            return []

        return data.get("articles", [])

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Try again.")
    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")
    except requests.exceptions.HTTPError:
        try:
            message = response.json().get("message", response.text)
        except ValueError:
            message = response.text

        print(f"NewsAPI request failed ({response.status_code}): {message}")
    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
    except ValueError:
        print("Error: NewsAPI returned invalid JSON.")

    return []


def print_news_brief(category, articles):
    """Display the articles in a readable format."""
    today = datetime.now().astimezone().strftime("%d %B %Y")

    print("\n" + "=" * 60)
    print("              DAILY NEWS BRIEF")
    print("=" * 60)
    print(f"Date: {today}")
    print(f"Category: {category.title()}")
    print(f"Articles found: {len(articles)}")
    print("-" * 60)

    if not articles:
        print("No headlines were returned for this category.")
        print("Try another category or check your API access.")
        return

    for number, article in enumerate(articles, start=1):
        title = article.get("title") or "Title unavailable"
        source = (article.get("source") or {}).get("name") or "Unknown source"
        description = article.get("description") or "No summary available."
        url = article.get("url") or "No article link available"
        published = article.get("publishedAt") or "Unknown date"

        print(f"\n{number}. {title}")
        print(f"   Source: {source}")
        print(f"   Published: {published}")
        print(f"   Summary: {shorten(description, width=220, placeholder='...')}")
        print(f"   Read more: {url}")

    print("\n" + "=" * 60)
    print("End of news brief.")
    print("=" * 60)


def main():
    print("Welcome to the News Brief Generator!")

    if not validate_api_key():
        return

    category = get_category()
    articles = fetch_headlines(category)
    print_news_brief(category, articles)


if __name__ == "__main__":
    main()
