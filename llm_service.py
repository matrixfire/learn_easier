import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


# ==========================================
# 1. DEFINE YOUR CREDENTIALS
# ==========================================
GLM_API_KEY = os.getenv("GLM_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


# Model A: GLM (Zhipu)
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
GLM_MODEL_NAME = "openai/glm-4" # Prefix tells LiteLLM it's an OpenAI-compatible endpoint

# Model B: Minimax (Hosted on NVIDIA)
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL_NAME = "openai/minimaxai/minimax-m2.7" # Add openai/ prefix here too

# Model C: DeepSeek (Direct)
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1" # Notice the added /v1
DEEPSEEK_MODEL_NAME = "openai/deepseek-v4-flash" # We add openai/ to force standard routing


# ==========================================
# 2. DEFINE YOUR MESSAGE
# ==========================================
messages = [{"role": "user", "content": "Hi! Say a quick hello, and tell me a joke about your history AND WHO YOU THINK IS YOUR FATHER?"}]

# ==========================================
# 3. SWITCH BETWEEN MODELS SEAMLESSLY
# ==========================================

print("--- Calling GLM ---")
response_glm = completion(
    model=GLM_MODEL_NAME,
    api_key=GLM_API_KEY,
    api_base=GLM_BASE_URL,
    messages=messages
)
print("GLM Response:", response_glm.choices[0].message.content)


# print("\n--- Calling Minimax via NVIDIA ---")
# response_minimax = completion(
#     model=NVIDIA_MODEL_NAME,
#     api_key=NVIDIA_API_KEY,
#     api_base=NVIDIA_BASE_URL,
#     messages=messages
# )
# print("Minimax Response:", response_minimax.choices[0].message.content)



print("\n--- Calling DeepSeek ---")
try:
    response_deepseek = completion(
        model=DEEPSEEK_MODEL_NAME,
        api_key=DEEPSEEK_API_KEY,
        api_base=DEEPSEEK_BASE_URL,
        messages=messages
    )
    print("DeepSeek Response:", response_deepseek.choices[0].message.content)
except Exception as e:
    print(f"DeepSeek Error: {e}")