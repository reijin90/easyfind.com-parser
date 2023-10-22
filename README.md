# Easyfind Web Scraping Tool

This tool allows you to scrape data from the given URL using Selenium WebDriver and BeautifulSoup. The tool parses and collects data from specific tables in the webpage, filters it, and finally saves the resultant data in a CSV file.

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

## Errors and Troubleshooting

If you run into any errors, make sure all required Python packages are installed and ensure that your Python version is 3.x. Check whether Firefox WebDriver for Selenium is properly installed and its path is correctly set in your `PATH` environment variable.

For specific issues, please open an issue in this repository with details about the error.

## Contribution

Contributions to improve this tool are welcomed. Please open an issue or submit a Pull request.
