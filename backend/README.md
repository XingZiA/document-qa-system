# Document Q&A System - Backend

基于 FastAPI 的文档问答系统后端，支持多格式文档解析、向量检索和 LLM 流式对话。

## 技术栈

- **Web 框架**: FastAPI + Uvicorn
- **数据库**: SQLite + SQLAlchemy (异步)
- **向量存储**: FAISS
- **嵌入模型**: 阿里百炼 text-embedding-v3
- **LLM**: 阿里百炼 (qwen3-max / qwen-plus / qwen-turbo)
- **文档解析**: PyMuPDF + pdfplumber + python-docx

## 快速启动

```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

服务默认运行在 `http://localhost:8000`，API 文档自动生成在 `/docs`。

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── __main__.py          # python -m app 入口
│   ├── main.py              # FastAPI 应用主文件
│   ├── config.py            # 配置管理 (pydantic-settings)
│   ├── database.py          # 数据库连接与初始化
│   ├── api/
│   │   ├── chat.py          # 流式对话接口
│   │   ├── conversations.py # 会话管理 CRUD
│   │   ├── documents.py     # 文档上传与管理
│   │   ├── health.py        # 健康检查
│   │   ├── settings.py      # 系统设置
│   │   └── deps.py          # 公共依赖
│   ├── models/
│   │   ├── orm.py           # SQLAlchemy 数据模型
│   │   └── schemas.py       # Pydantic 请求/响应模型
│   └── services/
│       ├── chunker.py       # 文本切片
│       ├── embeddings.py    # 向量嵌入
│       ├── llm.py           # LLM 调用 (含视觉模型)
│       ├── parser.py        # 文档解析 (PDF/DOCX/TXT/MD)
│       ├── rag.py           # RAG 检索增强
│       └── vector_store.py  # FAISS 向量存储
├── data/                    # 运行时数据 (自动创建)
├── requirements.txt
└── pyproject.toml
```

## API 路由

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/health` | 健康检查 |
| POST | `/api/v1/documents/upload` | 上传文档 |
| GET | `/api/v1/documents` | 文档列表 |
| DELETE | `/api/v1/documents/{id}` | 删除文档 |
| POST | `/api/v1/conversations` | 创建会话 |
| GET | `/api/v1/conversations` | 会话列表 |
| GET | `/api/v1/conversations/{id}` | 会话详情 |
| GET | `/api/v1/conversations/{id}/messages` | 消息列表 |
| DELETE | `/api/v1/conversations/{id}` | 删除会话 |
| POST | `/api/v1/chat/{id}/stream` | 流式对话 (SSE) |
| GET | `/api/v1/settings` | 系统设置 |
| PUT | `/api/v1/settings/model` | 切换 LLM 模型 |

## 环境变量

在 `backend/` 目录下创建 `.env` 文件 (参考 `.env.example`)：

```env
DASHSCOPE_API_KEY=your_api_key
LLM_MODEL=qwen3-max
```

## 支持的文档格式

- PDF (含表格提取、图片图表识别)
- DOCX
- TXT
- Markdown
