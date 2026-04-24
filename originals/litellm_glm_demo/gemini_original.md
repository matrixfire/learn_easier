# Gemini Original Response — LiteLLM + GLM Demo

**🚨 First, a critical security warning:** You just shared a real, live API key in your prompt. If this is a real key, anyone who sees this can use it, and you will be billed for their usage. **You should go to your GLM/Zhipu developer dashboard and revoke/delete this key immediately after you finish testing.** Always treat API keys like your bank account password!

***

With that out of the way, let's build your demo. Zhipu AI (the makers of the GLM models) upgraded their `v4` API to be fully compatible with the standard OpenAI format.

Because of this, you can use LiteLLM in a very straightforward way. For a quick standalone demo, we won't even use a hidden `.env` file—we will just plug your exact credentials directly into a Python script so you can run it instantly.

### Step 1: Install LiteLLM
If you haven't already, open your terminal or command prompt and install the library:
```bash
pip install litellm
```

### Step 2: The Demo Code
Create a file named `demo.py` and paste the following code.

Notice how we use the `openai/` prefix before the model name (`glm-4`). This tells LiteLLM: *"Hey, treat this like a standard OpenAI request, but send it to the custom Base URL I'm providing instead."*

```python
from litellm import completion

# 1. Your credentials and endpoint
GLM_API_KEY = "cecc9ef3025e46c2a6e9eba6d4b39fb0.2Mn4EInAXGzejxr8"
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

# 2. Define the message you want to send
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Hello! Please write a short haiku about learning to code."}
]

print("Sending request to GLM...")

# 3. Call the model
try:
    response = completion(
        model="openai/glm-4",          # We use 'openai/' to tell LiteLLM to use the standard format
        api_key=GLM_API_KEY,           # Your secret token
        api_base=GLM_BASE_URL,         # The custom routing address
        messages=messages
    )

    # 4. Print the result
    print("\n--- GLM Response ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")
```

### Why this is awesome:
You just successfully mapped a custom Chinese LLM into the exact same standardized format we talked about earlier. If you wanted to swap this script back to ChatGPT, you would literally just change the `api_key`, remove the `api_base` (since LiteLLM knows OpenAI's default URL), and change the model to `gpt-4o`.

Run that script, and you should get a nice haiku back from GLM!
