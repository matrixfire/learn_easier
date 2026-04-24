---
name: save-original
description: Save original files as-is to originals/ folder without any LLM processing or modification
---

# save-original

Save files exactly as they are to the `originals/` folder — no reading, no modifying, no LLM tokens wasted on content. Just a straight file copy.

## Usage

```
/save-original <file>
/save-original <file1> <file2> …
/save-original <file> <subfolder>
```

## What it does

Runs `bash save_original.sh` which:
1. Copies your file(s) to `originals/` (or `originals/<subfolder>/`)
2. Preserves the original content exactly — nothing is changed
3. If a file with the same name already exists, appends a timestamp instead of overwriting

## Examples

```
/save-original some_article.md
/save-original notes.txt chapter1
/save-original file1.md file2.md my_folder
```

## Why this skill exists

When you find material that's already good and you want to keep it as-is, you don't need LLM processing. This skill just copies the file — zero token cost on the content.
