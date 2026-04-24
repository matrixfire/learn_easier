import os
import sys
import io
import fitz
import easyocr
import tempfile

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

pdf_path = sys.argv[1] if len(sys.argv) > 1 else r"软考资料/2022.11系统架构设计师真题及解析.pdf"
start_page = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end_page = int(sys.argv[3]) if len(sys.argv) > 3 else None

output_dir = r"软考资料/temp_images_2022"
os.makedirs(output_dir, exist_ok=True)

# Extract pages as images if not already done
doc = fitz.open(pdf_path)
total = len(doc)
print(f"Total pages: {total}", file=sys.stderr)

# Ensure images exist
for i in range(total):
    img_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
    if not os.path.exists(img_path):
        page = doc[i]
        pix = page.get_pixmap(dpi=200)
        pix.save(img_path)
doc.close()

# Initialize OCR reader
print("Initializing EasyOCR...", file=sys.stderr)
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("EasyOCR ready.", file=sys.stderr)

if end_page is None:
    end_page = total

# OCR each page
for i in range(start_page, min(end_page, total)):
    img_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
    print(f"Processing page {i+1}...", file=sys.stderr)
    # Copy to temp file with ASCII name (OpenCV can't handle Chinese paths)
    import shutil
    tmp_path = os.path.join(tempfile.gettempdir(), f"ocr_page_{i+1}.png")
    shutil.copy2(img_path, tmp_path)
    results = reader.readtext(tmp_path, detail=0)
    os.unlink(tmp_path)
    text = '\n'.join(results)
    print(f"--- Page {i+1} ---")
    print(text)
    print()

print("Done.", file=sys.stderr)
