# Python-EventWebScraper
A versatile script for scraping event details from websites, while adhering to robots.txt policies.

## Features:

- **Robots.txt Adherence**: The script checks the `robots.txt` of a website before scraping.
- **Pagination Handling**: If the events on a website are paginated, the script can navigate through the pages to scrape all data.
- **SQLite Storage**: Scraped data is saved in an SQLite database.
- **CSV Export**: The script provides an option to export the scraped data to a CSV file.

## Prerequisites:

Before you run the script, ensure you have:

- Python3 installed.
- Installed necessary libraries. You can do so with the command:
```
pip install requests beautifulsoup4 robotexclusionrulesparser
```

## How to Run:

1. Clone this repository to your local machine.
2. Navigate to the directory containing `event_scraper.py`.
3. Run the script using the command: `python3 event_scraper.py`.
4. Once the script has finished executing, check the directory for the `events.csv` file containing the scraped data.

## Disclaimer:

Please respect the `robots.txt` file of websites and always make sure to not hit the servers of the websites too hard. Web scraping might be illegal in some jurisdictions, and some websites' terms of service may disallow scraping. Always obtain proper permissions when required.

## License: 
MIT
