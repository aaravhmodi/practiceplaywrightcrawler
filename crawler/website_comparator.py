from .soup_parser import parse_html
from .playwright_crawler import RecursiveWebCrawler
import time
from urllib.parse import urlparse
import json

class WebsiteComparator:
    def __init__(self, max_depth=2, max_pages=30, delay=0):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.website1_data = {}
        self.website2_data = {}
        self.comparison_results = {}

    def compare_websites(self, url1, url2):
        """Compare two websites comprehensively"""
        print(f"Starting comparison between {url1} and {url2}")
        
        # Crawl both websites
        print("\nCrawling Website 1...")
        crawler1 = RecursiveWebCrawler(self.max_depth, self.max_pages, self.delay)
        website1_logs = crawler1.crawl_website(url1)
        
        print("\nCrawling Website 2...")
        crawler2 = RecursiveWebCrawler(self.max_depth, self.max_pages, self.delay)
        website2_logs = crawler2.crawl_website(url2)
        
        # Process and analyze data
        self.website1_data = self._process_website_data(website1_logs, url1)
        self.website2_data = self._process_website_data(website2_logs, url2)
        
        # Generate comparison
        self.comparison_results = self._generate_comparison()
        
        return {
            "website1": self.website1_data,
            "website2": self.website2_data,
            "comparison": self.comparison_results,
            "website1_logs": website1_logs,
            "website2_logs": website2_logs
        }

    def _process_website_data(self, logs, base_url):
        """Process raw crawl logs into structured data"""
        data = {
            "base_url": base_url,
            "domain": urlparse(base_url).netloc,
            "pages": [],
            "all_links": set(),
            "all_buttons": set(),
            "all_forms": [],
            "all_images": [],
            "all_tables": [],
            "all_lists": [],
            "social_links": [],
            "meta_tags": [],
            "total_word_count": 0,
            "total_images": 0,
            "total_forms": 0,
            "total_tables": 0,
            "total_lists": 0,
            "unique_keywords": set(),
            "page_titles": set(),
            "navigation_structure": set(),
            "content_types": set(),
            "technologies_detected": set(),
            "errors": []
        }
        
        for log in logs:
            if "data" in log and log["data"]:
                page_data = log["data"]
                
                # Extract page information
                if page_data.get("title"):
                    data["page_titles"].add(page_data["title"])
                
                # Collect all links
                if page_data.get("links"):
                    data["all_links"].update(page_data["links"])
                
                # Collect forms
                if page_data.get("forms"):
                    data["all_forms"].extend(page_data["forms"])
                    data["total_forms"] += len(page_data["forms"])
                
                # Collect images
                if page_data.get("images"):
                    data["all_images"].extend(page_data["images"])
                    data["total_images"] += len(page_data["images"])
                
                # Collect tables
                if page_data.get("tables"):
                    data["all_tables"].extend(page_data["tables"])
                    data["total_tables"] += len(page_data["tables"])
                
                # Collect lists
                if page_data.get("lists"):
                    data["all_lists"].extend(page_data["lists"])
                    data["total_lists"] += len(page_data["lists"])
                
                # Collect social links
                if page_data.get("social_links"):
                    data["social_links"].extend(page_data["social_links"])
                
                # Collect meta tags
                if page_data.get("meta_tags"):
                    data["meta_tags"].extend(page_data["meta_tags"])
                
                # Word count
                if page_data.get("word_count"):
                    data["total_word_count"] += page_data["word_count"]
                
                # Keywords
                if page_data.get("important_words"):
                    data["unique_keywords"].update(page_data["important_words"])
                
                # Navigation structure
                if page_data.get("page_structure"):
                    structure = page_data["page_structure"]
                    for key, value in structure.items():
                        if value:
                            data["navigation_structure"].add(key.replace("has_", ""))
                
                # Detect technologies
                self._detect_technologies(page_data, data)
                
                # Store page data
                data["pages"].append({
                    "url": log.get("url", ""),
                    "title": page_data.get("title", ""),
                    "word_count": page_data.get("word_count", 0),
                    "links_count": len(page_data.get("links", [])),
                    "images_count": len(page_data.get("images", [])),
                    "forms_count": len(page_data.get("forms", [])),
                    "headings": page_data.get("headings", []),
                    "keywords": page_data.get("important_words", [])
                })
            
            # Collect errors
            if "error" in log:
                data["errors"].append({
                    "url": log.get("url", ""),
                    "error": log["error"],
                    "action": log.get("action", "")
                })
        
        # Convert sets to lists for JSON serialization
        data["all_links"] = list(data["all_links"])
        data["unique_keywords"] = list(data["unique_keywords"])
        data["page_titles"] = list(data["page_titles"])
        data["navigation_structure"] = list(data["navigation_structure"])
        data["content_types"] = list(data["content_types"])
        data["technologies_detected"] = list(data["technologies_detected"])
        
        return data

    def _detect_technologies(self, page_data, data):
        """Detect technologies used on the page"""
        # Check for common technologies in meta tags
        if page_data.get("meta_tags"):
            for meta in page_data["meta_tags"]:
                content = meta.get("content", "").lower()
                name = meta.get("name", "").lower()
                property_name = meta.get("property", "").lower()
                
                # Detect frameworks and technologies
                if "generator" in name and content:
                    if "wordpress" in content:
                        data["technologies_detected"].add("WordPress")
                    elif "drupal" in content:
                        data["technologies_detected"].add("Drupal")
                    elif "joomla" in content:
                        data["technologies_detected"].add("Joomla")
                
                if "viewport" in name:
                    data["technologies_detected"].add("Responsive Design")
                
                if "og:" in property_name:
                    data["technologies_detected"].add("Open Graph")
                
                if "twitter:" in property_name:
                    data["technologies_detected"].add("Twitter Cards")

    def _generate_comparison(self):
        """Generate comprehensive comparison between websites"""
        comparison = {
            "overview": {},
            "structure_differences": {},
            "content_differences": {},
            "technical_differences": {},
            "functionality_differences": {},
            "detailed_analysis": {}
        }
        
        # Overview comparison
        comparison["overview"] = {
            "website1_domain": self.website1_data["domain"],
            "website2_domain": self.website2_data["domain"],
            "website1_pages": len(self.website1_data["pages"]),
            "website2_pages": len(self.website2_data["pages"]),
            "website1_total_words": self.website1_data["total_word_count"],
            "website2_total_words": self.website2_data["total_word_count"],
            "website1_total_links": len(self.website1_data["all_links"]),
            "website2_total_links": len(self.website2_data["all_links"])
        }
        
        # Structure differences
        comparison["structure_differences"] = {
            "pages_count": {
                "website1": len(self.website1_data["pages"]),
                "website2": len(self.website2_data["pages"]),
                "difference": len(self.website1_data["pages"]) - len(self.website2_data["pages"])
            },
            "navigation_structure": {
                "website1": self.website1_data["navigation_structure"],
                "website2": self.website2_data["navigation_structure"],
                "unique_to_website1": list(set(self.website1_data["navigation_structure"]) - set(self.website2_data["navigation_structure"])),
                "unique_to_website2": list(set(self.website2_data["navigation_structure"]) - set(self.website1_data["navigation_structure"])),
                "common": list(set(self.website1_data["navigation_structure"]) & set(self.website2_data["navigation_structure"]))
            },
            "page_titles": {
                "website1": self.website1_data["page_titles"],
                "website2": self.website2_data["page_titles"],
                "unique_to_website1": list(set(self.website1_data["page_titles"]) - set(self.website2_data["page_titles"])),
                "unique_to_website2": list(set(self.website2_data["page_titles"]) - set(self.website1_data["page_titles"])),
                "common": list(set(self.website1_data["page_titles"]) & set(self.website2_data["page_titles"]))
            }
        }
        
        # Content differences
        comparison["content_differences"] = {
            "word_count": {
                "website1": self.website1_data["total_word_count"],
                "website2": self.website2_data["total_word_count"],
                "difference": self.website1_data["total_word_count"] - self.website2_data["total_word_count"],
                "percentage_difference": self._calculate_percentage_difference(
                    self.website1_data["total_word_count"], 
                    self.website2_data["total_word_count"]
                )
            },
            "keywords": {
                "website1": self.website1_data["unique_keywords"],
                "website2": self.website2_data["unique_keywords"],
                "unique_to_website1": list(set(self.website1_data["unique_keywords"]) - set(self.website2_data["unique_keywords"])),
                "unique_to_website2": list(set(self.website2_data["unique_keywords"]) - set(self.website1_data["unique_keywords"])),
                "common": list(set(self.website1_data["unique_keywords"]) & set(self.website2_data["unique_keywords"])),
                "similarity_percentage": self._calculate_keyword_similarity()
            },
            "content_elements": {
                "images": {
                    "website1": self.website1_data["total_images"],
                    "website2": self.website2_data["total_images"],
                    "difference": self.website1_data["total_images"] - self.website2_data["total_images"]
                },
                "forms": {
                    "website1": self.website1_data["total_forms"],
                    "website2": self.website2_data["total_forms"],
                    "difference": self.website1_data["total_forms"] - self.website2_data["total_forms"]
                },
                "tables": {
                    "website1": self.website1_data["total_tables"],
                    "website2": self.website2_data["total_tables"],
                    "difference": self.website1_data["total_tables"] - self.website2_data["total_tables"]
                },
                "lists": {
                    "website1": self.website1_data["total_lists"],
                    "website2": self.website2_data["total_lists"],
                    "difference": self.website1_data["total_lists"] - self.website2_data["total_lists"]
                }
            }
        }
        
        # Technical differences
        comparison["technical_differences"] = {
            "technologies": {
                "website1": self.website1_data["technologies_detected"],
                "website2": self.website2_data["technologies_detected"],
                "unique_to_website1": list(set(self.website1_data["technologies_detected"]) - set(self.website2_data["technologies_detected"])),
                "unique_to_website2": list(set(self.website2_data["technologies_detected"]) - set(self.website1_data["technologies_detected"])),
                "common": list(set(self.website1_data["technologies_detected"]) & set(self.website2_data["technologies_detected"]))
            },
            "meta_tags": {
                "website1_count": len(self.website1_data["meta_tags"]),
                "website2_count": len(self.website2_data["meta_tags"]),
                "difference": len(self.website1_data["meta_tags"]) - len(self.website2_data["meta_tags"])
            },
            "social_links": {
                "website1": self.website1_data["social_links"],
                "website2": self.website2_data["social_links"],
                "unique_to_website1": [link for link in self.website1_data["social_links"] if link not in self.website2_data["social_links"]],
                "unique_to_website2": [link for link in self.website2_data["social_links"] if link not in self.website1_data["social_links"]],
                "common": [link for link in self.website1_data["social_links"] if link in self.website2_data["social_links"]]
            }
        }
        
        # Functionality differences
        comparison["functionality_differences"] = {
            "forms_analysis": self._compare_forms(),
            "links_analysis": self._compare_links(),
            "errors": {
                "website1_errors": len(self.website1_data["errors"]),
                "website2_errors": len(self.website2_data["errors"]),
                "website1_error_details": self.website1_data["errors"],
                "website2_error_details": self.website2_data["errors"]
            }
        }
        
        # Detailed analysis
        comparison["detailed_analysis"] = {
            "content_richness": self._analyze_content_richness(),
            "interactivity_level": self._analyze_interactivity(),
            "seo_indicators": self._analyze_seo_indicators(),
            "accessibility_features": self._analyze_accessibility(),
            "performance_indicators": self._analyze_performance()
        }
        
        return comparison

    def _calculate_percentage_difference(self, val1, val2):
        """Calculate percentage difference between two values"""
        if val1 == 0 and val2 == 0:
            return 0
        if val2 == 0:
            return 100
        return round(((val1 - val2) / val2) * 100, 2)

    def _calculate_keyword_similarity(self):
        """Calculate keyword similarity percentage"""
        keywords1 = set(self.website1_data["unique_keywords"])
        keywords2 = set(self.website2_data["unique_keywords"])
        
        if not keywords1 and not keywords2:
            return 100
        if not keywords1 or not keywords2:
            return 0
        
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        
        return round((intersection / union) * 100, 2)

    def _compare_forms(self):
        """Compare forms between websites"""
        forms1 = self.website1_data["all_forms"]
        forms2 = self.website2_data["all_forms"]
        
        return {
            "website1_forms": forms1,
            "website2_forms": forms2,
            "website1_form_types": list(set([form.get("method", "get") for form in forms1])),
            "website2_form_types": list(set([form.get("method", "get") for form in forms2])),
            "website1_input_types": list(set([input_field.get("type", "text") for form in forms1 for input_field in form.get("inputs", [])])),
            "website2_input_types": list(set([input_field.get("type", "text") for form in forms2 for input_field in form.get("inputs", [])]))
        }

    def _compare_links(self):
        """Compare links between websites"""
        links1 = self.website1_data["all_links"]
        links2 = self.website2_data["all_links"]
        
        # Categorize links
        internal1 = [link for link in links1 if self.website1_data["domain"] in link]
        external1 = [link for link in links1 if self.website1_data["domain"] not in link]
        internal2 = [link for link in links2 if self.website2_data["domain"] in link]
        external2 = [link for link in links2 if self.website2_data["domain"] not in link]
        
        return {
            "website1_total_links": len(links1),
            "website2_total_links": len(links2),
            "website1_internal_links": len(internal1),
            "website2_internal_links": len(internal2),
            "website1_external_links": len(external1),
            "website2_external_links": len(external2),
            "internal_link_difference": len(internal1) - len(internal2),
            "external_link_difference": len(external1) - len(external2)
        }

    def _analyze_content_richness(self):
        """Analyze content richness of both websites"""
        richness1 = self._calculate_content_richness(self.website1_data)
        richness2 = self._calculate_content_richness(self.website2_data)
        
        return {
            "website1_richness_score": richness1,
            "website2_richness_score": richness2,
            "richness_difference": richness1 - richness2,
            "winner": "Website 1" if richness1 > richness2 else "Website 2" if richness2 > richness1 else "Tie"
        }

    def _calculate_content_richness(self, website_data):
        """Calculate content richness score"""
        score = 0
        score += min(website_data["total_word_count"] / 1000, 10)  # Max 10 points for words
        score += min(website_data["total_images"] * 0.5, 5)  # Max 5 points for images
        score += min(website_data["total_forms"] * 2, 10)  # Max 10 points for forms
        score += min(website_data["total_tables"] * 3, 6)  # Max 6 points for tables
        score += min(website_data["total_lists"] * 1, 4)  # Max 4 points for lists
        score += min(len(website_data["unique_keywords"]) * 0.2, 5)  # Max 5 points for keywords
        return round(score, 2)

    def _analyze_interactivity(self):
        """Analyze interactivity level of both websites"""
        interactivity1 = self._calculate_interactivity(self.website1_data)
        interactivity2 = self._calculate_interactivity(self.website2_data)
        
        return {
            "website1_interactivity_score": interactivity1,
            "website2_interactivity_score": interactivity2,
            "interactivity_difference": interactivity1 - interactivity2,
            "winner": "Website 1" if interactivity1 > interactivity2 else "Website 2" if interactivity2 > interactivity1 else "Tie"
        }

    def _calculate_interactivity(self, website_data):
        """Calculate interactivity score"""
        score = 0
        score += min(website_data["total_forms"] * 5, 25)  # Max 25 points for forms
        score += min(len(website_data["all_links"]) * 0.1, 10)  # Max 10 points for links
        score += min(len(website_data["pages"]) * 2, 20)  # Max 20 points for pages
        return round(score, 2)

    def _analyze_seo_indicators(self):
        """Analyze SEO indicators for both websites"""
        seo1 = self._calculate_seo_score(self.website1_data)
        seo2 = self._calculate_seo_score(self.website2_data)
        
        return {
            "website1_seo_score": seo1,
            "website2_seo_score": seo2,
            "seo_difference": seo1 - seo2,
            "winner": "Website 1" if seo1 > seo2 else "Website 2" if seo2 > seo1 else "Tie"
        }

    def _calculate_seo_score(self, website_data):
        """Calculate SEO score"""
        score = 0
        score += min(len(website_data["meta_tags"]) * 2, 20)  # Max 20 points for meta tags
        score += min(len(website_data["unique_keywords"]) * 0.5, 15)  # Max 15 points for keywords
        score += min(website_data["total_word_count"] / 500, 10)  # Max 10 points for content
        score += min(len(website_data["all_links"]) * 0.2, 10)  # Max 10 points for internal linking
        return round(score, 2)

    def _analyze_accessibility(self):
        """Analyze accessibility features"""
        return {
            "website1_alt_texts": len([img for img in self.website1_data["all_images"] if img.get("alt")]),
            "website2_alt_texts": len([img for img in self.website2_data["all_images"] if img.get("alt")]),
            "website1_alt_text_percentage": round((len([img for img in self.website1_data["all_images"] if img.get("alt")]) / max(len(self.website1_data["all_images"]), 1)) * 100, 2),
            "website2_alt_text_percentage": round((len([img for img in self.website2_data["all_images"] if img.get("alt")]) / max(len(self.website2_data["all_images"]), 1)) * 100, 2)
        }

    def _analyze_performance(self):
        """Analyze performance indicators"""
        return {
            "website1_total_elements": self.website1_data["total_images"] + self.website1_data["total_forms"] + self.website1_data["total_tables"],
            "website2_total_elements": self.website2_data["total_images"] + self.website2_data["total_forms"] + self.website2_data["total_tables"],
            "website1_pages_per_element": round(len(self.website1_data["pages"]) / max(self.website1_data["total_images"] + self.website1_data["total_forms"] + self.website1_data["total_tables"], 1), 2),
            "website2_pages_per_element": round(len(self.website2_data["pages"]) / max(self.website2_data["total_images"] + self.website2_data["total_forms"] + self.website2_data["total_tables"], 1), 2)
        }
