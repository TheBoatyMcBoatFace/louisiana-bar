import requests
from bs4 import BeautifulSoup

# Define the URL
url = 'https://www.legis.la.gov/legis/Laws_Toc.aspx?folder=69&level=Parent'

# Send a GET request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table based on the known structure and attributes (somewhat simplified approach)
    # Assuming the table of interest is uniquely identified by its proximity to the specific title
    title = soup.find('span', string="Code of Criminal Procedure")
    # Moving up to the common parent of title and table, then finding the table
    table = title.find_next_sibling('table')

    if not table:
        print("Table not found directly after the title, trying a broader search.")
        # If the table isn't the immediate next sibling, this part searches more broadly around the title
        container = title.find_parent('div')
        table = container.find('table')

    if table:
        # Extract and print all links (href attributes) from the table
        for link in table.find_all('a', href=True):
            full_url = f"https://www.legis.la.gov/legis/{link['href']}"  # Assuming relative URL needs prefix
            print(full_url)
    else:
        print("Failed to locate the table.")
else:
    print(f"Failed to fetch the page, status code: {response.status_code}")
