# DeepSeek Original Response — LLM API Minimum Requirements

You're exactly right: at minimum you need **two things** — an **API key** (or token) and a **base URL**.
To make your client truly model‑agnostic, add one more: the **model name**.

So the absolute minimum set of credentials for each provider/service is:

| Credential | Example | Notes |
|------------|---------|-------|
| **API Key** | `sk-abc123...` | Sometimes called "token" or "secret". Usually passed in an `Authorization: Bearer <key>` header. |
| **Base URL** | `https://api.openai.com/v1` | The root of the API. If the provider follows the OpenAI standard (most do), requests are sent to `{base_url}/chat/completions`. |
| **Model Name** | `gpt-4o`, `deepseek-chat`, `gemini-2.0-flash` | Tells the server *which* model to run. Even with the same base URL, a provider may offer multiple models. |

That's it. With these three pieces you can call almost any LLM that exposes an OpenAI‑compatible interface (which DeepSeek, Gemini via Vertex/GenAI, and many resellers do).

**A quick note on Gemini** — if you use Google's official SDK, the authentication is different (a service account JSON or API key in a parameter), but you can also access Gemini through OpenAI‑compatible endpoints (like via Google's own `generativelanguage.googleapis.com` when properly configured, or through middlemen like OpenRouter), so storing a base URL + key + model still works perfectly.

### For a central, provider‑agnostic config file
A simple JSON or YAML file holding an array of configurations is enough. Example:

```json
[
  {
    "provider": "openai",
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-...",
    "model": "gpt-4o"
  },
  {
    "provider": "deepseek",
    "base_url": "https://api.deepseek.com/v1",
    "api_key": "sk-...",
    "model": "deepseek-chat"
  },
  {
    "provider": "gemini_reshaped",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
    "api_key": "your-google-key",
    "model": "gemini-2.0-flash"
  }
]
```

Your client code then reads from this file, picks an entry, and sends requests to `base_url` with the corresponding key and model name. Because all three use the same OpenAI request format (`/chat/completions`), the client doesn't need to change any logic — just swap the configuration entry.

You were spot on. Nothing else is required.
