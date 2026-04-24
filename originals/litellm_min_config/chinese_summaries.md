# LiteLLM 最低配置 — 三家 AI 回答的中文总结

---

## DeepSeek 回答总结

### 核心结论
用 LiteLLM 后，每家模型只需要 **Provider 前缀 + Model Name + API Key**，LiteLLM 自动处理端点和协议转换。

### 三家配置清单

| | OpenAI | DeepSeek | Gemini |
|---|---|---|---|
| **Provider 前缀** | `openai/`（可省略，自动识别） | `deepseek/`（必须加） | `gemini/`（必须加） |
| **Model Name** | `gpt-4o`, `gpt-4o-mini`, `o3-mini` | `deepseek-chat`, `deepseek-reasoner` | `gemini-2.0-flash`, `gemini-2.5-pro` |
| **API Key** | `sk-...` → 环境变量 `OPENAI_API_KEY` | `sk-...` → 环境变量 `DEEPSEEK_API_KEY` | `AIza...` → 环境变量 `GEMINI_API_KEY` |

### 与不用 LiteLLM 的对比
- 不用 LiteLLM：需要 API Key + Base URL + Model Name
- 用 LiteLLM：只需要 API Key + Model Name（带 provider 前缀），Base URL 由 LiteLLM 内置处理

---

## ChatGPT 回答总结

### 最低需要三样，但 Base URL 变成可选

| 必需程度 | 配置项 | 说明 |
|----------|--------|------|
| **必须** | Model 字符串（带 provider 前缀） | 如 `openai/gpt-4o`，这是 LiteLLM 最重要的抽象层 |
| **必须** | API Key | 通过环境变量提供（`OPENAI_API_KEY` 等） |
| **仅有时需要** | Base URL | 自托管、代理/网关、Azure 时才需设置，大多数情况 LiteLLM 内置了 |

### LiteLLM 消除了什么
- 不同 SDK（OpenAI/Google/DeepSeek 各自的库）
- 不同请求格式
- 不同认证头
- 不同流式格式
- 全部变成一个函数调用：`completion(model="openai/gpt-4o", messages=[...])`

### 核心抽象
> "model string 替代了 provider SDK 的复杂性"

### 关键隐藏要求：provider 前缀路由
- `openai/...`、`anthropic/...`、`azure/...` 告诉 LiteLLM 用哪个后端适配器
- 配置里必须保留这个前缀映射

### 中心配置文件结构
每家只需 `api_key` + `model`（带前缀），可选加 `api_base`、`type`、`timeout`、`max_tokens`、`temperature`

### 终极心智模型
> 你不再调"OpenAI 或 DeepSeek"，而是调 **"model + credentials + optional endpoint"**

---

## Gemini 回答总结

### 核心好消息：用 LiteLLM 后配置更少了
- LiteLLM 已内置各家 Base URL，**你不再需要自己跟踪 Base URL**（除非用自定义中间商/代理）

### 只需要两样东西

1. **API Key**（按 LiteLLM 规定的环境变量名）
   - `OPENAI_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `GEMINI_API_KEY`

2. **Model Name + Provider 前缀**（LiteLLM 的"秘方"）
   - `openai/gpt-4o`
   - `deepseek/deepseek-chat`
   - `gemini/gemini-1.5-flash`

### .env 文件极简版
只剩三行 Key，不再有 Base URL 和 Model 行

### 可运行的代码示例
- `load_dotenv()` 加载 .env
- 统一用 `completion(model="前缀/模型名", messages=[...])` 调用
- 切换模型只改 model 字符串，代码结构不变

---

## 三家回答对比

| 主题 | DeepSeek | ChatGPT | Gemini |
|------|----------|---------|--------|
| 最低配置项 | 3 样：Provider 前缀 + Model + API Key | 2+1 样：Model 字符串 + API Key + (可选)Base URL | 2 样：API Key + 带前缀的 Model Name |
| Base URL 态度 | 未单独提及，隐含由 LiteLLM 处理 | 明确说"有时需要"（自托管/代理/Azure） | 明确说"不再需要"（除非用自定义代理） |
| 配置文件 | 表格形式，每家 3 行 | JSON 格式，含可选字段 | .env 只剩 Key，最简洁 |
| 代码示例 | 无 | 单行 `completion()` 调用 | 完整可运行的 Python 代码 |
| 独特亮点 | 三家完整表格；OpenAI 前缀可省略 | 提出隐藏要求（前缀路由）；列出 LiteLLM 消除的 4 项复杂性；Provider Registry 概念 | 唯一给出可运行代码；强调 .env 极简化 |
| 环境变量名差异 | 用 `GEMINI_API_KEY` | 用 `GOOGLE_API_KEY` | 用 `GEMINI_API_KEY` |

### 注意：环境变量名差异
- ChatGPT 说 Gemini 的 Key 用 `GOOGLE_API_KEY`
- DeepSeek 和 Gemini 说用 `GEMINI_API_KEY`
- 实际使用时需查 LiteLLM 文档确认当前版本的正确命名
