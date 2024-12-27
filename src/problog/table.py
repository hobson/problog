import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch

def generate_pdf(data, conversation_info):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceBefore=6,
        spaceAfter=6
    )

    # Table data setup and style
    formatted_data = []
    for row in data:
        formatted_row = [Paragraph(cell, style_normal if i > 0 else styles['Heading1']) for i, cell in enumerate(row)]
        formatted_data.append(formatted_row)

    col_widths = [pdf.pagesize[0] * 0.35, pdf.pagesize[0] * 0.35, pdf.pagesize[0] * 0.15, pdf.pagesize[0] * 0.15]
    table = Table(formatted_data, colWidths=col_widths)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EAECEE')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
    ])
    table.setStyle(style)

    # Create elements
    elements = [
        Paragraph(f"ID: {conversation_info['id']}", style_normal),
        Paragraph(f"Title: {conversation_info['title']}", style_normal),
        Paragraph(f"Username: {conversation_info['username']}", style_normal),
        Paragraph("<br/>", style_normal), 
        table
    ]

    pdf.build(elements)
    buffer.seek(0)
    return buffer