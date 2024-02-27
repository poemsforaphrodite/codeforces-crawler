# Codeforces Problem Scraper

This is a Python script that uses the Apify platform to scrape problem information from Codeforces. The script reads start URLs from a `url.txt` file, and then it runs an Apify actor with a custom page function to extract the problem's title, statement, input, and output. The extracted information is then saved to a `main_info.json` file.

## Prerequisites

- Python 3.x
- Apify account with API key
- `apify_client` Python package

## Installation

1. Install the `apify_client` package using pip:

```bash
pip install apify_client
```
Set your Apify API key as an environment variable:
```bash
export APIFY_API_KEY=your_api_key_here
```
Usage
Create a url.txt file with the URLs you want to scrape, one URL per line.
Run the script:
```bash
python scraper.py
```

The script will output a main_info.json file with the extracted problem information.
Customization

The script uses a custom page function to extract the problem's title, statement, input, and output. You can modify this function to extract different information or to handle different websites.
Contributing
