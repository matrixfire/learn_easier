import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from reportlab.lib.pagesizes import A4, A5, B5
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm, inch, cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
        KeepTogether, Flowable, Preformatted, Frame, PageTemplate, BaseDocTemplate
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import (
        HexColor, black, white, grey, lightgrey, darkgrey,
        CMYKColor, PCMYKColor
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.pdfgen import canvas
except ImportError:
    print("Error: reportlab not installed. Run: uv pip install reportlab")
    sys.exit(1)


# Page size definitions
PAGE_SIZES = {
    "A4": A4,
    "A5": A5,
    "B5": B5,
}

# Color scheme for modern look
COLORS = {
    "primary": HexColor("#2563eb"),      # Blue
    "secondary": HexColor("#7c3aed"),    # Purple
    "accent": HexColor("#f59e0b"),       # Amber
    "code_bg": HexColor("#1e293b"),     # Dark slate
    "code_text": HexColor("#a5b4fc"),   # Light blue
    "code_inline_bg": HexColor("#e2e8f0"),
    "code_inline_text": HexColor("#dc2626"),
    "quote_border": HexColor("#94a3b8"),
    "quote_bg": HexColor("#f1f5f9"),
    "quote_text": HexColor("#64748b"),
    "table_header": HexColor("#3b82f6"),
    "table_header_text": white,
    "table_even": HexColor("#f8fafc"),
    "table_odd": white,
    "line": HexColor("#e2e8f0"),
}


def register_chinese_fonts():
    """Register Chinese fonts if available"""
    font_dirs = [
        "C:/Windows/Fonts",
        "/System/Library/Fonts",
        "/usr/share/fonts",
        "/usr/share/fonts/truetype",
    ]

    chinese_fonts = [
        ("SimSun", "simsun.ttc"),
        ("SimHei", "simhei.ttf"),
        ("Microsoft YaHei", "msyh.ttc"),
        ("Microsoft YaHei UI", "msyhui.ttc"),
        ("PingFang SC", "PingFang.ttc"),
        ("Noto Sans CJK", "NotoSansCJK-Regular.ttc"),
        ("WenQuanYi", "WenQuanYiZenHei-Regular.ttf"),
    ]

    for font_name, font_file in chinese_fonts:
        for font_dir in font_dirs:
            font_path = Path(font_dir) / font_file
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    print(f"Registered font: {font_name}")
                    return font_name
                except Exception as e:
                    continue

    print("Warning: No Chinese font found, using default fonts")
    return None


def register_mono_fonts():
    """Register monospace fonts for code"""
    font_dirs = [
        "C:/Windows/Fonts",
    ]

    mono_fonts = [
        ("Consolas", "consola.ttf"),
        ("Courier New", "cour.ttf"),
        ("JetBrains Mono", "JetBrainsMono-Regular.ttf"),
    ]

    for font_name, font_file in mono_fonts:
        for font_dir in font_dirs:
            font_path = Path(font_dir) / font_file
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    return font_name
                except Exception:
                    continue

    return "Courier"


class HeaderFooter:
    """Draw header and footer on each page"""

    def __init__(self, page_size, title=""):
        self.page_size = page_size
        self.title = title
        self.width, self.height = page_size

    def draw_page_header_footer(self, canvas_obj, doc):
        """Draw header and footer on each page"""
        width, height = self.page_size

        # Header
        canvas_obj.setFillColor(COLORS["primary"])
        canvas_obj.rect(0, height - 25*mm, width, 25*mm, fill=1, stroke=0)

        canvas_obj.setFillColor(white)
        canvas_obj.setFont("Helvetica-Bold", 10)
        canvas_obj.drawString(20*mm, height - 17*mm, self.title)

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawRightString(width - 20*mm, height - 17*mm, datetime.now().strftime("%Y-%m-%d"))

        # Footer
        canvas_obj.setFillColor(COLORS["line"])
        canvas_obj.line(20*mm, 20*mm, width - 20*mm, 20*mm)

        canvas_obj.setFillColor(COLORS["quote_text"])
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawCentredString(width / 2, 12*mm, f"Page {doc.page}")


class CodeBlock(Flowable):
    """Custom flowable for code blocks with background"""

    def __init__(self, code, language="", font_name="Courier"):
        super().__init__()
        self.code = code
        self.language = language
        self.font_name = font_name

    def wrap(self, availWidth, availHeight):
        """Calculate size"""
        self.width = min(availWidth, 170*mm)
        self.height = max(len(self.code.split('\n')) * 3.5*mm + 10*mm, 30*mm)
        return self.width, self.height

    def draw(self):
        """Draw the code block"""
        self.canv.setFillColor(COLORS["code_bg"])
        self.canv.roundRect(5*mm, 0, self.width - 5*mm, self.height, 3*mm, fill=1, stroke=0)

        self.canv.setFillColor(COLORS["code_text"])
        self.canv.setFont(self.font_name, 8)
        self.canv.drawString(8*mm, self.height - 5*mm, f"{self.language}:" if self.language else "code:")

        self.canv.setFont(self.font_name, 9)
        y = self.height - 12*mm
        for line in self.code.split('\n'):
            self.canv.drawString(8*mm, y, line.rstrip())
            y -= 3.5*mm


def parse_inline_formatting(text):
    """Parse inline formatting: bold, italic, code, links"""
    # Code inline
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" color="#dc2626" backColor="#e2e8f0">\1</font>', text)

    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)

    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<!-- not handled -->\1<-->', text)

    return text


