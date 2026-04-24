# DeepSeek Original Response — LLM API Compatibility & Best Practices

It's completely normal to feel there's a maze of different API rules out there. But here's some good news: the industry has largely consolidated around a single standard, which makes your goal very achievable. You had the core pieces right from the start—you only need an **API key**, a **base URL**, and a **model name** to get started with almost any provider.

### 🧩 The Key to Simplicity: The OpenAI API Standard

You're right to suspect that switching between models could be a tangled mess of code changes. The best practice that has emerged to solve this is for nearly every provider to make their API "OpenAI-compatible." This means you can use the exact same code (like the official `openai` Python library), and simply change those three pieces of information to talk to a completely different model from a different company.

In practice, the industry often uses libraries like **LiteLLM** to manage this. It acts as a universal translator, letting you call over 100 different LLMs using a single, consistent format in your code. But at its foundation, this works precisely because of the standardization around the OpenAI format. As of 2025-2026, the open-source library LiteLLM has become the most popular standard to provide a unified interface.

### 📝 What You Need to Collect

Below is the precise information you need to gather for each of the three models you mentioned. Storing these details securely will allow you to switch between them with zero code changes.

**OpenAI (GPT Models)**

| Credential | Specific Value / Format | Where to Find It |
| :--- | :--- | :--- |
| **API Key** | Looks like: `sk-proj-...` | **[OpenAI API Keys Page](https://platform.openai.com/api-keys)** |
| **Base URL** | `https://api.openai.com/v1` | This is the standard endpoint. You don't need to look for it. |
| **Model Name** | `gpt-4o`, `gpt-4o-mini`, `o3-mini`, etc. | **[OpenAI Models Page](https://platform.openai.com/docs/models)** |
| **Auth. Method** | `Bearer` Token (e.g., `Authorization: Bearer YOUR_KEY`) | You just need the key; the HTTP method is standard across all three. |
| **SDK Use** | Recommended: `pip install openai` | This is the official Python library. Your code won't change for other providers. |

**DeepSeek**

| Credential | Specific Value / Format | Where to Find It |
| :--- | :--- | :--- |
| **API Key** | Looks like: `sk-...` (a string provided by DeepSeek) | **[DeepSeek API Keys Page](https://platform.deepseek.com/api_keys)** |
| **Base URL** | `https://api.deepseek.com` | DeepSeek uses this as its standard base URL. |
| **Model Name** | `deepseek-chat` (for V3) or `deepseek-reasoner` (for R1) | **[DeepSeek Models Page](https://api-docs.deepseek.com/guides/models)** |
| **Auth. Method** | `Bearer` Token (uses the same `Authorization: Bearer YOUR_KEY` header as OpenAI) | Identical to the others. |
| **SDK Use** | Recommended: `pip install openai` | You can point the official OpenAI SDK to DeepSeek's servers. |

**Google Gemini**

**Important**: Google offers an official OpenAI-compatible endpoint. Be sure to use this new endpoint (`generativelanguage.googleapis.com/v1beta/openai`), which was created after Google made this compatibility available in 2025.

| Credential | Specific Value / Format | Where to Find It |
| :--- | :--- | :--- |
| **API Key** | Looks like: `AIza...` (a string from Google) | **[Google AI Studio API Keys](https://aistudio.google.com/apikey)** |
| **Base URL** | `https://generativelanguage.googleapis.com/v1beta/openai` | This is the *crucial* piece of information that makes it seamlessly compatible. |
| **Model Name** | `gemini-2.5-flash`, `gemini-2.5-pro`, etc. | **[Google Models Page](https://ai.google.dev/gemini-api/docs/models)** |
| **Auth. Method** | `Bearer` Token (uses the same `Authorization: Bearer YOUR_KEY` header) | While Google has other complex authentication methods, the OpenAI-compatible endpoint works in this simple, familiar way. |
| **SDK Use** | Recommended: `pip install openai` | Again, just point the OpenAI SDK to the base URL above and provide your Google key. |

---

With this list in hand, you can gather everything you need, store it securely as you planned, and build your application with confidence.
