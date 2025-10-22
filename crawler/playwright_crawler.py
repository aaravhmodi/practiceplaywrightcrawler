from playwright.sync_api import sync_playwright
from .soup_parser import parse_html
import time
from urllib.parse import urljoin, urlparse
import json

class RecursiveWebCrawler:
    def __init__(self, max_depth=3, max_pages=50, delay=0):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.visited_buttons = set()
        self.results = []
        self.pages_to_visit = []
        self.current_depth = 0

    def crawl_website(self, start_url):
        """Main crawling method that handles recursive exploration"""
        self.pages_to_visit = [(start_url, 0)]  # (url, depth)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            
            try:
                while self.pages_to_visit and len(self.results) < self.max_pages:
                    current_url, depth = self.pages_to_visit.pop(0)
                    
                    if depth > self.max_depth or current_url in self.visited_urls:
                        continue
                        
                    self.current_depth = depth
                    print(f"\nCrawling depth {depth}: {current_url}")
                    
                    page = context.new_page()
                    try:
                        self._crawl_page(page, current_url, depth)
                    finally:
                        page.close()
                        
            finally:
                browser.close()
        
        return self.results

    def _crawl_page(self, page, url, depth):
        """Crawl a single page comprehensively"""
        try:
            # Navigate to page
            page.goto(url, wait_until='networkidle')
            time.sleep(self.delay)
            
            # Record page visit
            self.visited_urls.add(url)
            
            # Get comprehensive page data
            page_data = self._get_comprehensive_page_data(page)
            
            # Parse with BeautifulSoup
            html_content = page.content()
            parsed_data = parse_html(html_content)
            
            # Combine data
            comprehensive_data = {
                **page_data,
                **parsed_data
            }
            
            # Record initial page load
            self.results.append({
                "action": f"Loaded page (depth {depth})",
                "url": url,
                "depth": depth,
                "timestamp": time.time(),
                "data": comprehensive_data
            })
            
            print(f"Recorded page: {comprehensive_data.get('title', 'No title')}")
            
            # Find and follow links to other pages
            self._follow_links(page, url, depth)
            
            # Find and click all buttons
            self._click_all_buttons(page, url, depth)
            
        except Exception as e:
            self.results.append({
                "action": f"Failed to crawl page (depth {depth})",
                "url": url,
                "depth": depth,
                "error": str(e),
                "timestamp": time.time()
            })

    def _get_comprehensive_page_data(self, page):
        """Extract comprehensive data from the page"""
        try:
            # Basic page info
            data = {
                "title": page.title(),
                "url": page.url,
                "viewport_size": page.viewport_size,
                "load_time": time.time()
            }
            
            # JavaScript execution for dynamic data
            js_data = page.evaluate("""
                () => {
                    return {
                        document_title: document.title,
                        document_url: document.URL,
                        document_referrer: document.referrer,
                        document_domain: document.domain,
                        window_location: {
                            href: window.location.href,
                            protocol: window.location.protocol,
                            host: window.location.host,
                            pathname: window.location.pathname,
                            search: window.location.search,
                            hash: window.location.hash
                        },
                        page_ready_state: document.readyState,
                        user_agent: navigator.userAgent,
                        language: navigator.language,
                        cookie_enabled: navigator.cookieEnabled,
                        on_line: navigator.onLine,
                        screen_resolution: {
                            width: screen.width,
                            height: screen.height
                        },
                        window_size: {
                            width: window.innerWidth,
                            height: window.innerHeight
                        },
                        forms_count: document.forms.length,
                        images_count: document.images.length,
                        scripts_count: document.scripts.length,
                        stylesheets_count: document.styleSheets.length,
                        meta_tags: Array.from(document.querySelectorAll('meta')).map(meta => ({
                            name: meta.name,
                            content: meta.content,
                            property: meta.property,
                            charset: meta.charset
                        }))
                    };
                }
            """)
            
            data.update(js_data)
            return data
            
        except Exception as e:
            return {"error": f"Failed to extract page data: {str(e)}"}

    def _follow_links(self, page, current_url, depth):
        """Find and queue links to other pages"""
        try:
            # Get all links
            links = page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links.map(link => ({
                        href: link.href,
                        text: link.innerText.trim(),
                        title: link.title
                    })).filter(link => link.href && link.href !== window.location.href);
                }
            """)
            
            # Filter and add new links to visit
            for link in links:
                href = link['href']
                
                # Normalize URL
                if href.startswith('/'):
                    href = urljoin(current_url, href)
                elif not href.startswith(('http://', 'https://')):
                    href = urljoin(current_url, href)
                
                # Check if we should follow this link
                if (href not in self.visited_urls and 
                    depth < self.max_depth and
                    self._is_same_domain(current_url, href)):
                    
                    self.pages_to_visit.append((href, depth + 1))
                    print(f"Queued link: {href}")
            
        except Exception as e:
            print(f"Error following links: {e}")

    def _click_all_buttons(self, page, url, depth):
        """Click all clickable elements on the page"""
        try:
            # Get all clickable elements
            clickables = page.evaluate("""
                () => {
                    const selectors = [
                        'button:not([disabled])',
                        'a:not([href^="#"]):not([href="javascript:void(0)"])',
                        '[role="button"]:not([disabled])',
                        '[onclick]',
                        'input[type="button"]:not([disabled])',
                        'input[type="submit"]:not([disabled])',
                        '.btn:not([disabled])',
                        '.button:not([disabled])'
                    ];
                    
                    const elements = [];
                    selectors.forEach(selector => {
                        const found = document.querySelectorAll(selector);
                        found.forEach(el => {
                            if (el.offsetParent !== null) { // Check if visible
                                elements.push({
                                    tag: el.tagName,
                                    text: el.innerText?.trim() || el.value || el.getAttribute('aria-label') || 'Unnamed',
                                    type: el.type || '',
                                    href: el.href || '',
                                    onclick: el.onclick ? 'has_onclick' : '',
                                    id: el.id || '',
                                    className: el.className || ''
                                });
                            }
                        });
                    });
                    
                    return elements;
                }
            """)
            
            # Click each unique button
            for i, clickable in enumerate(clickables):
                button_id = f"{clickable['tag']}_{clickable['text']}_{clickable['type']}"
                
                if button_id not in self.visited_buttons:
                    self.visited_buttons.add(button_id)
                    
                    try:
                        print(f"Clicking [{i+1}]: {clickable['text']}")
                        
                        # Find and click the element
                        element = page.query_selector(f"text={clickable['text']}")
                        if not element:
                            # Try by tag and text combination
                            element = page.query_selector(f"{clickable['tag'].lower()}:has-text('{clickable['text']}')")
                        
                        if element:
                            element.click()
                            time.sleep(self.delay)
                            
                            # Check if page changed
                            new_url = page.url
                            if new_url != url:
                                # Page navigated - record new page
                                self._record_page_after_click(page, clickable, url, new_url, depth)
                            else:
                                # Same page - check for content changes
                                self._record_content_change(page, clickable, url, depth)
                        
                    except Exception as e:
                        self.results.append({
                            "action": f"Failed to click button: {clickable['text']}",
                            "url": url,
                            "depth": depth,
                            "error": str(e),
                            "timestamp": time.time()
                        })
                        
        except Exception as e:
            print(f"Error clicking buttons: {e}")

    def _record_page_after_click(self, page, clickable, old_url, new_url, depth):
        """Record the new page after a click that caused navigation"""
        try:
            html_content = page.content()
            parsed_data = parse_html(html_content)
            page_data = self._get_comprehensive_page_data(page)
            
            comprehensive_data = {
                **page_data,
                **parsed_data
            }
            
            self.results.append({
                "action": f"Clicked '{clickable['text']}' - Navigated to new page",
                "url": new_url,
                "previous_url": old_url,
                "depth": depth,
                "clicked_element": clickable,
                "timestamp": time.time(),
                "data": comprehensive_data
            })
            
            # Add new page to visit queue if not visited
            if new_url not in self.visited_urls and depth < self.max_depth:
                self.pages_to_visit.append((new_url, depth + 1))
                
        except Exception as e:
            print(f"Error recording page after click: {e}")

    def _record_content_change(self, page, clickable, url, depth):
        """Record content changes on the same page after a click"""
        try:
            html_content = page.content()
            parsed_data = parse_html(html_content)
            
            self.results.append({
                "action": f"Clicked '{clickable['text']}' - Content changed",
                "url": url,
                "depth": depth,
                "clicked_element": clickable,
                "timestamp": time.time(),
                "data": parsed_data
            })
            
        except Exception as e:
            print(f"Error recording content change: {e}")

    def _is_same_domain(self, url1, url2):
        """Check if two URLs are from the same domain"""
        try:
            domain1 = urlparse(url1).netloc
            domain2 = urlparse(url2).netloc
            return domain1 == domain2
        except:
            return False

def crawl_website(start_url, max_depth=3, max_pages=50, delay=0):
    """Main function to start recursive crawling"""
    crawler = RecursiveWebCrawler(max_depth=max_depth, max_pages=max_pages, delay=delay)
    return crawler.crawl_website(start_url)
