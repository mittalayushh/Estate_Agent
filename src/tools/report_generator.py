"""
PDF Report Generator — Creates professional investment advisory PDFs.

Uses ReportLab to generate branded, structured advisory reports
with property details, comparable analysis, and risk assessment.
"""

import os
import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import inch, mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, PageBreak
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ── Brand Colors ──
PRIMARY = HexColor("#00ffcc") if REPORTLAB_AVAILABLE else None
DARK_BG = HexColor("#0a0a14") if REPORTLAB_AVAILABLE else None
CARD_BG = HexColor("#1a1a2e") if REPORTLAB_AVAILABLE else None
TEXT_MAIN = HexColor("#f0f0f5") if REPORTLAB_AVAILABLE else None
TEXT_MUTED = HexColor("#9aa0a6") if REPORTLAB_AVAILABLE else None
ACCENT = HexColor("#00d4aa") if REPORTLAB_AVAILABLE else None


def generate_pdf(report_text: str, property_data: dict = None,
                 comparables: list = None, risk_data: dict = None,
                 filename: str = "Estate_Agent_Advisory.pdf") -> str:
    """
    Generates a professional PDF advisory report.

    Args:
        report_text: The full advisory report text
        property_data: Property input details
        comparables: List of comparable property dicts
        risk_data: Risk assessment dict
        filename: Output filename

    Returns:
        Path to the generated PDF file
    """
    if not REPORTLAB_AVAILABLE:
        # Fallback: save as text file
        txt_path = filename.replace('.pdf', '.txt')
        with open(txt_path, 'w') as f:
            f.write(report_text)
        return txt_path

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    # ── Styles ──
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor("#666666"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor("#00856a"),
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor("#333333"),
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor("#999999"),
        leading=10,
        alignment=TA_JUSTIFY,
        spaceBefore=20
    )

    elements = []

    # ── Header ──
    elements.append(Paragraph("🏠 Estate Agent AI", title_style))
    elements.append(Paragraph("Investment Advisory Report", subtitle_style))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))

    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=HexColor("#00d4aa"),
        spaceAfter=20
    ))

    # ── Property Summary Table ──
    if property_data:
        elements.append(Paragraph("📋 Property Details", heading_style))

        table_data = [
            ["Parameter", "Value"],
            ["City", property_data.get('City', 'N/A')],
            ["State", property_data.get('State', 'N/A')],
            ["Type", property_data.get('Property_Type', 'N/A')],
            ["BHK", str(property_data.get('BHK', 'N/A'))],
            ["Size", f"{property_data.get('Size_in_SqFt', 'N/A')} sq ft"],
            ["Furnished", property_data.get('Furnished_Status', 'N/A')],
            ["Security", property_data.get('Security', 'N/A')],
            ["Transport", property_data.get('Public_Transport_Accessibility', 'N/A')],
        ]

        table = Table(table_data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#00856a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 16))

    # ── Comparable Properties Table ──
    if comparables and len(comparables) > 0:
        elements.append(Paragraph("🏘️ Comparable Properties", heading_style))

        comp_data = [["Variant", "BHK", "Size (sqft)", "Price (₹L)", "Diff %"]]
        for comp in comparables:
            comp_data.append([
                comp.get('label', ''),
                str(comp.get('bhk', '')),
                str(comp.get('size_sqft', '')),
                f"₹{comp.get('predicted_price_lakhs', '')}L",
                f"{comp.get('price_diff_pct', '')}%"
            ])

        comp_table = Table(comp_data, colWidths=[140, 50, 80, 90, 60])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#00856a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(comp_table)
        elements.append(Spacer(1, 16))

    # ── Risk Assessment ──
    if risk_data:
        elements.append(Paragraph("⚠️ Risk Assessment", heading_style))
        elements.append(Paragraph(
            f"Overall Risk: <b>{risk_data.get('overall_risk_level', 'N/A')}</b> "
            f"(Score: {risk_data.get('overall_risk_score', 'N/A')}/100)",
            body_style
        ))

        for factor in risk_data.get('risk_factors', []):
            elements.append(Paragraph(
                f"• <b>{factor['factor']}</b> [{factor['severity']}]: {factor['details']}",
                body_style
            ))

        elements.append(Spacer(1, 12))

    # ── Main Report ──
    elements.append(Paragraph("📊 Advisory Report", heading_style))

    # Parse and format report sections
    for line in report_text.split('\n'):
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 4))
        elif line.startswith('## '):
            elements.append(Paragraph(line.replace('## ', ''), heading_style))
        elif line.startswith('# '):
            elements.append(Paragraph(line.replace('# ', ''), heading_style))
        elif line.startswith('**') and line.endswith('**'):
            elements.append(Paragraph(f"<b>{line.strip('*')}</b>", body_style))
        else:
            # Escape XML special characters
            safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(safe_line, body_style))

    # ── Disclaimer ──
    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=HexColor("#cccccc"),
        spaceBefore=20, spaceAfter=10
    ))
    elements.append(Paragraph(
        "<b>DISCLAIMER</b>: This report is generated by an AI system for informational "
        "purposes only. It does not constitute financial, legal, or investment advice. "
        "Property valuations are model predictions and may differ from actual market prices. "
        "Always consult with qualified professionals (RERA-registered agents, financial advisors, "
        "legal counsel) before making investment decisions. Past performance does not guarantee "
        "future results. The creators of this system bear no liability for investment decisions "
        "made based on this report.",
        disclaimer_style
    ))

    # Build PDF
    doc.build(elements)

    # Return bytes
    buffer.seek(0)
    return buffer.getvalue()
