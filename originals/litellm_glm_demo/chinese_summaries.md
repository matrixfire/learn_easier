# LiteLLM + GLM (智谱) 实战演示 — 三家 AI 回答的中文总结

---

## DeepSeek 回答总结

### 核心结论
LiteLLM 内置了 `zhipu/` 专用路由，只需 **API Key + Model Name**，Base URL 已内置默认值，无需手动指定。

### 使用步骤
1. `pip install litellm`
2. 设置环境变量 `ZHIPU_API_KEY`
3. 调用 `completion(model="zhipu/glm-4-flash", messages=[...])`

### 两种调用方式

| 方式 | Model 写法 | 是否需要 api_base | 适用场景 |
|------|-----------|------------------|---------|
| 专用路由（推荐） | `zhipu/glm-4-flash` | 不需要，LiteLLM 内置 | 用智谱官方 API |
| 通用 OpenAI 路由 | `openai/glm-4-flash` | 需要，手动传 `api_base` | 用中间商/自托管 |

### 可用模型
`glm-4-flash`（快、便宜）、`glm-4-plus`、`glm-4`、`glm-3-turbo`

---

## ChatGPT 回答总结

### 安全警告
你粘贴了 API Key，**应该立即撤销/重新生成**。

### GLM 的关键事实
- 智谱 v4 API 是 **OpenAI 兼容**的——同样的 `/chat/completions` 格式和消息结构

### 最低需要四样
1. **API Key**（从智谱获取）
2. **Base URL**：`https://open.bigmodel.cn/api/paas/v4`
3. **Model Name**：如 `glm-4.7`、`glm-4.5`、`glm-5`
4. **Provider 映射**：用 `openai/glm-4.7`，因为 LiteLLM 把 GLM 当 OpenAI 兼容后端

### 为什么能工作
```
你的代码 → LiteLLM → OpenAI 兼容适配层 → GLM API（智谱端点）
```

### 推荐做法：用环境变量
- `export ZHIPU_API_KEY="your-key"`
- 代码里用 `os.getenv("ZHIPU_API_KEY")`

### 模型切换只需改一个字符串
- GPT: `openai/gpt-4o`
- GLM: `openai/glm-4.7`
- DeepSeek: `deepseek/deepseek-chat`

### 注意事项
- 模型命名可能不同（`glm-4.7` vs `glm-4` vs `glm-5`），报 "model not found" 是命名不匹配，不是 LiteLLM 的问题

---

## Gemini 回答总结

### 安全警告（最醒目）
- 开头就用大红色警告：你暴露了真实 API Key，**立刻去智谱开发者后台撤销**
- "把 API Key 当银行密码对待"

### 使用步骤
1. `pip install litellm`
2. 代码里直接用 `openai/` 前缀 + `api_base` + `api_key`
3. 调用 `completion(model="openai/glm-4", api_key=..., api_base=..., messages=...)`

### 关键解释
- `openai/` 前缀告诉 LiteLLM："用标准 OpenAI 格式，但发到我自己提供的 Base URL"
- 包含 try/except 错误处理

### 切换到其他模型
改 `api_key`、删掉 `api_base`（LiteLLM 内置了 OpenAI 地址）、改 model 名即可

---

## 三家回答对比

| 主题 | DeepSeek | ChatGPT | Gemini |
|------|----------|---------|--------|
| 调用方式 | `zhipu/glm-4-flash`（专用路由，最简洁） | `openai/glm-4.7` + `api_base`（通用路由） | `openai/glm-4` + `api_base`（通用路由） |
| 是否需要 api_base | 不需要（内置默认） | 需要 | 需要 |
| 环境变量名 | `ZHIPU_API_KEY` | `ZHIPU_API_KEY` | 直接硬编码（演示用） |
| 安全提醒 | 无 | 有，建议撤销 Key | 最醒目，开头大段红色警告 |
| 错误处理 | 无 | 无 | 有 try/except |
| 独特亮点 | 提供两种调用方式对比（专用 vs 通用）；最简洁 | 解释了调用链路；提到了模型命名差异问题；环境变量最佳实践 | 唯一带错误处理；解释了 `openai/` 前缀的含义 |

### 关键差异：调用方式
- **DeepSeek 说**：用 `zhipu/` 专用路由，不需要 `api_base`，最干净
- **ChatGPT 和 Gemini 说**：用 `openai/` 通用路由 + `api_base`，更显式

两种都能工作。如果 LiteLLM 版本支持 `zhipu/` 路由，DeepSeek 的方式更简洁；如果版本较旧不支持，ChatGPT/Gemini 的通用方式更稳妥。
