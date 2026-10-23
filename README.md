# Web Crawler and Data Extraction

A Python-based web crawler that collects structured information from web pages, follows links within the same domain, avoids duplicate URLs, respects `robots.txt`, and exports extracted data to JSON and CSV files.

## Features

- Fetches web pages using Requests.
- Extracts page titles, meta descriptions, headings, text, links, and timestamps.
- Follows same-domain links by default.
- Normalizes URLs and avoids duplicate visits.
- Checks `robots.txt` before crawling.
- Supports page limits, request delays, and timeouts.
- Handles HTTP errors and network failures.
- Exports crawled data to JSON and CSV.
- Includes automated unit tests and sample output files.

## Technology Stack

- Python 3.10+
- Requests
- BeautifulSoup4
- unittest

## Project Structure

```text
Web Crawler Data Extraction/
|-- main.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- web_crawler/
|   |-- __init__.py
|   |-- crawler.py
|   |-- extractor.py
|   |-- exporter.py
|   |-- url_utils.py
|-- tests/
|   |-- test_extractor.py
|   |-- test_url_utils.py
|   |-- test_exporter.py
|-- output/
    |-- sample_data.json
    |-- sample_data.csv
```

## Requirements

- Python 3.10 or later
- An internet connection for live crawling
- pip for installing dependencies

## Installation on Windows

Open PowerShell in the project directory.

Activate the existing virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

If you have not created a virtual environment yet, create one first:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the Crawler

Example using the Quotes to Scrape demo website:

```powershell
python main.py https://quotes.toscrape.com/ --max-pages 5 --delay 1
```

This command requests up to five pages with a one-second delay between requests. Actual results depend on network connectivity and the website's availability and crawling rules.

To see the available command-line options, run:

```powershell
python main.py --help
```

## Run Automated Tests

Run the unit tests with Python's built-in unittest framework:

```powershell
python -m unittest discover -s tests -v
```

The tests cover URL utilities, content extraction, and data export functionality.

## Output Files

The crawler writes its generated files to the `output/` directory:

- `crawled_data.json` — extracted page data in JSON format.
- `crawled_data.csv` — extracted page data in CSV format.
- `crawler.log` — crawl activity, warnings, and errors.

Sample output files are also included for demonstration.

## Responsible Crawling

- Crawl only websites you are permitted to access.
- Respect each website's `robots.txt`, terms, and rate limits.
- Use reasonable page limits and request delays.
- Do not bypass authentication, paywalls, or access restrictions.
- Network or DNS failures may prevent a live crawl from completing.

## Troubleshooting

If a live crawl fails because of a network or DNS error, check your internet connection and try again later. A failed live crawl does not automatically mean the unit tests or extraction code are broken.

If a test fails, review the error output and verify that the project dependencies are installed.