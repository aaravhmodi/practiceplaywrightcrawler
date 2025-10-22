from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1","h2","h3"]) if h.get_text(strip=True)]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    links = [a.get("href") for a in soup.find_all("a", href=True) if a.get("href")]

    # Get all visible text for word count and analysis
    visible_text = soup.get_text()
    words = visible_text.split()
    word_count = len(words)
    
    # Extract important keywords using TF-IDF
    important_words = extract_keywords(visible_text)
    
    # Extract meta information
    meta_description = ""
    meta_tags = soup.find_all("meta")
    for meta in meta_tags:
        if meta.get("name") == "description":
            meta_description = meta.get("content", "")
            break

    # Extract forms data
    forms_data = []
    for form in soup.find_all('form'):
        form_info = {
            'action': form.get('action', ''),
            'method': form.get('method', 'get'),
            'inputs': []
        }
        for input_field in form.find_all('input'):
            form_info['inputs'].append({
                'type': input_field.get('type', 'text'),
                'name': input_field.get('name', ''),
                'placeholder': input_field.get('placeholder', ''),
                'required': input_field.has_attr('required')
            })
        forms_data.append(form_info)

    # Extract images data
    images_data = []
    for img in soup.find_all('img'):
        images_data.append({
            'src': img.get('src', ''),
            'alt': img.get('alt', ''),
            'width': img.get('width', ''),
            'height': img.get('height', ''),
            'title': img.get('title', '')
        })

    # Extract tables data
    tables_data = []
    for table in soup.find_all('table'):
        table_info = {
            'rows': len(table.find_all('tr')),
            'headers': [th.get_text(strip=True) for th in table.find_all('th')]
        }
        tables_data.append(table_info)

    # Extract lists data
    lists_data = []
    for ul in soup.find_all(['ul', 'ol']):
        list_items = [li.get_text(strip=True) for li in ul.find_all('li')]
        lists_data.append({
            'type': ul.name,
            'items': list_items[:10]  # Limit to first 10 items
        })

    # Extract all text content for analysis
    all_text = soup.get_text()
    sentences = [s.strip() for s in all_text.split('.') if s.strip()]
    
    # Extract social media links
    social_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(social in href.lower() for social in ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']):
            social_links.append({
                'platform': next(social for social in ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube'] if social in href.lower()),
                'url': href
            })

    return {
        "headings": headings[:10],
        "paragraphs": paragraphs[:5],
        "links": links[:20],
        "word_count": word_count,
        "title": soup.title.string if soup.title else "No title",
        "meta_description": meta_description,
        "important_words": important_words[:15],
        "text_content": visible_text[:1000] + "..." if len(visible_text) > 1000 else visible_text,
        "forms": forms_data,
        "images": images_data[:10],
        "tables": tables_data,
        "lists": lists_data[:5],
        "sentences_count": len(sentences),
        "social_links": social_links,
        "total_elements": {
            "headings": len(headings),
            "paragraphs": len(paragraphs),
            "links": len(links),
            "images": len(images_data),
            "forms": len(forms_data),
            "tables": len(tables_data),
            "lists": len(lists_data)
        },
        "page_structure": {
            "has_navigation": bool(soup.find('nav')),
            "has_footer": bool(soup.find('footer')),
            "has_header": bool(soup.find('header')),
            "has_main": bool(soup.find('main')),
            "has_aside": bool(soup.find('aside'))
        }
    }

def extract_keywords(text, max_features=20):
    """Extract important keywords using TF-IDF"""
    try:
        # Clean and prepare text
        cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [word for word in cleaned_text.split() if len(word) > 3]
        
        if not words:
            return []
            
        # Use TF-IDF to find important terms
        vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([' '.join(words)])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top terms by TF-IDF scores
        scores = tfidf_matrix.toarray()[0]
        word_scores = list(zip(feature_names, scores))
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [word for word, score in word_scores if score > 0]
    except:
        return []
