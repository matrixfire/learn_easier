# DeepSeek Original Response — LiteLLM + GLM Demo

You're all set — with LiteLLM, using your GLM (Zhipu) service is straightforward. Because Zhipu's API is already OpenAI‑compatible, LiteLLM has a built‑in provider `zhipu/` that requires only your **API key** and the **model name**. The base URL you provided (`https://open.bigmodel.cn/api/paas/v4`) is already the default endpoint for this provider, so you don't need to specify it separately.

Here's a complete minimal demo.

---

### 🧪 Step‑by‑step demo

#### 1. Install LiteLLM
```bash
pip install litellm
```

#### 2. Set your API key as an environment variable
From the terminal (recommended for security):
```bash
export ZHIPU_API_KEY="cecc9ef3025e46c2a6e9eba6d4b39fb0.2Mn4EInAXGzejxr8"
```
Or, in your Python script for quick testing (avoid this in production):
```python
import os
os.environ["ZHIPU_API_KEY"] = "cecc9ef3025e46c2a6e9eba6d4b39fb0.2Mn4EInAXGzejxr8"
```

#### 3. Write the demo script
Create a file, say `demo.py`:

```python
from litellm import completion

# The model name – choose the one you have access to
# Common options: glm-4-flash, glm-4-plus, glm-4, glm-3-turbo
model = "zhipu/glm-4-flash"   # ⬅️ fast, inexpensive

# Send a simple greeting
response = completion(
    model=model,
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

# Print the reply
print(response.choices[0].message.content)
```

#### 4. Run it
```bash
python demo.py
```

That's all. LiteLLM automatically handles the authentication (Bearer token added to the header) and routes the request to `https://open.bigmodel.cn/api/paas/v4/chat/completions` using the standard OpenAI request format.

---

### 🔁 What if you need a custom base URL?

If you ever use a non‑default endpoint (e.g., a reseller), you can fall back to the generic `openai/` provider and supply the `api_base` directly:

```python
response = completion(
    model="openai/glm-4-flash",
    api_base="https://open.bigmodel.cn/api/paas/v4",   # your custom URL
    api_key="cecc9ef3025e46c2a6e9eba6d4b39fb0.2Mn4EInAXGzejxr8",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

But for Zhipu's official API, the built‑in `zhipu/` route is the cleanest choice.
