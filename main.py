from crawler.playwright_crawler import crawl_website
from crawler.report_generator import generate_report
from crawler.website_comparator import WebsiteComparator
from crawler.comparison_report_generator import ComparisonReportGenerator
import json
import os
import requests
from urllib.parse import urljoin, urlparse

def validate_url(url):
    """Validate and normalize URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        response = requests.head(url, timeout=10)
        return url, response.status_code
    except requests.RequestException as e:
        print(f"Warning: Could not validate URL {url}: {e}")
        return url, None

def main():
    # Choose mode
    print("Website Crawler - Choose Mode:")
    print("1. Single website crawl")
    print("2. Compare two websites")
    
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == "2":
        compare_websites()
    else:
        crawl_single_website()

def crawl_single_website():
    """Crawl a single website"""
    url = input("Enter URL to crawl: ").strip()
    
    # Get crawling configuration
    print("\nCrawling Configuration:")
    try:
        max_depth = int(input("Max depth (default 3): ") or "3")
        max_pages = int(input("Max pages to crawl (default 50): ") or "50")
        delay = 0  # No delay, we go fast!
    except ValueError:
        max_depth, max_pages, delay = 3, 50, 0
        print("Using default values: depth=3, max_pages=50, delay=0 (NO DELAY!)")
    
    # Validate URL
    url, status_code = validate_url(url)
    print(f"\nTarget URL: {url}")
    if status_code:
        print(f"URL Status: {status_code}")
    
    # Start crawling
    print(f"\nStarting recursive crawl process...")
    print(f"Configuration: depth={max_depth}, max_pages={max_pages}, delay={delay}s")
    logs = crawl_website(url, max_depth=max_depth, max_pages=max_pages, delay=delay)

    # Save results
    os.makedirs("output", exist_ok=True)
    with open("output/logs.json", "w", encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    # Generate report
    generate_report(logs, "output/report.pdf")
    print("\nCrawl complete! Report saved to output/report.pdf")
    
    # Print comprehensive summary
    total_actions = len(logs)
    successful_actions = len([log for log in logs if 'error' not in log])
    pages_visited = len(set(log.get('url', '') for log in logs))
    buttons_clicked = len([log for log in logs if 'clicked' in log.get('action', '').lower()])
    
    print(f"\nCRAWLING SUMMARY:")
    print(f"   • Total actions: {total_actions}")
    print(f"   • Successful actions: {successful_actions}")
    print(f"   • Pages visited: {pages_visited}")
    print(f"   • Buttons clicked: {buttons_clicked}")
    print(f"   • Unique URLs discovered: {len(set(log.get('url', '') for log in logs))}")
    print(f"   • Files saved: output/logs.json, output/report.pdf")

def compare_websites():
    """Compare two websites"""
    print("\nWebsite Comparison Mode")
    print("=" * 40)
    
    # Get URLs
    url1 = input("Enter first website URL: ").strip()
    url2 = input("Enter second website URL: ").strip()
    
    # Get comparison configuration
    print("\nComparison Configuration:")
    try:
        max_depth = int(input("Max depth for each site (default 2): ") or "2")
        max_pages = int(input("Max pages per site (default 30): ") or "30")
        delay = 0  # No delay, we go fast!
    except ValueError:
        max_depth, max_pages, delay = 2, 30, 0
        print("Using default values: depth=2, max_pages=30, delay=0 (NO DELAY!)")
    
    # Validate URLs
    url1, status1 = validate_url(url1)
    url2, status2 = validate_url(url2)
    
    print(f"\nWebsite 1: {url1}")
    if status1:
        print(f"URL Status: {status1}")
    print(f"Website 2: {url2}")
    if status2:
        print(f"URL Status: {status2}")
    
    # Start comparison
    print(f"\nStarting website comparison...")
    print(f"Configuration: depth={max_depth}, max_pages={max_pages}, delay={delay}s")
    
    comparator = WebsiteComparator(max_depth=max_depth, max_pages=max_pages, delay=delay)
    comparison_data = comparator.compare_websites(url1, url2)
    
    # Save results
    os.makedirs("output", exist_ok=True)
    
    # Save detailed comparison data
    with open("output/comparison_data.json", "w", encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)
    
    # Save individual website logs
    with open("output/website1_logs.json", "w", encoding='utf-8') as f:
        json.dump(comparison_data["website1_logs"], f, indent=2, ensure_ascii=False)
    
    with open("output/website2_logs.json", "w", encoding='utf-8') as f:
        json.dump(comparison_data["website2_logs"], f, indent=2, ensure_ascii=False)
    
    # Generate comparison report
    report_generator = ComparisonReportGenerator()
    report_generator.generate_comparison_report(comparison_data, "output/comparison_report.pdf")
    
    print("\nComparison complete! Reports saved:")
    print("   • output/comparison_report.pdf - Main comparison report")
    print("   • output/comparison_data.json - Detailed comparison data")
    print("   • output/website1_logs.json - Website 1 crawl logs")
    print("   • output/website2_logs.json - Website 2 crawl logs")
    
    # Print comparison summary
    comparison = comparison_data["comparison"]
    overview = comparison["overview"]
    
    print(f"\nCOMPARISON SUMMARY:")
    print(f"   • Website 1 pages: {overview['website1_pages']}")
    print(f"   • Website 2 pages: {overview['website2_pages']}")
    print(f"   • Website 1 words: {overview['website1_total_words']:,}")
    print(f"   • Website 2 words: {overview['website2_total_words']:,}")
    print(f"   • Website 1 links: {overview['website1_total_links']}")
    print(f"   • Website 2 links: {overview['website2_total_links']}")
    
    # Key differences
    content_diff = comparison["content_differences"]["word_count"]["difference"]
    page_diff = comparison["structure_differences"]["pages_count"]["difference"]
    
    print(f"\nKEY DIFFERENCES:")
    if content_diff != 0:
        print(f"   • Content volume difference: {content_diff:,} words")
    if page_diff != 0:
        print(f"   • Page count difference: {page_diff} pages")
    
    # Show winners
    richness_winner = comparison["detailed_analysis"]["content_richness"]["winner"]
    interactivity_winner = comparison["detailed_analysis"]["interactivity_level"]["winner"]
    seo_winner = comparison["detailed_analysis"]["seo_indicators"]["winner"]
    
    print(f"\nANALYSIS RESULTS:")
    print(f"   • Content richness winner: {richness_winner}")
    print(f"   • Interactivity winner: {interactivity_winner}")
    print(f"   • SEO optimization winner: {seo_winner}")

if __name__ == "__main__":
    main()
