import requests
import csv

# URL of the CSV file
url = "https://gist.githubusercontent.com/brooksandrew/e570c38bcc72a8d102422f2af836513b/raw/89c76b2563dbc0e88384719a35cba0dfc04cd522/edgelist_sleeping_giant.csv"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the CSV content
    data = response.text.strip().split('\n')
    reader = csv.reader(data)

    # Write data to a local CSV file
    with open('edgelist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(reader)

    print("CSV file saved successfully.")
else:
    print("Failed to fetch data from the URL.")
