import os
import sys
from pathlib import Path

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import pypdf
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def read_pdf(pdf_path: str, pages: str = "all") -> str:
    """
    Read a PDF file and return its text content.

    Args:
        pdf_path: Path to the PDF file
        pages: Page range to read (e.g., "1-5", "3", "all")

    Returns:
        Extracted text from the PDF
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        total_pages = len(reader.pages)

        if pages == "all":
            page_indices = list(range(total_pages))
        elif "-" in pages:
            start, end = map(int, pages.split("-"))
            page_indices = list(range(start - 1, min(end, total_pages)))
        else:
            page_num = int(pages) - 1
            page_indices = [page_num] if 0 <= page_num < total_pages else []

        text_parts = []
        for i in page_indices:
            page = reader.pages[i]
            text = page.extract_text()
            text_parts.append(f"--- Page {i + 1} ---\n{text}")

        return "\n\n".join(text_parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_reader.py <pdf_path> [pages]")
        print("Example: python pdf_reader.py document.pdf 1-5")
        print("Example: python pdf_reader.py document.pdf all")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else "all"

    try:
        text = read_pdf(pdf_path, pages)
        print(text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
