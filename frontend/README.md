# 文档问答系统 (Document QA System) - Frontend

基于 **RAG (Retrieval-Augmented Generation)** 架构的智能文档问答系统前端，支持多格式文档上传、流式对话和 Markdown 渲染。

## 技术栈

| 类型 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 (Composition API + `<script setup>`) | ^3.5 |
| 语言 | TypeScript | ~5.7 |
| 构建 | Vite | ^6.0 |
| 状态管理 | Pinia | ^2.3 |
| 路由 | Vue Router | ^4.5 |
| HTTP | Axios | ^1.7 |
| Markdown | marked + highlight.js | ^15 / ^11 |
| Lint | ESLint + typescript-eslint | - |

## 项目结构

```
frontend/
├── index.html                  # 入口 HTML
├── vite.config.ts              # Vite 构建配置
├── tsconfig.json               # TypeScript 配置
├── eslint.config.ts            # ESLint 配置
├── env.d.ts                    # 环境类型声明
├── package.json
├── .env.example                # 环境变量示例
├── .gitignore
├── README.md
└── src/
    ├── main.ts                 # 应用入口
    ├── App.vue                 # 根组件（布局 + 初始化）
    ├── api/                    # API 请求层
    │   ├── index.ts            # Axios 实例
    │   ├── chat.ts             # 流式对话 API
    │   ├── conversations.ts    # 会话 CRUD
    │   └── documents.ts        # 文档上传/管理
    ├── components/
    │   ├── chat/               # 聊天相关组件
    │   │   ├── ChatInput.vue   # 输入框
    │   │   ├── ChatMessage.vue # 消息气泡（Markdown 渲染）
    │   │   ├── ChatWindow.vue  # 消息列表容器
    │   │   └── TypewriterText.vue # 打字机效果
    │   ├── document/           # 文档相关组件
    │   │   ├── DocumentCard.vue   # 文档列表项
    │   │   └── DocumentUpload.vue # 上传弹窗（拖拽+点击）
    │   └── layout/             # 布局组件
    │       ├── AppHeader.vue   # 顶部栏
    │       └── AppSidebar.vue  # 侧边栏（会话+文档）
    ├── router/
    │   └── index.ts            # 路由配置
    ├── stores/                 # Pinia 状态管理
    │   ├── chat.ts             # 聊天状态（消息、流式）
    │   ├── conversation.ts     # 会话列表状态
    │   └── document.ts         # 文档列表状态
    ├── types/
    │   └── index.ts            # 全局 TypeScript 类型定义
    └── views/
        └── HomeView.vue        # 主页面
```

## 快速开始

### 前置条件

- Node.js >= 18
- 后端服务运行在 `http://localhost:8000`

### 安装与运行

```bash
# 安装依赖
npm install

# 启动开发服务器 (http://localhost:5173)
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### 环境变量

复制 `.env.example` 为 `.env` 并按需修改：

```bash
cp .env.example .env
```

所有客户端暴露的变量必须以 `VITE_` 为前缀。

### 后端代理

开发模式下，`/api` 请求自动代理到 `http://localhost:8000`，配置见 [vite.config.ts](vite.config.ts)。

## 功能特性

- **多格式文档上传** — 支持 PDF、Word (.doc/.docx)、TXT、Markdown，拖拽或点击上传
- **智能问答** — 基于 RAG 架构，结合上传文档进行语义检索和回答
- **流式输出** — SSE 流式接收 AI 回复，配合打字机效果实时渲染
- **Markdown 渲染** — 支持代码高亮、表格、列表等完整 Markdown 语法
- **多会话管理** — 新建/切换/删除对话，每条对话独立上下文

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/documents/upload` | 上传文档 (multipart/form-data) |
| GET | `/api/v1/documents` | 获取文档列表 |
| DELETE | `/api/v1/documents/:id` | 删除文档 |
| POST | `/api/v1/conversations` | 创建会话 |
| GET | `/api/v1/conversations` | 获取会话列表 |
| DELETE | `/api/v1/conversations/:id` | 删除会话 |
| GET | `/api/v1/conversations/:id/messages` | 获取历史消息 |
| POST | `/api/v1/chat/:id/stream` | 流式对话 (SSE) |

## 编码规范

### Vue 组件

- 使用 `<script setup lang="ts">` 语法
- Props 使用 TypeScript 泛型定义：`defineProps<{ ... }>()`
- Emits 使用类型标注：`defineEmits<{ close: [] }>()`
- 样式使用 `<style scoped>`，变量通过 CSS 自定义属性 `--xxx` 传递

### Pinia Store

- 命名：`useXxxStore`（如 `useChatStore`）
- Store ID 使用 kebab-case（如 `'chat'`）
- 使用 Composition API 风格（Setup Store）

### TypeScript

- 接口定义集中在 `src/types/index.ts`
- 路径别名 `@/` 映射到 `src/`
- 启用 strict 模式
