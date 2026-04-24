---
name: save-ai-responses
description: Save original AI responses from DeepSeek/ChatGPT/Gemini to originals/ folder and generate Chinese summaries with comparison tables
---

# save-ai-responses

Save original responses from multiple AI providers (DeepSeek, ChatGPT, Gemini) and generate Chinese summaries with a cross-provider comparison table.

## Usage

```
/save-ai-responses <topic>
```

Then paste the three AI responses in your message. Label each response so Claude knows which is which (e.g., "DeepSeek:", "ChatGPT:", "Gemini:").

## What it does

1. **Saves originals** — Each AI's response is saved verbatim (zero modification) to:
   - `originals/<topic>/deepseek_original.md`
   - `originals/<topic>/chatgpt_original.md`
   - `originals/<topic>/gemini_original.md`

2. **Writes Chinese summaries** — Creates `originals/<topic>/chinese_summaries.md` containing:
   - A Chinese summary of each AI's response
   - A comparison table at the end highlighting differences in depth, unique insights, and practical value

## Rules

- **Originals must be saved exactly as-is** — no editing, no formatting changes, no omissions
- **Summaries must be in Chinese**
- **Always include a comparison table** at the end of the summaries file
- Follow the existing naming pattern: `deepseek_original.md`, `chatgpt_original.md`, `gemini_original.md`, `chinese_summaries.md`
- Each original file should have a title header like `# DeepSeek Original Response — <Topic>`

## Example

```
/save-ai-responses llm_business_models
```

Then paste:

```
DeepSeek:
[paste DeepSeek's response here]

ChatGPT:
[paste ChatGPT's response here]

Gemini:
[paste Gemini's response here]
```

This will create:

```
originals/llm_business_models/
├── deepseek_original.md
├── chatgpt_original.md
├── gemini_original.md
└── chinese_summaries.md
```
