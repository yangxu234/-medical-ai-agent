# Medical AI Agent

医疗健康咨询AI Agent平台 - 通过AI技术为用户提供健康建议和就医指导。

## 项目特点

- 🤖 AI Agent驱动的健康咨询
- 🔒 支持多模型配置（DeepSeek/OpenAI/Claude等）
- 🛡️ 安全过滤，提供负责任的健康建议
- 💬 多轮对话，上下文记忆

## 技术栈

**后端:**
- Python + FastAPI
- LangChain (AI Agent框架)
- SQLAlchemy (ORM)
- ChromaDB (向量数据库)

**前端:**
- Vue 3 + TypeScript
- Vite
- Pinia (状态管理)
- Element Plus

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量
cp ../.env.example .env
# 编辑 .env 文件填入你的 API Key

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 访问应用

- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 项目结构

```
medical-ai-agent/
├── backend/                 # Python后端
│   ├── app/
│   │   ├── main.py         # FastAPI入口
│   │   ├── config.py       # 配置管理
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # 数据校验
│   │   ├── api/            # API路由
│   │   ├── agent/          # AI Agent核心
│   │   └── utils/          # 工具函数
│   └── knowledge_base/     # 医学知识库
├── frontend/               # Vue3前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── stores/         # 状态管理
│   │   └── api/            # API调用
│   └── package.json
└── README.md
```

## 注意事项

⚠️ 本平台仅提供健康建议，不构成医疗诊断或治疗方案。如有健康问题，请及时就医并咨询专业医疗人员。

## License

MIT