def markdown_to_pdf(md_path: str, output_path: str = None, page_size: str = "A5", title: str = None) -> str:
    """
    Convert markdown file to PDF with enhanced styling

    Args:
        md_path: Path to markdown file
        output_path: Output PDF path (optional)
        page_size: Page size (A4, A5, B5)
        title: Document title (optional)

    Returns:
        Path to generated PDF
    """
    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    if output_path is None:
        output_path = md_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    # Read markdown content
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title from content if not provided
    if title is None:
        first_line = content.strip().split('\n')[0]
        title = first_line.lstrip('#').strip()

    # Register fonts
    chinese_font = register_chinese_fonts()
    mono_font = register_mono_fonts()

    # Default font names
    title_font = chinese_font or "Helvetica-Bold"
    heading_font = chinese_font or "Helvetica"
    body_font = chinese_font or "Helvetica"
    code_font = mono_font or "Courier"

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=PAGE_SIZES.get(page_size, A5),
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=35*mm,
        bottomMargin=30*mm,
    )

    # Setup styles
    styles = getSampleStyleSheet()

    # Title style (for H1)
    title_style = ParagraphStyle(
        "BookTitle",
        parent=styles["Heading1"],
        fontName=title_font,
        fontSize=22,
        leading=30,
        spaceAfter=15*mm,
        spaceBefore=12*mm,
        alignment=TA_CENTER,
        textColor=black,
    )

    # H2 style
    h2_style = ParagraphStyle(
        "BookH2",
        parent=styles["Heading2"],
        fontName=heading_font,
        fontSize=15,
        leading=22,
        spaceAfter=8*mm,
        spaceBefore=10*mm,
        alignment=TA_LEFT,
        textColor=COLORS["primary"],
        borderWidth=1,
        borderColor=COLORS["primary"],
        borderPadding=(3, 0, 3, 0),
    )

    # H3 style
    h3_style = ParagraphStyle(
        "BookH3",
        parent=styles["Heading3"],
        fontName=heading_font,
        fontSize=13,
        leading=20,
        spaceAfter=6*mm,
        spaceBefore=8*mm,
        alignment=TA_LEFT,
        textColor=COLORS["secondary"],
    )

    # Body paragraph style
    body_style = ParagraphStyle(
        "BookBody",
        parent=styles["Normal"],
        fontName=body_font,
        fontSize=11,
        leading=16,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=darkgrey,
    )

    # Quote style
    quote_style = ParagraphStyle(
        "BookQuote",
        parent=styles["Normal"],
        fontName=body_font,
        fontSize=10,
        leading=15,
        spaceAfter=12,
        alignment=TA_LEFT,
        textColor=COLORS["quote_text"],
        leftIndent=10*mm,
        firstLineIndent=10*mm,
    )

    # List item style
    list_style = ParagraphStyle(
        "BookList",
        parent=styles["Normal"],
        fontName=body_font,
        fontSize=11,
        leading=16,
        spaceAfter=6,
        alignment=TA_LEFT,
        textColor=darkgrey,
        bulletIndent=5*mm,
        leftIndent=15*mm,
    )

    # Code inline style
    code_inline_style = ParagraphStyle(
        "CodeInline",
        parent=styles["Normal"],
        fontName=code_font,
        fontSize=10,
        leading=14,
        textColor=COLORS["code_inline_text"],
        backColor=COLORS["code_inline_bg"],
    )

    # Parse markdown and build PDF elements
    story = []
    lines = content.split("\n")

    # Add cover page
    story.append(Spacer(0, 30*mm))
    story.append(Paragraph(title, ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName=title_font,
        fontSize=32,
        leading=40,
        alignment=TA_CENTER,
        textColor=COLORS["primary"],
    )))
    story.append(Spacer(0, 40*mm))
    story.append(Paragraph(
        f"<font name='Helvetica' color='{COLORS['quote_text']}'>{datetime.now().strftime('%Y年%m月%d日')}</font>",
        ParagraphStyle(
            "CoverDate",
            parent=styles["Normal"],
            alignment=TA_CENTER,
        )
    ))
    story.append(PageBreak())

    # Parse content
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty lines
        if not stripped:
            i += 1
            continue

        # Code blocks
        if stripped.startswith("```"):
            language = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1

            code = '\n'.join(code_lines)
            if code.strip():
                story.append(CodeBlock(code, language, code_font))
                story.append(Spacer(0, 6*mm))

        # Headers
        elif stripped.startswith("# "):
            heading = stripped[2:].strip()
            story.append(Paragraph(heading, title_style))
        elif stripped.startswith("## "):
            heading = parse_inline_formatting(stripped[3:].strip())
            story.append(Paragraph(heading, h2_style))
        elif stripped.startswith("### "):
            heading = parse_inline_formatting(stripped[4:].strip())
            story.append(Paragraph(heading, h3_style))

        # Horizontal rule
        elif stripped.startswith("---") or stripped.startswith("***"):
            story.append(Spacer(0, 5*mm))

        # Quotes
        elif stripped.startswith("> "):
            quote_text = parse_inline_formatting(stripped[2:].strip())
            story.append(Paragraph(f"<i>{quote_text}</i>", quote_style))

        # Lists
        elif stripped.startswith("- ") or stripped.startswith("* "):
            item = parse_inline_formatting(stripped[2:].strip())
            story.append(Paragraph(f"• {item}", list_style))
        elif re.match(r'^\d+\.', stripped):
            item = parse_inline_formatting(re.sub(r'^\d+\.\s*', '', stripped))
            story.append(Paragraph(item, list_style))

        # Tables (simple parsing)
        elif stripped.startswith("|") and "|" in stripped:
            table_lines = [stripped]
            i += 1
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1

            # Parse table
            if len(table_lines) >= 2:
                rows = []
                for tl in table_lines:
                    cells = [c.strip() for c in tl.split("|")[1:-1]]
                    rows.append(cells)

                if rows:
                    table = Table(rows)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), COLORS["table_header"]),
                        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS["table_header_text"]),
                        ('FONTNAME', (0, 0), (-1, 0), heading_font),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('GRID', (0, 0), (-1, -1), 0.5, COLORS["line"]),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS["table_even"], COLORS["table_odd"]]),
                        ('FONTNAME', (0, 1), (-1, -1), body_font),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ]))
                    story.append(table)
                    story.append(Spacer(0, 8*mm))

        # Regular text
        else:
            text = parse_inline_formatting(stripped)
            story.append(Paragraph(text, body_style))

        i += 1

    # Build PDF with header/footer
    def on_page(canvas, doc):
        hf = HeaderFooter(doc.pagesize, title)
        hf.draw_page_header_footer(canvas, doc)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

    return str(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_generator.py <markdown_file> [output_pdf] [page_size] [title]")
        print("Page sizes: A4, A5 (default), B5")
        print("\nExample: python pdf_generator.py notes.md")
        print("Example: python pdf_generator.py notes.md output.pdf A4")
        print("Example: python pdf_generator.py notes.md output.pdf A5 'My Notes'")
        sys.exit(1)

    md_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    page_size = sys.argv[3] if len(sys.argv) > 3 else "A5"
    title = sys.argv[4] if len(sys.argv) > 4 else None

    try:
        result = markdown_to_pdf(md_path, output_path, page_size, title)
        print(f"✓ PDF created: {result}")
        print(f"  Page size: {page_size}")
        if title:
            print(f"  Title: {title}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
