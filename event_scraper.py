import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import logging
import csv
from robotexclusionrulesparser import RobotFileParserLookalike as RFP

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup
conn = sqlite3.connect('events.db')
cursor = conn.cursor()

# Create the SQLite table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT,
    venue TEXT,
    speakers TEXT,
    ticket_price TEXT,
    source TEXT
)
''')
conn.commit()


def can_scrape(url):
    """
    Check website's robots.txt to see if scraping is allowed using robotexclusionrulesparser.
    """
    robot_parser = RFP()
    robot_parser.set_url("/".join(url.split("/")[:3]) + "/robots.txt")
    robot_parser.read()
    return robot_parser.can_fetch("*", url)


def add_event(name, date, venue, speakers, ticket_price, source):
    """
    Add the event data into the SQLite database.
    """
    cursor.execute("INSERT INTO events (name, date, venue, speakers, ticket_price, source) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, date, venue, speakers, ticket_price, source))
    conn.commit()


def output_to_csv():
    """
    Output the data in the SQLite database to a CSV file.
    """
    with open('events.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()

        # Write headers and rows
        writer.writerow([desc[0] for desc in cursor.description])
        writer.writerows(rows)


def scrape_events(url):
    """
    Scrape event details from the given URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Pagination logic (assuming the website has a 'next-page' class for the next button)
    while True:
        # Find all events
        events = soup.find_all(class_='event')
        for event in events:
            name = event.find(class_='event-name').text
            date = event.find(class_='event-date').text
            venue = event.find(class_='event-venue').text
            speakers = event.find(class_='event-speakers').text
            ticket_price = event.find(class_='event-price').text

            add_event(name, date, venue, speakers, ticket_price, url)

        # Check for the next page
        next_page = soup.find(class_='next-page')
        if next_page and next_page.get('href'):
            url = next_page['href']
            time.sleep(3)
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                logging.error(f"Error fetching URL {url}: {e}")
                break
        else:
            break


def main():
    """
    Main scraping function. 
    Iterates over the list of websites to scrape and saves the data in SQLite.
    At the end, the data is exported to a CSV file.
    """
    websites = [
        'https://example-event-website1.com',
        'https://example-event-website2.com'
    ]

    for website in websites:
        if can_scrape(website):
            scrape_events(website)
            time.sleep(5)

    output_to_csv()
    print("Scraping completed!")


if __name__ == "__main__":
    main()
