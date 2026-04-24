# DeepSeek Original Response — LiteLLM Minimum Configuration

Using LiteLLM, the minimum configuration needed for each model is indeed very close to what you initially suspected: an **API Key** and the **Model Name**. LiteLLM handles the specific endpoint and protocol translation for you, providing a unified interface (the industry-standard OpenAI format) so you can switch between them with no code changes.

Here are the exact three things to provide for each model.

---

### 📝 Minimum Configuration Checklist for LiteLLM

**OpenAI (GPT)**

| Credential | Specific Value | How to Set It Up in LiteLLM |
| :--- | :--- | :--- |
| **Provider Route** | `openai/` | Use this as a prefix for the model name (e.g., `openai/gpt-4o`), or no prefix with `gpt-4o` to auto-detect OpenAI. |
| **Model Name** | `gpt-4o`, `gpt-4o-mini`, `o3-mini`, etc. | The exact model you want to use. |
| **API Key** | Looks like: `sk-...` | Set as the environment variable `OPENAI_API_KEY`. |

**DeepSeek**

| Credential | Specific Value | How to Set It Up in LiteLLM |
| :--- | :--- | :--- |
| **Provider Route** | `deepseek/` | Must be used as a prefix for the model name (e.g., `deepseek/deepseek-chat`) to route to DeepSeek. |
| **Model Name** | `deepseek-chat`, `deepseek-reasoner` | The exact model you want. All DeepSeek models are supported. |
| **API Key** | Looks like: `sk-...` (a string provided by DeepSeek) | Set as the environment variable `DEEPSEEK_API_KEY`. |

**Google Gemini**

| Credential | Specific Value | How to Set It Up in LiteLLM |
| :--- | :--- | :--- |
| **Provider Route** | `gemini/` | Must be used as a prefix for the model name (e.g., `gemini/gemini-2.0-flash`) to route to Google AI Studio using a simple API key. |
| **Model Name** | `gemini-2.0-flash`, `gemini-2.5-pro`, etc. | The exact model you want. |
| **API Key** | Looks like: `AIza...` (a string from Google) | Set as the environment variable `GEMINI_API_KEY`. |

---

That's it. For a simple greeting request with any of these providers, LiteLLM only requires the correct **model identifier** and an **API key** set as an environment variable. The library handles the network request formatting automatically.
