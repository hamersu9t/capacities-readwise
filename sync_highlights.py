import os
import requests
from datetime import datetime
import re
import yaml

READWISE_TOKEN = os.environ.get('READWISE_TOKEN')
CAPACITIES_TOKEN = os.environ.get('CAPACITIES_TOKEN')
CAPACITIES_SPACE_ID = os.environ.get('CAPACITIES_SPACE_ID')
EXPORT_API_URL = 'https://readwise.io/api/v2/export/'

def fetch_exports():
    if not READWISE_TOKEN:
        raise ValueError("READWISE_TOKEN environment variable is not set")
    
    headers = {'Authorization': f'Token {READWISE_TOKEN}'}
    all_results = []
    next_page_cursor = None

    while True:
        params = {'pageCursor': next_page_cursor} if next_page_cursor else {}
        response = requests.get(EXPORT_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        all_results.extend(data['results'])
        next_page_cursor = data.get('nextPageCursor')
        if not next_page_cursor:
            break

    return all_results

def write_article_to_capacities(article):
  # TODO looks like the capacities api is still extremely limited so i'll wait to implement this
  # for highlight in filtered_highlights:
  #     create_markdown_file(highlight, article)
  return

def main():
    try:
        print("Fetching exports...")
        exports = fetch_exports()
        print(f"Fetched {len(exports)} articles")

        print("Processing highlights...")
        for i, article in enumerate(exports, 1):
            highlights = article['highlights']
            print(f"Processing article {i} of {len(exports)}: '{article['title']}' - {len(highlights)} highlights")
            write_article_to_capacities(article)
        
        print(f"Successfully completed syncing {len(exports)} articles")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
