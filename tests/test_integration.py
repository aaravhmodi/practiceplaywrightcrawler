import pytest
from crawler.soup_parser import parse_html
from crawler.website_comparator import WebsiteComparator

def test_full_html_parsing_pipeline():
    """Test complete HTML parsing pipeline"""
    html = """
    <html>
        <head>
            <title>Integration Test Page</title>
            <meta name="description" content="Testing the crawler">
            <meta name="generator" content="WordPress">
        </head>
        <body>
            <header>
                <nav>
                    <a href="/home">Home</a>
                    <a href="/about">About</a>
                </nav>
            </header>
            <main>
                <h1>Welcome to Testing</h1>
                <p>This is a comprehensive test of the web crawler functionality.</p>
                <p>It includes multiple paragraphs to test content extraction.</p>
                <img src="test.jpg" alt="Test Image">
                <form action="/search" method="get">
                    <input type="text" name="q" placeholder="Search...">
                    <input type="submit" value="Search">
                </form>
                <ul>
                    <li>Feature 1</li>
                    <li>Feature 2</li>
                </ul>
            </main>
            <footer>
                <a href="https://facebook.com/page">Facebook</a>
                <p>Copyright 2024</p>
            </footer>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    # Check all major components
    assert result["title"] == "Integration Test Page"
    assert result["meta_description"] == "Testing the crawler"
    assert len(result["headings"]) >= 1
    assert len(result["paragraphs"]) >= 2
    assert len(result["links"]) >= 2
    assert len(result["images"]) >= 1
    assert len(result["forms"]) >= 1
    assert len(result["lists"]) >= 1
    assert result["page_structure"]["has_header"] == True
    assert result["page_structure"]["has_navigation"] == True
    assert result["page_structure"]["has_main"] == True
    assert result["page_structure"]["has_footer"] == True
    assert len(result["social_links"]) >= 1
    assert result["word_count"] > 0

def test_comparison_workflow():
    """Test the comparison workflow components"""
    comparator = WebsiteComparator(max_depth=1, max_pages=5, delay=0)
    
    # Test data processing
    mock_logs = [
        {
            "url": "https://test.com",
            "data": {
                "title": "Test Page",
                "links": ["https://test.com/link1", "https://test.com/link2"],
                "forms": [{"method": "post", "inputs": [{"type": "text"}]}],
                "images": [{"src": "image.jpg", "alt": "Test"}],
                "word_count": 500,
                "important_words": ["test", "example"],
                "page_structure": {"has_navigation": True, "has_header": True}
            }
        }
    ]
    
    result = comparator._process_website_data(mock_logs, "https://test.com")
    
    assert result["base_url"] == "https://test.com"
    assert result["domain"] == "test.com"
    assert len(result["pages"]) == 1
    assert result["total_word_count"] == 500
    assert len(result["all_links"]) == 2
    assert result["total_forms"] == 1
    assert result["total_images"] == 1

def test_empty_html_handling():
    """Test handling of empty or minimal HTML"""
    html = "<html></html>"
    
    result = parse_html(html)
    
    assert result["title"] == "No title"
    assert len(result["headings"]) == 0
    assert len(result["paragraphs"]) == 0
    assert result["word_count"] >= 0

def test_malformed_html_handling():
    """Test handling of malformed HTML"""
    html = "<html><body><h1>Unclosed heading<p>Paragraph</body>"
    
    # Should not raise an exception
    result = parse_html(html)
    
    assert isinstance(result, dict)
    assert "headings" in result
    assert "paragraphs" in result
