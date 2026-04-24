# Gemini Original Response — LiteLLM Minimum Configuration

You made an excellent choice with LiteLLM! It is currently the industry favorite for exactly this reason.

Because you are using LiteLLM, I have some great news: **it actually reduces the amount of information you need to collect.** The entire purpose of LiteLLM is to manage the underlying routing for you. Because it already knows the official Base URLs for OpenAI, DeepSeek, and Google, **you no longer need to track the Base URLs yourself** (unless you are using a custom middleman/proxy).

Here are the absolute minimum **two things** you need to provide to make LiteLLM work:

### 1. The API Keys (Named Specifically)
LiteLLM automatically looks for specific environment variables in your `.env` file. You must name them exactly what LiteLLM expects:
* `OPENAI_API_KEY`
* `DEEPSEEK_API_KEY`
* `GEMINI_API_KEY`

### 2. The Model Name with a "Provider Prefix"
This is LiteLLM's secret sauce. To tell LiteLLM which API to wake up, you simply add the provider's name and a forward slash (`/`) to the front of the model name.
* **OpenAI:** `openai/gpt-4o` (or `gpt-3.5-turbo`)
* **DeepSeek:** `deepseek/deepseek-chat`
* **Gemini:** `gemini/gemini-1.5-flash`

---

### Your New, Simplified `.env` File

With LiteLLM, your secret configuration file shrinks down to just this:

```text
OPENAI_API_KEY="sk-abc123yourkeyhere"
DEEPSEEK_API_KEY="sk-def456yourkeyhere"
GEMINI_API_KEY="AIzaSy789yourkeyhere"
```

### The Code (How to switch seamlessly)

Here is the exact Python code demonstrating how perfectly LiteLLM achieves your goal. Notice how the code structure never changes; you just swap out the `model_name` string.

```python
import os
from dotenv import load_dotenv
from litellm import completion

# 1. Load your secret .env file
load_dotenv()

# 2. Define your prompt
messages = [{"role": "user", "content": "Hello! Write a one-sentence greeting."}]

# 3. Call OpenAI
response_gpt = completion(model="openai/gpt-4o", messages=messages)
print("GPT says:", response_gpt.choices[0].message.content)

# 4. Call DeepSeek (Code doesn't change, just the model name!)
response_deepseek = completion(model="deepseek/deepseek-chat", messages=messages)
print("DeepSeek says:", response_deepseek.choices[0].message.content)

# 5. Call Gemini
response_gemini = completion(model="gemini/gemini-1.5-flash", messages=messages)
print("Gemini says:", response_gemini.choices[0].message.content)
```

By providing just the API keys and the prefixed model names, LiteLLM handles all the differing documentation, formats, and backend routing automatically.
