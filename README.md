# Easyfind Web Scraping Tool

This tool allows you to scrape data from the given URL using Selenium WebDriver and BeautifulSoup. The tool parses and collects data from specific tables in the webpage, filters it, and finally saves the resultant data in a CSV file.

*Note: This script was created with the help of AI tools/LLMs.*

## Requirements

- Python 3
- BeautifulSoup
- Selenium WebDriver
- pandas
- argparse

## Installation

To install all prerequisite Python libraries, use the following command:
```bash
pip install pandas beautifulsoup4 selenium argparse
```

Please note, this tool uses Firefox WebDriver for Selenium. Install it with the appropriate driver executable's path in your system's `PATH` variable. For more details check the official [Selenium documentation](https://selenium-python.readthedocs.io/installation.html).

For BeautifulSoup and pandas, no extra installation steps are required beyond the pip installation command above.

## Using the Script

The tool accepts two command line arguments, the start-date (`-s` or `--startdate`) and the filter-date (`-f` or `--filterdate`). 

The `-s` or `--startdate` is mandatory and determines the start-date to append to the URL query. It should follow the 'dd/mm/yyyy' format.

The `-f` or `--filterdate` helps to filter out dates in the final data frames, it should follow the 'yyyy-mm-dd' format.

Here's an example of how to run the script:

```bash
python3 main.py -s 01/10/2023 -f 2023-10-01
```

This script will continuously scrape data starting from the given start-date until it reaches the current date. At the end of scraping, the script generates a CSV file `output.csv` containing all the scraped data, and prints a message "Scraping completed. Data saved to output.csv." to indicate that the scraping process is done.

# Customizing the Tool

This tool is currently configured to scrape a specific category of lost items in a specific city from the EasyFind website. This is determined by the parameterized URL used in the script: 

```python
base_url = "https://secure.easyfind.com/webpublic/UI/SearchResultFoundItems.aspx?Category=5&SubCategory=26&City=z%u00fcrich&LostDate="
```

If you want the script to scrape data from different lost and found pages on the site, you will need to adjust the URL parameters in the script to match your desired search criteria. 

One of the easiest ways to do this is by performing a search manually on the EasyFind website and then copying the URL of the page with search results. The URL will contain parameters for category and city according to your selected search filters. 

For example, if you have performed a search for lost personal items in Geneva, the URL of the search results page might look like this:

```https://secure.easyfind.com/webpublic/UI/SearchResultFoundItems.aspx?Category=3&City=Gen%u00e8ve&LostDate=01/01/2023```

You can copy this URL and use it as the base URL in the script, but...

> :warning: **IMPORTANT**: Be sure to **remove the value** of the `LostDate` parameter from the URL. Keep the `LostDate` parameter itself in there, as the script appends its own value dynamically:

```python
base_url = "https://secure.easyfind.com/webpublic/UI/SearchResultFoundItems.aspx?Category=3&City=Gen%u00e8ve&LostDate="
```

Please, be careful with URL encoding and ensure you don't leave out important parameters like `Category` or `City`. The parameters in the base URL should exactly match your search criteria for the scraping to work correctly.

Please note that your desired category, city, and other search attributes might have a different parameter in the URL. Modify the script accordingly to match these parameters. Always make sure to inspect the webpage structure and the element identifiers, as they might differ for different categories or cities.

## Errors and Troubleshooting

If you run into any errors, make sure all required Python packages are installed and ensure that your Python version is 3.x. Check whether Firefox WebDriver for Selenium is properly installed and its path is correctly set in your `PATH` environment variable.

For specific issues, please open an issue in this repository with details about the error.

## Contribution

Contributions to improve this tool are welcomed. Please open an issue or submit a Pull request.
