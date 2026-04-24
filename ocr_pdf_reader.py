import sys
import io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz  # pymupdf
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

def ocr_pdf(pdf_path: str, pages: str = "all") -> str:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    if pages == "all":
        page_indices = list(range(total_pages))
    elif "-" in pages:
        start, end = map(int, pages.split("-"))
        page_indices = list(range(start - 1, min(end, total_pages)))
    else:
        page_num = int(pages) - 1
        page_indices = [page_num] if 0 <= page_num < total_pages else []

    results = []
    for i in page_indices:
        page = doc[i]
        # Render page to image at 200 DPI
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")

        # Run OCR
        ocr_result, _ = ocr(img_bytes)
        text_lines = []
        if ocr_result:
            for line in ocr_result:
                text_lines.append(line[1])

        page_text = "\n".join(text_lines)
        results.append(f"--- Page {i + 1} ---\n{page_text}")
        print(f"OCR page {i + 1}/{total_pages} done", file=sys.stderr)

    doc.close()
    return "\n\n".join(results)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_pdf_reader.py <pdf_path> [pages] [output_file]")
        print("Pages: 'all', '1-5', '3'")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else "all"
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        text = ocr_pdf(pdf_path, pages)
        if output_file:
            Path(output_file).write_text(text, encoding="utf-8")
            print(f"Output saved to: {output_file}", file=sys.stderr)
        else:
            print(text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
