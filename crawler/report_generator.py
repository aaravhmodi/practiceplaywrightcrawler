from fpdf import FPDF
import os
from datetime import datetime

def generate_report(logs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Website Crawler Report', 0, 1, 'C')
    pdf.ln(5)

    # Date and summary
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.cell(0, 8, f'Total Actions: {len(logs)}', 0, 1)
    pdf.ln(5)

    for i, log in enumerate(logs, 1):
        # Action header
        pdf.set_font('Arial', 'B', 12)
        action_text = log["action"]
        if "depth" in log:
            action_text += f" (Depth: {log['depth']})"
        pdf.cell(0, 8, f'Action #{i}: {action_text}', 0, 1)
        
        # URL
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f'URL: {log["url"]}', 0, 1)
        
        # Timestamp
        if "timestamp" in log:
            from datetime import datetime
            timestamp = datetime.fromtimestamp(log["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            pdf.cell(0, 6, f'Time: {timestamp}', 0, 1)
        
        # Summary data
        if "data" in log and log["data"]:
            data = log["data"]
            
            # Title
            if data.get('title'):
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f'Title: {data["title"]}', 0, 1)
            
            # Meta description
            if data.get('meta_description'):
                pdf.set_font('Arial', '', 9)
                desc = data["meta_description"][:80] + "..." if len(data["meta_description"]) > 80 else data["meta_description"]
                pdf.cell(0, 5, f'Description: {desc}', 0, 1)
            
            # Page structure info
            if data.get('page_structure'):
                structure = data['page_structure']
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(0, 5, 'Page Structure:', 0, 1)
                pdf.set_font('Arial', '', 8)
                structure_info = []
                if structure.get('has_navigation'): structure_info.append('Navigation')
                if structure.get('has_header'): structure_info.append('Header')
                if structure.get('has_footer'): structure_info.append('Footer')
                if structure.get('has_main'): structure_info.append('Main')
                if structure_info:
                    pdf.cell(0, 4, f'• {", ".join(structure_info)}', 0, 1)
            
            # Headings
            if data.get('headings'):
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f'Key Headings ({len(data["headings"])} total):', 0, 1)
                pdf.set_font('Arial', '', 9)
                for heading in data['headings'][:3]:
                    heading_text = heading[:50] + "..." if len(heading) > 50 else heading
                    pdf.cell(0, 5, f'• {heading_text}', 0, 1)
            
            # Important keywords
            if data.get('important_words'):
                pdf.set_font('Arial', 'B', 10)
                keywords = ", ".join(data["important_words"][:8])
                pdf.cell(0, 6, f'Keywords: {keywords}', 0, 1)
            
            # Comprehensive statistics
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, 'Page Statistics:', 0, 1)
            pdf.set_font('Arial', '', 9)
            
            if data.get('total_elements'):
                elements = data['total_elements']
                pdf.cell(0, 5, f'• Links: {elements.get("links", 0)}', 0, 1)
                pdf.cell(0, 5, f'• Images: {elements.get("images", 0)}', 0, 1)
                pdf.cell(0, 5, f'• Forms: {elements.get("forms", 0)}', 0, 1)
                pdf.cell(0, 5, f'• Tables: {elements.get("tables", 0)}', 0, 1)
                pdf.cell(0, 5, f'• Lists: {elements.get("lists", 0)}', 0, 1)
            
            pdf.cell(0, 5, f'• Word count: {data.get("word_count", 0)}', 0, 1)
            pdf.cell(0, 5, f'• Sentences: {data.get("sentences_count", 0)}', 0, 1)
            
            # Forms details
            if data.get('forms'):
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f'Forms found: {len(data["forms"])}', 0, 1)
                pdf.set_font('Arial', '', 8)
                for form in data['forms'][:2]:  # Show first 2 forms
                    pdf.cell(0, 4, f'• {form.get("method", "GET")} form with {len(form.get("inputs", []))} inputs', 0, 1)
            
            # Social media links
            if data.get('social_links'):
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f'Social Links: {len(data["social_links"])}', 0, 1)
                pdf.set_font('Arial', '', 8)
                for social in data['social_links'][:3]:
                    pdf.cell(0, 4, f'• {social["platform"].title()}: {social["url"][:40]}...', 0, 1)
            
            # Text preview
            if data.get('text_content'):
                pdf.set_font('Arial', '', 8)
                preview = data["text_content"][:120] + "..." if len(data["text_content"]) > 120 else data["text_content"]
                pdf.cell(0, 5, f'Content: {preview}', 0, 1)

        # Error handling
        if "error" in log:
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(255, 0, 0)  # Red color for errors
            pdf.cell(0, 6, f'Error: {log["error"]}', 0, 1)
            pdf.set_text_color(0, 0, 0)  # Reset to black

        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Add separator line
        pdf.ln(3)

    # Footer
    pdf.set_font('Arial', '', 8)
    pdf.cell(0, 10, 'Generated by Web Crawler MVP with scikit-learn, lxml, and fpdf2', 0, 1, 'C')

    pdf.output(filename)
    print(f"Report generated: {filename}")
