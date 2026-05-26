# CLAUDE.md — 文档问答系统前端

## 项目概览

基于 RAG 架构的智能文档问答系统前端。Vue 3 + TypeScript + Vite + Pinia 构建，支持文档上传、多会话管理和 SSE 流式对话。

## 技术栈与约定

- **Vue 3 Composition API** — 全部使用 `<script setup lang="ts">` 语法
- **Pinia Setup Stores** — store 命名 `useXxxStore`，ID 使用 kebab-case
- **路径别名** — `@/` 映射到 `src/`
- **CSS 变量** — 全局主题变量定义在 `App.vue` 的 `:root` 中
- **类型定义** — 集中放在 `src/types/index.ts`
- **API 层** — 按模块拆分 (`api/chat.ts`, `api/documents.ts`, `api/conversations.ts`)，Axios 实例在 `api/index.ts`

## 关键文件

| 文件 | 用途 |
|------|------|
| [src/main.ts](src/main.ts) | 入口：创建 Vue app、安装 Pinia、Router |
| [src/App.vue](src/App.vue) | 根组件：布局分发、初始化数据加载 |
| [src/api/index.ts](src/api/index.ts) | Axios 实例（baseURL `/api/v1`，timeout 60s） |
| [src/api/chat.ts](src/api/chat.ts) | SSE 流式对话（`fetch` + `ReadableStream`） |
| [src/stores/chat.ts](src/stores/chat.ts) | 聊天状态：消息列表、流式内容、中断控制 |
| [src/stores/conversation.ts](src/stores/conversation.ts) | 会话状态：列表、活跃会话 |
| [src/stores/document.ts](src/stores/document.ts) | 文档状态：列表、上传状态 |
| [vite.config.ts](vite.config.ts) | Vite 配置：Vue 插件、`@` 别名、API 代理到 `localhost:8000` |
| [tsconfig.json](tsconfig.json) | TypeScript 配置：strict、bundler moduleResolution |

## 开发命令

```bash
npm run dev      # 启动开发服务器 (5173)
npm run build    # 类型检查 + 构建
npm run preview  # 预览构建产物
npm run lint     # ESLint 检查 + 自动修复
```

## 数据流

```
Component → Pinia Store → API Layer → Backend (/api/*)
                                          ↑
                                   Vite Proxy (dev)
```

1. 组件通过 `useXxxStore()` 获取 store 实例
2. Store actions 调用 API 层函数
3. API 层通过 Axios 实例 (`/api/v1`) 或 `fetch`（SSE 流）请求后端
4. 开发环境下 Vite 将 `/api` 代理到 `localhost:8000`

## 流式对话流程

1. 用户输入 → `ChatInput.send()` → `chatStore.startStream(convId, query)`
2. `startStream` 先 push user message → 调用 `streamChat()` (fetch + ReadableStream)
3. `onToken` 追加到 `streamingContent` → `ChatWindow` 检测到变化渲染 `<ChatMessage is-streaming>`
4. 流式消息内使用 `TypewriterText` 做打字机效果
5. `onDone` push assistant message，清空 `streamingContent`

## 注意事项

- `streamChat` 使用原生 `fetch`（非 Axios），因为 Axios 不支持 SSE 流式读取
- `TypewriterText` 在 `ChatMessage` 内用于流式展示，`ChatWindow` 不需要单独引入
- 用户消息气泡用 `flex-direction: row-reverse` 实现右侧对齐
- 文档上传支持的格式：pdf, docx, doc, txt, md
