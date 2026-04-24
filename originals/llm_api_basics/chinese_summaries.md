# LLM API 调用最低要求 — 三家 AI 回答的中文总结

---

## DeepSeek 回答总结

### 核心结论
调用 LLM API 最低需要三样东西：**API Key + Base URL + Model Name**

| 凭证 | 示例 | 说明 |
|------|------|------|
| API Key | `sk-abc123...` | 有时叫 token/secret，放在请求头 `Authorization: Bearer <key>` 里 |
| Base URL | `https://api.openai.com/v1` | API 的根地址，请求发到 `{base_url}/chat/completions` |
| Model Name | `gpt-4o`、`deepseek-chat` | 告诉服务器跑哪个模型，同一 Base URL 下可能有多个模型 |

### 统一配置方案
- 用一个 JSON/YAML 文件存所有服务商的配置（provider、base_url、api_key、model）
- 代码读配置文件，选一个 entry 发请求
- 因为都走 OpenAI 兼容格式（`/chat/completions`），切换服务商只需换配置，代码逻辑不用改

### Gemini 特殊说明
- Google 官方 SDK 认证方式不同（服务账号 JSON 或 API Key 参数）
- 但也可以走 OpenAI 兼容端点（`generativelanguage.googleapis.com/v1beta/openai`），这样统一格式仍然适用

---

## ChatGPT 回答总结

### 最低要求（五层，但核心三个）

1. **API Key** — 身份认证 + 计费，放在 `Authorization: Bearer` 头里，几乎所有 API 必须有
2. **Base URL** — 决定请求路由到哪家公司的基础设施
3. **Model Name** — 非常重要但常被忽略，没有它 API 不知道跑哪个模型
4. **端点路径**（如 `/chat/completions`）— 通常被 SDK 隐藏，但底层需要
5. **请求格式**（messages 数组、role 字段等）— 不是凭证，但正确调用必须遵守

### 你的原始想法只差一个
- 你说"API 就是 API Key + Base URL" → **80-90% 正确，只缺了 Model Name**

### 不需要的东西
- 服务器硬件信息、模型权重、内部算法、GPU 访问、部署代码（除非自托管）

### 安全提醒（重要）
- **绝对不要**把 API Key 硬编码在代码里或提交到 GitHub
- 用环境变量（`.env`）或密钥管理器（AWS Secrets Manager、Vault 等）

### 架构名称
你想要的"中心配置文件 + 不改代码切换模型"叫 **LLM 抽象层 / Provider-Agnostic Client**

---

## Gemini 回答总结

### 三大必备要素

1. **API Key** — 你的秘密密码，告诉服务商"谁在请求、该找谁收钱"
2. **Base URL** — 请求发往的网址，用中间商或自托管时特别重要
3. **Model Name（你漏掉的关键）** — 同一个 Base URL 下托管了多个模型，不指定服务器不知道唤醒哪个 AI

### 实现无缝切换的方法

- **`.env` 文件**：把 API Key、Base URL、Model Name 存在环境变量文件里，代码从中读取，避免密钥泄露
- **OpenAI 兼容标准**：OpenAI API 格式已成行业标准，DeepSeek 和大多数中间商都兼容。切换 GPT → DeepSeek 只需改 `.env` 里的 Base URL 和 Model Name，代码不用动
- **抽象库**：对于 API 结构差异大的（如 Gemini 原生 API），用 **LiteLLM** 或 **LangChain** 做通用翻译层——写一次代码，库自动适配不同服务商

---

## 三家回答对比

| 主题 | DeepSeek | ChatGPT | Gemini |
|------|----------|---------|--------|
| 最低要求 | 3 样：Key + URL + Model | 3 样核心 + 2 样辅助（端点路径、请求格式） | 3 样：Key + URL + Model |
| 配置方案 | JSON 配置文件 + 代码读配置 | JSON 配置 + provider→config→请求 的切换 | `.env` 环境变量文件 |
| 无缝切换原理 | 都走 OpenAI 兼容格式，换配置即可 | 同上，叫"LLM 抽象层" | 同上，推荐 LiteLLM/LangChain 做适配 |
| 安全提醒 | 无 | 重点强调：不要硬编码 Key，用 `.env` 或密钥管理器 | 强调 `.env` 文件防止密钥泄露 |
| 独特亮点 | 给了完整 JSON 配置示例；Gemini 特殊认证的变通方案 | 最详细，列了"不需要的东西"清单；给架构命名；5 层拆分最细 | 最实用导向，直接给出 .env + OpenAI 兼容 + LiteLLM 三板斧 |
