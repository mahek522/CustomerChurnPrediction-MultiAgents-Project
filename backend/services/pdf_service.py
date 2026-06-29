import sys
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(report_text: str, output_path: str) -> str:
    """
    Generates a PDF report from the executive summary report text and saves it to output_path.
    """
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Define clean, professional color palette
        primary_color = colors.HexColor("#1b365d") # Sleek navy
        secondary_color = colors.HexColor("#4b6b94") # Slate blue
        text_color = colors.HexColor("#2d3748") # Dark grey
        
        # Modify existing styles to avoid conflicts
        body_style = ParagraphStyle(
            'CustomBodyText',
            parent=styles['BodyText'],
            textColor=text_color,
            fontSize=10,
            leading=14
        )
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            textColor=primary_color,
            fontSize=22,
            leading=26,
            alignment=1, # Center
            spaceAfter=20
        )
        
        h1_style = ParagraphStyle(
            'CustomH1',
            parent=styles['Heading1'],
            textColor=primary_color,
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            textColor=secondary_color,
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        
        story = []
        
        # Header
        story.append(Paragraph("BNP PARIBAS CHURN INTELLIGENCE REPORT", title_style))
        story.append(Spacer(1, 10))
        
        # Convert report text lines into paragraphs
        lines = report_text.split('\n')
        for line in lines:
            line_str = line.strip()
            if not line_str:
                story.append(Spacer(1, 6))
                continue
            
            # Check for header indicators in markdown
            if line_str.startswith("###"):
                story.append(Spacer(1, 4))
                story.append(Paragraph(line_str.replace("###", "").strip(), h2_style))
            elif line_str.startswith("##"):
                story.append(Spacer(1, 8))
                story.append(Paragraph(line_str.replace("##", "").strip(), h1_style))
            elif line_str.startswith("#"):
                story.append(Spacer(1, 10))
                story.append(Paragraph(line_str.replace("#", "").strip(), title_style))
            else:
                # Handle bullet points
                if line_str.startswith("-") or line_str.startswith("*"):
                    bullet_text = line_str[1:].strip()
                    story.append(Paragraph(f"&bull; {bullet_text}", body_style))
                else:
                    story.append(Paragraph(line_str, body_style))
                    
        doc.build(story)
        return output_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise e
