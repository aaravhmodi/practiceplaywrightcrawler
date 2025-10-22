import pytest
from crawler.soup_parser import parse_html, extract_keywords

def test_parse_html_basic():
    """Test basic HTML parsing"""
    html = """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Main Heading</h1>
            <h2>Sub Heading</h2>
            <p>This is a test paragraph with some content.</p>
            <a href="https://example.com">Link 1</a>
            <a href="/internal">Link 2</a>
            <img src="image.jpg" alt="Test Image">
            <form action="/submit" method="post">
                <input type="text" name="username">
                <input type="password" name="password">
            </form>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    assert result["title"] == "Test Page"
    assert result["meta_description"] == "Test description"
    assert len(result["headings"]) == 2
    assert "Main Heading" in result["headings"]
    assert len(result["links"]) == 2
    assert len(result["images"]) == 1
    assert len(result["forms"]) == 1
    assert result["word_count"] > 0

def test_parse_html_with_navigation():
    """Test HTML parsing with navigation structure"""
    html = """
    <html>
        <body>
            <header><h1>Header</h1></header>
            <nav><a href="/home">Home</a></nav>
            <main><p>Main content</p></main>
            <footer><p>Footer</p></footer>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    assert result["page_structure"]["has_header"] == True
    assert result["page_structure"]["has_navigation"] == True
    assert result["page_structure"]["has_main"] == True
    assert result["page_structure"]["has_footer"] == True

def test_parse_html_empty():
    """Test parsing empty HTML"""
    html = "<html><body></body></html>"
    
    result = parse_html(html)
    
    assert result["title"] == "No title"
    assert len(result["headings"]) == 0
    assert len(result["paragraphs"]) == 0

def test_extract_keywords():
    """Test keyword extraction"""
    text = "business professional services quality company team development innovation technology"
    
    keywords = extract_keywords(text)
    
    assert isinstance(keywords, list)
    assert len(keywords) > 0

def test_parse_html_with_forms():
    """Test form parsing"""
    html = """
    <html>
        <body>
            <form action="/login" method="post">
                <input type="email" name="email" placeholder="Enter email" required>
                <input type="password" name="pass">
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    assert len(result["forms"]) == 1
    form = result["forms"][0]
    assert form["action"] == "/login"
    assert form["method"] == "post"
    assert len(form["inputs"]) == 3

def test_parse_html_with_lists():
    """Test list parsing"""
    html = """
    <html>
        <body>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
            <ol>
                <li>Ordered 1</li>
            </ol>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    assert len(result["lists"]) == 2
    assert result["lists"][0]["type"] == "ul"
    assert result["lists"][1]["type"] == "ol"

def test_parse_html_social_links():
    """Test social media link detection"""
    html = """
    <html>
        <body>
            <a href="https://facebook.com/page">Facebook</a>
            <a href="https://twitter.com/user">Twitter</a>
            <a href="https://linkedin.com/company">LinkedIn</a>
        </body>
    </html>
    """
    
    result = parse_html(html)
    
    assert len(result["social_links"]) == 3
    platforms = [link["platform"] for link in result["social_links"]]
    assert "facebook" in platforms
    assert "twitter" in platforms
    assert "linkedin" in platforms
