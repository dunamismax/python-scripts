# cross_platform/misc/get_daily_quote.py
import json
import urllib.request
from typing import Any, Dict, List

# --- Configuration ---
# The new API endpoint for a single random quote. No API key is needed for basic use.
# Per the docs, this is the simplest endpoint for learning and random daily quotes.
API_URL = "https://zenquotes.io/api/random"


def fetch_random_quote() -> Dict[str, Any] | None:
    """
    Fetches a single random quote from the ZenQuotes API.

    Returns:
        A dictionary containing the quote data, or None if an error occurs.
    """
    print("Fetching a random quote from ZenQuotes.io...")
    try:
        # The 'with' statement ensures the connection is closed automatically.
        # A timeout is added as a safeguard against a non-responsive server.
        with urllib.request.urlopen(API_URL, timeout=10) as response:
            if response.status != 200:
                print(f"Error: API returned status code {response.status}")
                return None

            # The response data is in bytes, so we decode it into a string (UTF-8).
            data_string = response.read().decode("utf-8")

            # The ZenQuotes API returns a JSON array containing a single object.
            # We parse it into a Python list.
            data: List[Dict[str, Any]] = json.loads(data_string)

            # We check if the list is not empty and then return the first item.
            if data:
                return data[0]
            else:
                print("Error: API returned an empty response.")
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main() -> None:
    """Main function to fetch, parse, and display the quote."""
    quote_data = fetch_random_quote()

    if quote_data:
        # The API uses 'q' for the quote text and 'a' for the author.
        content = quote_data.get("q", "No content found.")
        author = quote_data.get("a", "Unknown Author")

        # Simple, clean formatting for the output.
        print("\n" + "=" * 60)
        print(f'"{content}"')
        print(f"— {author}")
        print("=" * 60)

        # Per the API's terms, attribution is required for the free version.
        # This is good practice to respect the people providing the free service.
        print("Inspirational quotes provided by ZenQuotes API")


if __name__ == "__main__":
    main()
