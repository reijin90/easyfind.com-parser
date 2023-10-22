from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import argparse
from datetime import datetime, timedelta
import urllib.parse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Web scraping dates.')
parser.add_argument('-s', '--startdate', required=True, help='Start date in dd/mm/yyyy format')
parser.add_argument('-f', '--filterdate', required=True, help='Filter date in yyyy-mm-dd format')
args = parser.parse_args()

# Convert the start-date argument into a datetime object
current_date = datetime.strptime(args.startdate, '%d/%m/%Y')

# Define the base URL
base_url = "https://secure.easyfind.com/webpublic/UI/SearchResultFoundItems.aspx?Category=5&SubCategory=26&City=z%u00fcrich&LostDate="

# Define the options for Firefox
options = Options()
options.add_argument("--headless")

# Create a new instance of the Firefox driver with the defined options
driver = webdriver.Firefox(options=options)

# The rest of your code...

# Define a function to parse table data and add it to our dataframe
def parse_table(table_id):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': table_id})

    data = []

    if table is not None: 
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    return pd.DataFrame(data)

final_df = pd.DataFrame()

# Continue looping until the current date
while current_date.date() < datetime.now().date():
    # Create the URL with the current date
    url = base_url + urllib.parse.quote(current_date.strftime('%m/%d/%Y'))
    
    # Navigate to the website
    driver.get(url)
    print(f"Parsing URL '{url}'")

    # Initialize an empty dataframe to hold all our parsed data
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    # While the "next" button is active for table 1, keep clicking it and parsing the table data on the new page
    while True:
        # Parse the table and append the data to our dataframe
        df1 = pd.concat([df1, parse_table('MainContentPlaceHolder_ResultListTable')], ignore_index=True)
        print("Current table 1 size: ", df1.shape)

        # Try to click the "next" button and wait for the new page to load
        try:
            next_button = driver.find_element(By.ID, 'MainContentPlaceHolder_SearchResultNavigationControl_MoveNextButton')
            next_button.click()
            print("Navigating to the next page of table 1...")
            time.sleep(2)
        except NoSuchElementException:
            print("Reached the end of table 1.")
            # If the "next" button can't be clicked, we've reached the end of the pages and break the loop
            break

    # While the "next" button is active for table 2, keep clicking it and parsing the table data on the new page
    while True:
        # Parse the table and append the data to our dataframe
        df2 = pd.concat([df2, parse_table('MainContentPlaceHolder_ExternalResultListTable')], ignore_index=True)
        print("Current table 2 size: ", df2.shape)

        # Try to click the "next" button and wait for the new page to load
        try:
            next_button = driver.find_element(By.ID, 'MainContentPlaceHolder_SearchExternalResultsNavigationControl_MoveNextButton')
            next_button.click()
            print("Navigating to the next page of table 2...")
            time.sleep(2)
        except NoSuchElementException:
            print("Reached the end of table 2.")
            # If the "next" button can't be clicked, we've reached the end of the pages and break the loop
            break

    # Drop empty rows
    df1.dropna(how='all', inplace=True)
    df2.dropna(how='all', inplace=True)

    # Drop last column of df1
    df1 = df1.iloc[:, :-1]

    # Filter out rows that don't contain "Zürich" in df1
    df1 = df1[df1.apply(lambda row: row.astype(str).str.contains('Zürich').any(), axis=1)]

    # Filter out rows that don't contain "Schlüssel" in both dataframes
    df1 = df1[df1.apply(lambda row: row.astype(str).str.contains('Schlüssel').any(), axis=1)]
    df2 = df2[df2.apply(lambda row: row.astype(str).str.contains('Schlüssel').any(), axis=1)]

    # Shift the second and third columns in df2 to the right by one column
    df2[df2.columns[1:]] = df2[df2.columns[1:]].shift(1, axis=1)

    # Merge the two dataframes
    df = pd.concat([df1, df2], axis=0, ignore_index=True)

    # Convert the first column to datetime
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], dayfirst=True)

    # Sort by date in descending order
    df.sort_values(by=df.columns[0], ascending=False, inplace=True)

    # After parsing data, append this day's data to the final dataframe:
    final_df = pd.concat([final_df, df])

    # After parsing code get the max date
    max_date = pd.to_datetime(df[df.columns[0]], dayfirst=True).max()

    # If max_date is later than today, replace with today's date
    if max_date.date() > datetime.today().date():
        current_date = datetime.today()
    else:
        current_date = max_date + timedelta(days=1) # Start from the next da

driver.quit()

# Once outside the loop, you can perform any final operations on final_df
# Filter the dataframe to keep only entries on or after the provided filter-date
final_df = final_df[final_df[final_df.columns[0]] >= args.filterdate]

# Write the final dataframe to a CSV file
final_df.to_csv('output.csv', index=False)

print("Scraping completed. Data saved to output.csv.")