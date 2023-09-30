import requests
import json
from bs4 import BeautifulSoup

url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the pickup line categories
categories = soup.find_all('h2', 'body-h2 css-zy1ra eqwrocx0')

# Create an empty dictionary to store the pickup lines
pickup_lines_dict = {}

# Scrape pickup lines under each category
for category in categories:
    # Get the category title
    category_title = category.text.strip()


    # Find the next sibling element after the category title
    next_sibling = category.find_next_sibling()

    # Create a list to store the pickup lines within the category
    pickup_lines = []

    # Iterate over the pickup lines within the category
    while next_sibling and next_sibling.name != 'h2':
        if next_sibling.name == 'ul':
            # Find all the list items within the ul element
            pickup_lines.extend([line.text.strip() for line in next_sibling.find_all('li')])

        # Move to the next sibling element
        next_sibling = next_sibling.find_next_sibling()

    # Add the pickup lines to the dictionary
    pickup_lines_dict[category_title] = pickup_lines

# Save the pickup lines dictionary as a JSON file
with open('pickup_lines.json', 'w') as json_file:
    json.dump(pickup_lines_dict, json_file, indent=4)

print("Pickup lines saved as 'pickup_lines.json' file.")