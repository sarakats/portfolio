#=========================================================================================#
# Program: aquWikiData.py                                                                 #
# Purpose: To scrape information about aquariums from Wikipedia and store them            #
#          in a .csv file                                                                 #
# Author : Sara Katsabas                                                                  #
#=========================================================================================#

# Import required modules
import requests
from bs4 import BeautifulSoup
import csv

# Function: scrape_aquarium_info
# Purpose : Scrape information from Wikipedia articles about aquariums around the world
def scrape_aquarium_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ### Parameters for specific items on the Wiki page
    # Find title of the page
    title = soup.find('h1', {'id': 'firstHeading'}).text.strip()

    # Initialize with defaults
    location = "not available"
    number_of_animals = "not available"
    tank_volume = "not available"
    coordinates = "not available"

    # Handling infobox text
    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.text.strip().lower()
                data_text = data.text.strip().replace('\n', ' ')
                if 'location' in header_text:
                    location = data_text
                elif 'number of animals' in header_text or 'no. of animals' in header_text:
                    number_of_animals = data_text
                elif 'volume' in header_text or 'total volume' in header_text:
                    tank_volume = data_text

    # Get coordinates from geo microformat (if available)
    coord = soup.find('span', class_='geo')
    if coord:
        coordinates = coord.text.strip()

    return {
        'Name': title,
        'Location': location,
        'Number of Animals': number_of_animals,
        'Tank Volume': tank_volume,
        'Coordinates': coordinates
    }

# Function: write_to_csv
# Purpose : Write gathered information to a .csv file
def write_to_csv(data, filename='C:/Assignment5/aquariums.csv'):

    file_exists = False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Location', 'Number of Animals', 'Tank Volume', 'Coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Usage in Command Prompt window
if __name__ == "__main__":
    while True:
        url = input("Enter Wikipedia URL (or type 'done' to finish): ").strip()
        if url.lower() == 'done':
            break
        try:
            data = scrape_aquarium_info(url)
            write_to_csv(data)
            print(f"Info for '{data['Title']}' saved.")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
