# Website Crawler MVP

A Python-based web crawler that uses Playwright for dynamic interactions and BeautifulSoup for content parsing, generating comprehensive PDF reports.

## Features

**Playwright Integration** - Handles dynamic SPAs and JavaScript interactions  
**BeautifulSoup Parsing** - Extracts and analyzes HTML content  
**Interactive Crawling** - Clicks buttons and follows user actions  
**Comprehensive Logging** - Records all actions, URLs, and extracted content  
**PDF Reports** - Generates detailed visual reports of findings  

## Project Structure

```
webcrawler/
│
├── main.py                 # Entry point
├── crawler/
│   ├── __init__.py
│   ├── playwright_crawler.py
│   ├── soup_parser.py
│   ├── report_generator.py
│   └── utils/
│       └── dom_helper.js   # Optional injected JS for button discovery
│
├── requirements.txt
├── README.md
└── output/
    ├── report.pdf
    └── logs.json
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

## Usage

Run the crawler:
```bash
python main.py
```

Enter the target URL when prompted. The crawler will:
1. Load the initial page
2. Find all clickable elements (buttons, links, etc.)
3. Click each element and record the results
4. Parse content using BeautifulSoup
5. Generate a PDF report in the `output/` directory

## Output

The crawler generates two files in the `output/` directory:

- **`logs.json`** - Raw data with all actions, URLs, and parsed content
- **`report.pdf`** - Formatted report with summaries and findings

## Example Output

```
Crawl complete! Report saved to output/report.pdf
```

The PDF report includes:
- Total number of actions performed
- Each click action with URL and timestamp
- Page titles and meta descriptions
- Extracted headings and content summaries
- Important keywords using TF-IDF analysis
- Link counts and word counts
- Text content previews
- Error handling for failed actions

## Dependencies

- **playwright** - Web automation and browser control
- **beautifulsoup4** - HTML parsing and content extraction
- **scikit-learn** - Machine learning features for keyword extraction
- **lxml** - Fast XML/HTML parser for BeautifulSoup
- **fpdf2** - Lightweight PDF generation
- **requests** - HTTP requests for URL validation

## Next Steps

This MVP can be extended with:
- Recursive crawling with depth control
- Site map generation
- Content filtering and categorization
- Database storage for large-scale crawling
- Multi-threaded crawling for performance
