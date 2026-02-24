import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_country_data(url):
    """
    Fetches and parses a Wikipedia page to get its HTML content.
    
    Args:
        url (str): The URL of the page to scrape.

    Returns:
        BeautifulSoup: A BeautifulSoup object if the request is successful, None otherwise.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the page: {e}")
        return None


def clean_country_name(dirty_name):
    """
    Cleans a country name by removing bracketed references and duplicate text.
    
    Args:
        dirty_name (str): The country name with potential unwanted characters.
    
    Returns:
        str: The cleaned country name without duplicates.
    """
    # Removes bracketed notes, e.g., [12]
    cleaned_name = re.sub(r'\[.*?\]', '', dirty_name)
    
    # Handles duplicate names like "China China"
    cleaned_name = re.sub(r'(\S+)\s+\1', r'\1', cleaned_name)
    
    # Strips any leading/trailing whitespace
    return cleaned_name.strip()


def extract_table_data(soup):
    """
    Extracts data from the population table on the Wikipedia page.
    
    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.

    Returns:
        list: A list of dictionaries with data for each country.
    """
    table = soup.find('table', {'class': 'wikitable'})

    if not table:
        print("Error: Could not find the table with class 'wikitable'.")
        return []

    rows = table.find_all('tr')
    country_data = []
    
    # Iterates over rows, skipping the header (first row)
    for row in rows[1:]:
        cells = row.find_all('td')
        
        # Ensures the row has enough cells
        if len(cells) >= 3:
            position = cells[0].text.strip()
            country = clean_country_name(cells[1].text)
            population = cells[2].text.strip().replace('.', '')
            
            country_data.append({
                'Position': position,
                'Country': country,
                'Population': population
            })
            
    return country_data


def main():
    """
    Main function to run the web scraping script.
    """
    print("Starting web scraping on Wikipedia...")
    url = "https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_poblaci%C3%B3n"

    soup = fetch_country_data(url)

    if soup:
        extracted_data = extract_table_data(soup)

        if extracted_data:
            print("\n--- Extracted country data (first 10) ---")
            for country in extracted_data[:10]:
                print(f"Position: {country['Position']}, Country: {country['Country']}, Population: {country['Population']}")
                
            df = pd.DataFrame(extracted_data)
            print("\n--- Pandas DataFrame (first 5 rows) ---")
            print(df.head())
            
            # Optional: Save data to a CSV file
            # df.to_csv('world_population.csv', index=False)
            # print("\nData saved to 'world_population.csv'.")
        else:
            print("Could not extract data from the table.")
    
    print("\nWeb scraping finished.")

if __name__ == "__main__":
    main()
