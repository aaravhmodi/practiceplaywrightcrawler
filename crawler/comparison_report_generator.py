from fpdf import FPDF
import os
from datetime import datetime

class ComparisonReportGenerator:
    def __init__(self):
        self.pdf = None
        self.width = 210  # A4 width in mm
        self.height = 297  # A4 height in mm
        self.margin = 20
        self.current_y = self.margin
        self.cell_height = 6
        self.table_width = 170  # Total table width
        self.col_width = 85  # Width of each column

    def generate_comparison_report(self, comparison_data, filename):
        """Generate comprehensive table-based comparison report"""
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title page with similarity score
        self._add_title_page_with_similarity(comparison_data)
        
        # Overall similarity score and statistics
        self._add_similarity_statistics(comparison_data)
        
        # Basic comparison table
        self._add_basic_comparison_table(comparison_data)
        
        # Pages comparison table
        self._add_pages_comparison_table(comparison_data)
        
        # Buttons comparison table
        self._add_buttons_comparison_table(comparison_data)
        
        # Content elements comparison table
        self._add_content_elements_table(comparison_data)
        
        # Technical features comparison table
        self._add_technical_features_table(comparison_data)
        
        # Forms comparison table
        self._add_forms_comparison_table(comparison_data)
        
        # Links comparison table
        self._add_links_comparison_table(comparison_data)
        
        # Similar items section
        self._add_similar_items_section(comparison_data)
        
        # Different items section
        self._add_different_items_section(comparison_data)
        
        # Summary and recommendations
        self._add_summary_section(comparison_data)
        
        # Footer
        self._add_footer()
        
        self.pdf.output(filename)
        print(f"Comparison report generated: {filename}")

    def _add_title_page_with_similarity(self, data):
        """Add title page with overall similarity score"""
        self.pdf.set_font('Arial', 'B', 20)
        self.pdf.cell(0, 15, 'Website Comparison Report', 0, 1, 'C')
        self.pdf.ln(10)
        
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 8, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.pdf.ln(15)
        
        # Calculate overall similarity score
        similarity_score = self._calculate_overall_similarity_score(data)
        
        # Similarity score box
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 8, f'Overall Similarity Score: {similarity_score}%', 0, 1, 'C')
        self.pdf.ln(10)
        
        # Website details in table format
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(self.col_width, 8, 'Website 1', 1, 0, 'C')
        self.pdf.cell(self.col_width, 8, 'Website 2', 1, 1, 'C')
        
        self.pdf.set_font('Arial', '', 10)
        details = [
            ('Domain', data["website1"]["domain"], data["website2"]["domain"]),
            ('Pages Crawled', str(len(data["website1"]["pages"])), str(len(data["website2"]["pages"]))),
            ('Total Words', f"{data['website1']['total_word_count']:,}", f"{data['website2']['total_word_count']:,}"),
            ('Total Links', str(len(data["website1"]["all_links"])), str(len(data["website2"]["all_links"]))),
            ('Total Images', str(data["website1"]["total_images"]), str(data["website2"]["total_images"])),
            ('Total Forms', str(data["website1"]["total_forms"]), str(data["website2"]["total_forms"]))
        ]
        
        for label, val1, val2 in details:
            self.pdf.cell(30, self.cell_height, label, 1, 0)
            self.pdf.cell(self.col_width-30, self.cell_height, val1, 1, 0, 'C')
            self.pdf.cell(self.col_width, self.cell_height, val2, 1, 1, 'C')
        
        self.pdf.ln(10)

    def _add_similarity_statistics(self, data):
        """Add similarity statistics section"""
        self._add_section_header("Similarity Statistics")
        
        # Calculate various similarity scores
        keyword_similarity = data["comparison"]["content_differences"]["keywords"]["similarity_percentage"]
        structure_similarity = self._calculate_structure_similarity(data)
        content_similarity = self._calculate_content_similarity(data)
        technical_similarity = self._calculate_technical_similarity(data)
        
        # Similarity scores table
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.cell(0, 8, 'Similarity Breakdown:', 0, 1)
        self.pdf.set_font('Arial', '', 10)
        
        similarities = [
            ('Keyword Similarity', f"{keyword_similarity}%"),
            ('Structure Similarity', f"{structure_similarity}%"),
            ('Content Similarity', f"{content_similarity}%"),
            ('Technical Similarity', f"{technical_similarity}%")
        ]
        
        for metric, score in similarities:
            self.pdf.cell(60, self.cell_height, metric, 1, 0)
            self.pdf.cell(30, self.cell_height, score, 1, 1, 'C')
        
        self.pdf.ln(5)

    def _add_basic_comparison_table(self, data):
        """Add basic comparison table"""
        self._add_section_header("Basic Comparison")
        
        # Create comparison table
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(50, self.cell_height, 'Metric', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 1', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 2', 1, 1, 'C')
        
        self.pdf.set_font('Arial', '', 9)
        
        metrics = [
            ('Pages', len(data["website1"]["pages"]), len(data["website2"]["pages"])),
            ('Total Words', f"{data['website1']['total_word_count']:,}", f"{data['website2']['total_word_count']:,}"),
            ('Unique Keywords', len(data["website1"]["unique_keywords"]), len(data["website2"]["unique_keywords"])),
            ('Page Titles', len(data["website1"]["page_titles"]), len(data["website2"]["page_titles"])),
            ('Navigation Elements', len(data["website1"]["navigation_structure"]), len(data["website2"]["navigation_structure"])),
            ('Technologies', len(data["website1"]["technologies_detected"]), len(data["website2"]["technologies_detected"])),
            ('Meta Tags', len(data["website1"]["meta_tags"]), len(data["website2"]["meta_tags"])),
            ('Social Links', len(data["website1"]["social_links"]), len(data["website2"]["social_links"])),
            ('Errors', len(data["website1"]["errors"]), len(data["website2"]["errors"]))
        ]
        
        for metric, val1, val2 in metrics:
            self.pdf.cell(50, self.cell_height, metric, 1, 0)
            self.pdf.cell(self.col_width, self.cell_height, str(val1), 1, 0, 'C')
            self.pdf.cell(self.col_width, self.cell_height, str(val2), 1, 1, 'C')
        
        self.pdf.ln(5)

    def _add_pages_comparison_table(self, data):
        """Add comprehensive pages comparison table with every detail"""
        self._add_section_header("Complete Pages Analysis")
        
        # Detailed page analysis for Website 1
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 ({data["website1"]["domain"]}) - All Pages:', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, page in enumerate(data["website1"]["pages"], 1):
            self.pdf.cell(0, 6, f'Page {i}: {page.get("url", "Unknown URL")}', 0, 1)
            self.pdf.cell(0, 6, f'  Title: {page.get("title", "No title")}', 0, 1)
            self.pdf.cell(0, 6, f'  Word Count: {page.get("word_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Links: {page.get("links_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Images: {page.get("images_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Forms: {page.get("forms_count", 0)}', 0, 1)
            
            # All headings on this page
            headings = page.get("headings", [])
            if headings:
                self.pdf.cell(0, 6, f'  Headings ({len(headings)}):', 0, 1)
                for heading in headings:
                    heading_short = heading[:80] + "..." if len(heading) > 80 else heading
                    self.pdf.cell(10, 5, '', 0, 0)  # Indent
                    self.pdf.cell(0, 5, f'• {heading_short}', 0, 1)
            
            # All keywords on this page
            keywords = page.get("keywords", [])
            if keywords:
                self.pdf.cell(0, 6, f'  Keywords ({len(keywords)}): {", ".join(keywords[:10])}', 0, 1)
                if len(keywords) > 10:
                    self.pdf.cell(0, 5, f'    ... and {len(keywords) - 10} more', 0, 1)
            
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # Detailed page analysis for Website 2
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 ({data["website2"]["domain"]}) - All Pages:', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, page in enumerate(data["website2"]["pages"], 1):
            self.pdf.cell(0, 6, f'Page {i}: {page.get("url", "Unknown URL")}', 0, 1)
            self.pdf.cell(0, 6, f'  Title: {page.get("title", "No title")}', 0, 1)
            self.pdf.cell(0, 6, f'  Word Count: {page.get("word_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Links: {page.get("links_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Images: {page.get("images_count", 0)}', 0, 1)
            self.pdf.cell(0, 6, f'  Forms: {page.get("forms_count", 0)}', 0, 1)
            
            # All headings on this page
            headings = page.get("headings", [])
            if headings:
                self.pdf.cell(0, 6, f'  Headings ({len(headings)}):', 0, 1)
                for heading in headings:
                    heading_short = heading[:80] + "..." if len(heading) > 80 else heading
                    self.pdf.cell(10, 5, '', 0, 0)  # Indent
                    self.pdf.cell(0, 5, f'• {heading_short}', 0, 1)
            
            # All keywords on this page
            keywords = page.get("keywords", [])
            if keywords:
                self.pdf.cell(0, 6, f'  Keywords ({len(keywords)}): {", ".join(keywords[:10])}', 0, 1)
                if len(keywords) > 10:
                    self.pdf.cell(0, 5, f'    ... and {len(keywords) - 10} more', 0, 1)
            
            self.pdf.ln(2)
        
        self.pdf.ln(5)

    def _add_buttons_comparison_table(self, data):
        """Add comprehensive buttons comparison with every button detail"""
        self._add_section_header("Complete Buttons and Interactive Elements Analysis")
        
        # Extract detailed button information from logs
        website1_buttons = self._extract_detailed_buttons_from_logs(data["website1_logs"])
        website2_buttons = self._extract_detailed_buttons_from_logs(data["website2_logs"])
        
        # Website 1 - All Buttons
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 ({data["website1"]["domain"]}) - All Buttons ({len(website1_buttons)}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, button in enumerate(website1_buttons, 1):
            self.pdf.cell(0, 6, f'Button {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Text: "{button.get("text", "No text")}"', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Tag: {button.get("tag", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Type: {button.get("type", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Href: {button.get("href", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'ID: {button.get("id", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Class: {button.get("className", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'OnClick: {button.get("onclick", "None")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # Website 2 - All Buttons
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 ({data["website2"]["domain"]}) - All Buttons ({len(website2_buttons)}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, button in enumerate(website2_buttons, 1):
            self.pdf.cell(0, 6, f'Button {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Text: "{button.get("text", "No text")}"', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Tag: {button.get("tag", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Type: {button.get("type", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Href: {button.get("href", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'ID: {button.get("id", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Class: {button.get("className", "None")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'OnClick: {button.get("onclick", "None")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # Button Comparison Analysis
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, 'Button Comparison Analysis:', 0, 1)
        self.pdf.set_font('Arial', '', 9)
        
        # Extract button texts for comparison
        buttons1_texts = [button.get("text", "") for button in website1_buttons]
        buttons2_texts = [button.get("text", "") for button in website2_buttons]
        
        common_buttons = set(buttons1_texts) & set(buttons2_texts)
        website1_unique = set(buttons1_texts) - set(buttons2_texts)
        website2_unique = set(buttons2_texts) - set(buttons1_texts)
        
        self.pdf.cell(0, 6, f'Common buttons: {len(common_buttons)}', 0, 1)
        self.pdf.cell(0, 6, f'Website 1 unique buttons: {len(website1_unique)}', 0, 1)
        self.pdf.cell(0, 6, f'Website 2 unique buttons: {len(website2_unique)}', 0, 1)
        
        # Show all common buttons
        if common_buttons:
            self.pdf.set_font('Arial', 'B', 10)
            self.pdf.cell(0, 8, 'All Common Buttons:', 0, 1)
            self.pdf.set_font('Arial', '', 8)
            for button_text in sorted(common_buttons):
                self.pdf.cell(0, 5, f'• "{button_text}"', 0, 1)
        
        self.pdf.ln(5)

    def _add_content_elements_table(self, data):
        """Add comprehensive content elements analysis with every detail"""
        self._add_section_header("Complete Content Elements Analysis")
        
        # Website 1 - All Images
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 ({data["website1"]["domain"]}) - All Images ({data["website1"]["total_images"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, image in enumerate(data["website1"]["all_images"], 1):
            self.pdf.cell(0, 6, f'Image {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Src: {image.get("src", "No src")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Alt: "{image.get("alt", "No alt text")}"', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Width: {image.get("width", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Height: {image.get("height", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Title: {image.get("title", "No title")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # Website 2 - All Images
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 ({data["website2"]["domain"]}) - All Images ({data["website2"]["total_images"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, image in enumerate(data["website2"]["all_images"], 1):
            self.pdf.cell(0, 6, f'Image {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Src: {image.get("src", "No src")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Alt: "{image.get("alt", "No alt text")}"', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Width: {image.get("width", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Height: {image.get("height", "Unknown")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Title: {image.get("title", "No title")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # All Links Analysis
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 - All Links ({len(data["website1"]["all_links"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, link in enumerate(data["website1"]["all_links"], 1):
            link_short = link[:100] + "..." if len(link) > 100 else link
            self.pdf.cell(0, 5, f'{i}. {link_short}', 0, 1)
        
        self.pdf.ln(5)
        
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 - All Links ({len(data["website2"]["all_links"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, link in enumerate(data["website2"]["all_links"], 1):
            link_short = link[:100] + "..." if len(link) > 100 else link
            self.pdf.cell(0, 5, f'{i}. {link_short}', 0, 1)
        
        self.pdf.ln(5)
        
        # All Keywords Analysis
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 - All Keywords ({len(data["website1"]["unique_keywords"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        keywords_text1 = ", ".join(data["website1"]["unique_keywords"])
        # Split long keyword lists into multiple lines
        if len(keywords_text1) > 100:
            words = keywords_text1.split(", ")
            current_line = ""
            for word in words:
                if len(current_line + word + ", ") > 100:
                    self.pdf.cell(0, 5, current_line.rstrip(", "), 0, 1)
                    current_line = word + ", "
                else:
                    current_line += word + ", "
            if current_line:
                self.pdf.cell(0, 5, current_line.rstrip(", "), 0, 1)
        else:
            self.pdf.cell(0, 5, keywords_text1, 0, 1)
        
        self.pdf.ln(5)
        
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 - All Keywords ({len(data["website2"]["unique_keywords"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        keywords_text2 = ", ".join(data["website2"]["unique_keywords"])
        # Split long keyword lists into multiple lines
        if len(keywords_text2) > 100:
            words = keywords_text2.split(", ")
            current_line = ""
            for word in words:
                if len(current_line + word + ", ") > 100:
                    self.pdf.cell(0, 5, current_line.rstrip(", "), 0, 1)
                    current_line = word + ", "
                else:
                    current_line += word + ", "
            if current_line:
                self.pdf.cell(0, 5, current_line.rstrip(", "), 0, 1)
        else:
            self.pdf.cell(0, 5, keywords_text2, 0, 1)
        
        self.pdf.ln(5)

    def _add_technical_features_table(self, data):
        """Add technical features comparison table"""
        self._add_section_header("Technical Features Comparison")
        
        # Technologies comparison
        tech1 = set(data["website1"]["technologies_detected"])
        tech2 = set(data["website2"]["technologies_detected"])
        common_tech = tech1 & tech2
        unique_tech1 = tech1 - tech2
        unique_tech2 = tech2 - tech1
        
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(50, self.cell_height, 'Technology', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 1', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 2', 1, 1, 'C')
        
        self.pdf.set_font('Arial', '', 9)
        
        all_tech = tech1 | tech2
        for tech in all_tech:
            in_website1 = "Yes" if tech in tech1 else "No"
            in_website2 = "Yes" if tech in tech2 else "No"
            self.pdf.cell(50, self.cell_height, tech, 1, 0)
            self.pdf.cell(self.col_width, self.cell_height, in_website1, 1, 0, 'C')
            self.pdf.cell(self.col_width, self.cell_height, in_website2, 1, 1, 'C')
        
        self.pdf.ln(5)

    def _add_forms_comparison_table(self, data):
        """Add comprehensive forms comparison with every form detail"""
        self._add_section_header("Complete Forms Analysis")
        
        # Website 1 - All Forms
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 ({data["website1"]["domain"]}) - All Forms ({data["website1"]["total_forms"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, form in enumerate(data["website1"]["all_forms"], 1):
            self.pdf.cell(0, 6, f'Form {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Action: {form.get("action", "No action")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Method: {form.get("method", "get")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Inputs ({len(form.get("inputs", []))}):', 0, 1)
            
            for j, input_field in enumerate(form.get("inputs", []), 1):
                self.pdf.cell(20, 5, '', 0, 0)  # Double indent
                self.pdf.cell(0, 5, f'Input {j}: Type={input_field.get("type", "text")}, Name={input_field.get("name", "No name")}, Placeholder="{input_field.get("placeholder", "No placeholder")}", Required={input_field.get("required", False)}', 0, 1)
            
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # Website 2 - All Forms
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 ({data["website2"]["domain"]}) - All Forms ({data["website2"]["total_forms"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, form in enumerate(data["website2"]["all_forms"], 1):
            self.pdf.cell(0, 6, f'Form {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Action: {form.get("action", "No action")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Method: {form.get("method", "get")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Inputs ({len(form.get("inputs", []))}):', 0, 1)
            
            for j, input_field in enumerate(form.get("inputs", []), 1):
                self.pdf.cell(20, 5, '', 0, 0)  # Double indent
                self.pdf.cell(0, 5, f'Input {j}: Type={input_field.get("type", "text")}, Name={input_field.get("name", "No name")}, Placeholder="{input_field.get("placeholder", "No placeholder")}", Required={input_field.get("required", False)}', 0, 1)
            
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        # All Meta Tags Analysis
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 1 - All Meta Tags ({len(data["website1"]["meta_tags"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, meta in enumerate(data["website1"]["meta_tags"], 1):
            self.pdf.cell(0, 6, f'Meta {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Name: {meta.get("name", "No name")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Content: {meta.get("content", "No content")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Property: {meta.get("property", "No property")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Charset: {meta.get("charset", "No charset")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
        
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, f'Website 2 - All Meta Tags ({len(data["website2"]["meta_tags"])}):', 0, 1)
        self.pdf.set_font('Arial', '', 8)
        
        for i, meta in enumerate(data["website2"]["meta_tags"], 1):
            self.pdf.cell(0, 6, f'Meta {i}:', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)  # Indent
            self.pdf.cell(0, 5, f'Name: {meta.get("name", "No name")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Content: {meta.get("content", "No content")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Property: {meta.get("property", "No property")}', 0, 1)
            self.pdf.cell(10, 5, '', 0, 0)
            self.pdf.cell(0, 5, f'Charset: {meta.get("charset", "No charset")}', 0, 1)
            self.pdf.ln(2)
        
        self.pdf.ln(5)

    def _add_links_comparison_table(self, data):
        """Add links comparison table"""
        self._add_section_header("Links Comparison")
        
        links1 = data["website1"]["all_links"]
        links2 = data["website2"]["all_links"]
        
        # Categorize links
        domain1 = data["website1"]["domain"]
        domain2 = data["website2"]["domain"]
        
        internal1 = [link for link in links1 if domain1 in link]
        external1 = [link for link in links1 if domain1 not in link]
        internal2 = [link for link in links2 if domain2 in link]
        external2 = [link for link in links2 if domain2 not in link]
        
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(50, self.cell_height, 'Link Type', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 1', 1, 0, 'C')
        self.pdf.cell(self.col_width, self.cell_height, 'Website 2', 1, 1, 'C')
        
        self.pdf.set_font('Arial', '', 9)
        
        link_types = [
            ('Total Links', len(links1), len(links2)),
            ('Internal Links', len(internal1), len(internal2)),
            ('External Links', len(external1), len(external2))
        ]
        
        for link_type, val1, val2 in link_types:
            self.pdf.cell(50, self.cell_height, link_type, 1, 0)
            self.pdf.cell(self.col_width, self.cell_height, str(val1), 1, 0, 'C')
            self.pdf.cell(self.col_width, self.cell_height, str(val2), 1, 1, 'C')
        
        self.pdf.ln(5)

    def _add_similar_items_section(self, data):
        """Add similar items section"""
        self._add_section_header("Similar Items (Common Features)")
        
        comparison = data["comparison"]
        
        # Common technologies
        common_tech = comparison["technical_differences"]["technologies"]["common"]
        if common_tech:
            self.pdf.set_font('Arial', 'B', 10)
            self.pdf.cell(0, 8, 'Common Technologies:', 0, 1)
            self.pdf.set_font('Arial', '', 9)
            for tech in common_tech:
                self.pdf.cell(0, self.cell_height, f'• {tech}', 0, 1)
            self.pdf.ln(3)
        
        # Common page titles
        common_titles = comparison["structure_differences"]["page_titles"]["common"]
        if common_titles:
            self.pdf.set_font('Arial', 'B', 10)
            self.pdf.cell(0, 8, f'Common Page Titles ({len(common_titles)}):', 0, 1)
            self.pdf.set_font('Arial', '', 9)
            for title in common_titles[:10]:
                title_short = title[:60] + "..." if len(title) > 60 else title
                self.pdf.cell(0, self.cell_height, f'• {title_short}', 0, 1)
            self.pdf.ln(3)
        
        # Common keywords
        common_keywords = comparison["content_differences"]["keywords"]["common"]
        if common_keywords:
            self.pdf.set_font('Arial', 'B', 10)
            self.pdf.cell(0, 8, f'Common Keywords ({len(common_keywords)}):', 0, 1)
            self.pdf.set_font('Arial', '', 9)
            keywords_text = ", ".join(common_keywords[:15])
            self.pdf.cell(0, self.cell_height, keywords_text, 0, 1)
            self.pdf.ln(3)
        
        # Common navigation structure
        common_nav = comparison["structure_differences"]["navigation_structure"]["common"]
        if common_nav:
            self.pdf.set_font('Arial', 'B', 10)
            self.pdf.cell(0, 8, 'Common Navigation Elements:', 0, 1)
            self.pdf.set_font('Arial', '', 9)
            nav_text = ", ".join(common_nav)
            self.pdf.cell(0, self.cell_height, nav_text, 0, 1)
            self.pdf.ln(3)

    def _add_different_items_section(self, data):
        """Add different items section"""
        self._add_section_header("Different Items (Unique Features)")
        
        comparison = data["comparison"]
        
        # Website 1 unique features
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(0, 8, f'Unique to Website 1 ({data["website1"]["domain"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 9)
        
        # Unique technologies
        unique_tech1 = comparison["technical_differences"]["technologies"]["unique_to_website1"]
        if unique_tech1:
            self.pdf.cell(0, self.cell_height, f'Technologies: {", ".join(unique_tech1)}', 0, 1)
        
        # Unique page titles
        unique_titles1 = comparison["structure_differences"]["page_titles"]["unique_to_website1"]
        if unique_titles1:
            self.pdf.cell(0, self.cell_height, f'Page titles: {len(unique_titles1)} unique', 0, 1)
        
        # Unique keywords
        unique_keywords1 = comparison["content_differences"]["keywords"]["unique_to_website1"]
        if unique_keywords1:
            keywords_text = ", ".join(unique_keywords1[:10])
            self.pdf.cell(0, self.cell_height, f'Keywords: {keywords_text}', 0, 1)
        
        self.pdf.ln(5)
        
        # Website 2 unique features
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(0, 8, f'Unique to Website 2 ({data["website2"]["domain"]}):', 0, 1)
        self.pdf.set_font('Arial', '', 9)
        
        # Unique technologies
        unique_tech2 = comparison["technical_differences"]["technologies"]["unique_to_website2"]
        if unique_tech2:
            self.pdf.cell(0, self.cell_height, f'Technologies: {", ".join(unique_tech2)}', 0, 1)
        
        # Unique page titles
        unique_titles2 = comparison["structure_differences"]["page_titles"]["unique_to_website2"]
        if unique_titles2:
            self.pdf.cell(0, self.cell_height, f'Page titles: {len(unique_titles2)} unique', 0, 1)
        
        # Unique keywords
        unique_keywords2 = comparison["content_differences"]["keywords"]["unique_to_website2"]
        if unique_keywords2:
            keywords_text = ", ".join(unique_keywords2[:10])
            self.pdf.cell(0, self.cell_height, f'Keywords: {keywords_text}', 0, 1)
        
        self.pdf.ln(5)

    def _add_summary_section(self, data):
        """Add summary section"""
        self._add_section_header("Summary and Recommendations")
        
        comparison = data["comparison"]
        overall_similarity = self._calculate_overall_similarity_score(data)
        
        # Overall assessment
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.cell(0, 8, f'Overall Assessment: {overall_similarity}% Similarity', 0, 1)
        
        # Similarity interpretation
        if overall_similarity >= 80:
            similarity_level = "Very High"
        elif overall_similarity >= 60:
            similarity_level = "High"
        elif overall_similarity >= 40:
            similarity_level = "Medium"
        elif overall_similarity >= 20:
            similarity_level = "Low"
        else:
            similarity_level = "Very Low"
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.cell(0, 6, f'Similarity Level: {similarity_level}', 0, 1)
        
        # Key findings
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(0, 8, 'Key Findings:', 0, 1)
        self.pdf.set_font('Arial', '', 9)
        
        findings = []
        
        # Content differences
        word_diff = comparison["content_differences"]["word_count"]["difference"]
        if abs(word_diff) > 1000:
            findings.append(f"Significant content volume difference: {abs(word_diff):,} words")
        
        # Page differences
        page_diff = comparison["structure_differences"]["pages_count"]["difference"]
        if abs(page_diff) > 5:
            findings.append(f"Notable page count difference: {abs(page_diff)} pages")
        
        # Technology differences
        tech_diff1 = len(comparison["technical_differences"]["technologies"]["unique_to_website1"])
        tech_diff2 = len(comparison["technical_differences"]["technologies"]["unique_to_website2"])
        if tech_diff1 > 0 or tech_diff2 > 0:
            findings.append(f"Different technology stacks: {tech_diff1} vs {tech_diff2} unique technologies")
        
        # Add findings
        for i, finding in enumerate(findings[:5], 1):
            self.pdf.cell(0, self.cell_height, f'{i}. {finding}', 0, 1)
        
        self.pdf.ln(3)
        
        # Recommendations
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.cell(0, 8, 'Recommendations:', 0, 1)
        self.pdf.set_font('Arial', '', 9)
        
        recommendations = []
        
        if overall_similarity < 50:
            recommendations.append("Consider standardizing features and content structure")
        
        if abs(word_diff) > 5000:
            recommendations.append("Balance content volume for better user experience")
        
        if tech_diff1 > 2 or tech_diff2 > 2:
            recommendations.append("Evaluate technology stack differences for consistency")
        
        for i, rec in enumerate(recommendations[:3], 1):
            self.pdf.cell(0, self.cell_height, f'{i}. {rec}', 0, 1)

    def _add_section_header(self, title):
        """Add section header"""
        self.pdf.ln(5)
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 8, title, 0, 1)
        self.pdf.line(20, self.pdf.get_y(), 190, self.pdf.get_y())
        self.pdf.ln(3)

    def _add_footer(self):
        """Add footer"""
        self.pdf.ln(10)
        self.pdf.set_font('Arial', '', 8)
        self.pdf.cell(0, 10, 'Generated by Website Comparison Crawler with Playwright, BeautifulSoup, scikit-learn, lxml, and fpdf2', 0, 1, 'C')

    def _calculate_overall_similarity_score(self, data):
        """Calculate overall similarity score"""
        comparison = data["comparison"]
        
        # Weight different aspects
        keyword_similarity = comparison["content_differences"]["keywords"]["similarity_percentage"]
        structure_similarity = self._calculate_structure_similarity(data)
        content_similarity = self._calculate_content_similarity(data)
        technical_similarity = self._calculate_technical_similarity(data)
        
        # Weighted average
        overall_score = (
            keyword_similarity * 0.3 +
            structure_similarity * 0.25 +
            content_similarity * 0.25 +
            technical_similarity * 0.2
        )
        
        return round(overall_score, 1)

    def _calculate_structure_similarity(self, data):
        """Calculate structure similarity percentage"""
        comparison = data["comparison"]
        
        # Page titles similarity
        titles1 = set(comparison["structure_differences"]["page_titles"]["website1"])
        titles2 = set(comparison["structure_differences"]["page_titles"]["website2"])
        titles_similarity = len(titles1 & titles2) / max(len(titles1 | titles2), 1) * 100
        
        # Navigation similarity
        nav1 = set(comparison["structure_differences"]["navigation_structure"]["website1"])
        nav2 = set(comparison["structure_differences"]["navigation_structure"]["website2"])
        nav_similarity = len(nav1 & nav2) / max(len(nav1 | nav2), 1) * 100
        
        # Page count similarity
        pages1 = comparison["structure_differences"]["pages_count"]["website1"]
        pages2 = comparison["structure_differences"]["pages_count"]["website2"]
        pages_similarity = 100 - abs(pages1 - pages2) / max(pages1, pages2) * 100
        
        return round((titles_similarity + nav_similarity + pages_similarity) / 3, 1)

    def _calculate_content_similarity(self, data):
        """Calculate content similarity percentage"""
        comparison = data["comparison"]
        
        # Keyword similarity
        keyword_similarity = comparison["content_differences"]["keywords"]["similarity_percentage"]
        
        # Content elements similarity
        elements = comparison["content_differences"]["content_elements"]
        images_sim = 100 - abs(elements["images"]["website1"] - elements["images"]["website2"]) / max(elements["images"]["website1"], elements["images"]["website2"], 1) * 100
        forms_sim = 100 - abs(elements["forms"]["website1"] - elements["forms"]["website2"]) / max(elements["forms"]["website1"], elements["forms"]["website2"], 1) * 100
        
        return round((keyword_similarity + images_sim + forms_sim) / 3, 1)

    def _calculate_technical_similarity(self, data):
        """Calculate technical similarity percentage"""
        comparison = data["comparison"]
        
        # Technologies similarity
        tech1 = set(comparison["technical_differences"]["technologies"]["website1"])
        tech2 = set(comparison["technical_differences"]["technologies"]["website2"])
        tech_similarity = len(tech1 & tech2) / max(len(tech1 | tech2), 1) * 100
        
        # Meta tags similarity
        meta1 = comparison["technical_differences"]["meta_tags"]["website1_count"]
        meta2 = comparison["technical_differences"]["meta_tags"]["website2_count"]
        meta_similarity = 100 - abs(meta1 - meta2) / max(meta1, meta2, 1) * 100
        
        return round((tech_similarity + meta_similarity) / 2, 1)

    def _extract_buttons_from_logs(self, logs):
        """Extract button information from crawl logs"""
        buttons = []
        for log in logs:
            if "clicked_element" in log:
                button_text = log["clicked_element"].get("text", "")
                if button_text:
                    buttons.append(button_text)
        return buttons

    def _extract_detailed_buttons_from_logs(self, logs):
        """Extract detailed button information from crawl logs"""
        buttons = []
        for log in logs:
            if "clicked_element" in log:
                button_data = log["clicked_element"]
                buttons.append(button_data)
        return buttons