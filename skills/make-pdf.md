---
name: make-pdf
description: Convert markdown notes to professionally formatted PDF ebook with enhanced styling
---

# make-pdf

Converts markdown files to beautifully formatted PDF documents with ebook-standard page sizes.

## Usage

Convert a markdown file to PDF:
```
/make-pdf <markdown_file>
```

Specify output filename:
```
/make-pdf <markdown_file> <output_name>
```

Specify page size (A4, A5, B5):
```
/make-pdf <markdown_file> <output_name> <page_size>
```

## Examples

```bash
/make-pdf summaries/chapter01_computer_system_basics.md
/make-pdf summaries/git_basics.md git_guide A4
/make-pdf design_patterns.md design_ebook A5
```

## Page Sizes

| Size | Dimensions | Use Case |
|------|-----------|----------|
| A5 | 148 × 210 mm | Ebooks (default) |
| A4 | 210 × 297 mm | Documents |
| B5 | 176 × 250 mm | Books |

## Features

### Visual Design
- **Cover Page**: Centered title with current date
- **Color Header**: Blue background with title and date
- **Page Numbers**: Bottom-centered on every page
- **Professional Typography**: Optimized fonts and spacing
- **Color Scheme**: Modern blue/purple theme

### Content Rendering
- **Code Blocks**: Dark background with language label and monospace font
- **Inline Code**: Red text with gray background
- **Tables**: Colored headers with alternating row backgrounds
- **Markdown Support**: Headers, lists, quotes, bold, italic
- **Chinese Fonts**: Auto-detects Microsoft YaHei, SimSun, SimHei

### Technical
- UTF-8 support for multilingual content
- ISO 216 standard page sizes
- Proper margins and line heights
- Professional word wrapping

## Command Line

```bash
python pdf_generator.py <markdown_file> [output_pdf] [page_size] [title]
```

## Examples

```bash
# Default A5 ebook format
python pdf_generator.py notes.md

# A4 document with custom title
python pdf_generator.py notes.md output.pdf A4kt "My Notes"

# B5 book format
python pdf_generator.py book.md book.pdf B5
```
