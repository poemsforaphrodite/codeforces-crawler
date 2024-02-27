import json
import os
from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
my_secret = os.environ['APIFY_API_KEY']
client = ApifyClient(my_secret)

# Read start URLs from url.txt file
with open('url.txt', 'r') as file:
  start_urls = file.readlines()
  start_urls = [url.strip() for url in start_urls]

# Prepare the Actor input with the provided page function
run_input = {
    "runMode": "DEVELOPMENT",
    "startUrls": [{
        "url": url
    } for url in start_urls],
    "keepUrlFragments": False,
    "linkSelector": "a[href]",
    "globs": [
        {
            "glob": "https://codeforces.com/problemset/problem/1/[A-C]"
        },
    ],
    "pseudoUrls": [],
    "excludes": [{
        "glob": "/**/*.{png,jpg,jpeg,pdf}"
    }],
    "pageFunction": """
    async function pageFunction(context) {
        // jQuery is handy for finding DOM elements and extracting data from them.
        // To use it, make sure to enable the "Inject jQuery" option.
        const $ = context.jQuery;
        const pageTitle = $('title').first().text();
        const title = $('.title:first').text();
        const problemStatement = $('.problem-statement p').text().trim(); 
        const sampleTests = $('.sample-tests').text();

        // Select input and output sections and extract their text content
        const input = $('.input').find('pre').text().trim(); // Assuming input is wrapped in <pre> tags
        const output = $('.output').find('pre').text().trim(); // Assuming output is wrapped in <pre> tags

        // Return an object with the data extracted from the page.
        // It will be stored to the resulting dataset.
        return {
            title,
            problemStatement,
            input,
            output
        };
    }
    """,
    "injectJQuery": True,
    "proxyConfiguration": {
        "useApifyProxy": True
    },
    "proxyRotation": "RECOMMENDED",
    "initialCookies": [],
    "useChrome": False,
    "headless": True,
    "ignoreSslErrors": False,
    "ignoreCorsAndCsp": False,
    "downloadMedia": True,
    "downloadCss": True,
    "maxRequestRetries": 3,
    "maxPagesPerCrawl": 0,
    "maxResultsPerCrawl": 0,
    "maxCrawlingDepth": 0,
    "maxConcurrency": 50,
    "pageLoadTimeoutSecs": 60,
    "pageFunctionTimeoutSecs": 60,
    "waitUntil": ["networkidle2"],
    "preNavigationHooks": """[
        async (crawlingContext, gotoOptions) => {
            // ...
        },
    ]""",
    "postNavigationHooks": """[
        async (crawlingContext) => {
            // ...
        },
    ]""",
    "breakpointLocation": "NONE",
    "closeCookieModals": False,
    "maxScrollHeightPixels": 5000,
    "debugLog": False,
    "browserLog": False,
    "customData": {},
}

# Run the Actor and wait for it to finish
run = client.actor("moJRLRc85AitArpNN").call(run_input=run_input)

# Fetch Actor results from the run's dataset
results = [
    item for item in client.dataset(run["defaultDatasetId"]).iterate_items()
]

# Filter out main information
main_info = []
for result in results:
  main_info.append({
      "title": result["title"],
      "problemStatement": result["problemStatement"],
      "input": result["input"],
      "output": result["output"]
  })

# Save main information to a JSON file
with open('main_info.json', 'w') as json_file:
  json.dump(main_info, json_file)

print("Main information saved to main_info.json")
