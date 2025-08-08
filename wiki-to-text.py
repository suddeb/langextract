#Pre-requisite
#pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def wikipedia_to_text(url, filename):
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract text from paragraphs, you might need to adjust this selector
        # depending on what content you want to include (e.g., tables, headings)
        paragraphs = soup.find_all('p')
            
        with open(filename, 'w', encoding='utf-8') as f:
            for p in paragraphs:
                f.write(p.get_text() + '\n\n') # Add newlines for readability

        print(f"Content saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
wikipedia_url = "https://en.wikipedia.org/wiki/Spider-Man"
output_filename = "data/spiderman.txt"
wikipedia_to_text(wikipedia_url, output_filename)