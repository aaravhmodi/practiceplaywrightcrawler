import pytest
from crawler.website_comparator import WebsiteComparator

def test_website_comparator_init():
    """Test WebsiteComparator initialization"""
    comparator = WebsiteComparator(max_depth=2, max_pages=10, delay=0)
    
    assert comparator.max_depth == 2
    assert comparator.max_pages == 10
    assert comparator.delay == 0
    assert isinstance(comparator.website1_data, dict)
    assert isinstance(comparator.website2_data, dict)

def test_calculate_percentage_difference():
    """Test percentage difference calculation"""
    comparator = WebsiteComparator()
    
    # Test positive difference
    result = comparator._calculate_percentage_difference(100, 50)
    assert result == 100.0
    
    # Test negative difference
    result = comparator._calculate_percentage_difference(50, 100)
    assert result == -50.0
    
    # Test zero values
    result = comparator._calculate_percentage_difference(0, 0)
    assert result == 0

def test_calculate_keyword_similarity():
    """Test keyword similarity calculation"""
    comparator = WebsiteComparator()
    
    # Setup test data
    comparator.website1_data = {"unique_keywords": ["test", "python", "code"]}
    comparator.website2_data = {"unique_keywords": ["test", "python", "javascript"]}
    
    result = comparator._calculate_keyword_similarity()
    
    assert isinstance(result, float)
    assert 0 <= result <= 100

def test_calculate_content_richness():
    """Test content richness calculation"""
    comparator = WebsiteComparator()
    
    test_data = {
        "total_word_count": 5000,
        "total_images": 10,
        "total_forms": 3,
        "total_tables": 2,
        "total_lists": 5,
        "unique_keywords": ["word"] * 20
    }
    
    score = comparator._calculate_content_richness(test_data)
    
    assert isinstance(score, float)
    assert score > 0

def test_calculate_interactivity():
    """Test interactivity calculation"""
    comparator = WebsiteComparator()
    
    test_data = {
        "total_forms": 5,
        "all_links": ["link"] * 50,
        "pages": [{"url": "test"}] * 10
    }
    
    score = comparator._calculate_interactivity(test_data)
    
    assert isinstance(score, float)
    assert score > 0

def test_calculate_seo_score():
    """Test SEO score calculation"""
    comparator = WebsiteComparator()
    
    test_data = {
        "meta_tags": [{"name": "test"}] * 10,
        "unique_keywords": ["keyword"] * 30,
        "total_word_count": 3000,
        "all_links": ["link"] * 25
    }
    
    score = comparator._calculate_seo_score(test_data)
    
    assert isinstance(score, float)
    assert score > 0

def test_is_same_domain():
    """Test domain comparison"""
    comparator = WebsiteComparator()
    
    assert comparator.is_same_domain("https://example.com/page1", "https://example.com/page2") == True
    assert comparator.is_same_domain("https://example.com", "https://different.com") == False
    assert comparator.is_same_domain("http://test.com", "https://test.com") == True

def test_detect_technologies():
    """Test technology detection"""
    comparator = WebsiteComparator()
    
    data = {"technologies_detected": set()}
    
    page_data = {
        "meta_tags": [
            {"name": "generator", "content": "WordPress 5.8"},
            {"name": "viewport", "content": "width=device-width"},
            {"property": "og:title", "content": "Test"}
        ]
    }
    
    comparator._detect_technologies(page_data, data)
    
    assert "WordPress" in data["technologies_detected"]
    assert "Responsive Design" in data["technologies_detected"]
    assert "Open Graph" in data["technologies_detected"]
