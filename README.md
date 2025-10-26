# Top03-Kuai 项目

基于实时网络搜索和AI分析的动态商品推荐引擎。

## 🚀 项目特色

- **实时网络搜索**: 利用Serper.dev API获取最新商品信息
- **AI智能分析**: 使用Claude 3 Opus进行深度分析和推荐
- **动态配置**: 支持管理员自定义API密钥和提示词
- **响应式设计**: 现代化的用户界面
- **缓存优化**: Redis缓存提升性能

## 📋 技术栈

### 后端
- **框架**: FastAPI (Python 3.11)
- **数据库**: PostgreSQL (配置存储)
- **缓存**: Redis
- **搜索API**: Serper.dev
- **LLM**: Claude 3 Opus / GPT-4o

### 前端
- **框架**: Next.js 14 + React 18
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **部署**: Vercel / Netlify / GitHub Pages

## 🏗️ 项目结构

```
top03-kuai/
├── backend/                 # 后端服务
│   ├── app/                # FastAPI应用
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile         # Docker配置
├── frontend/               # 前端应用
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   ├── package.json       # Node.js依赖
│   └── Dockerfile         # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── .env.example          # 环境变量模板
└── README.md             # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd top03-kuai

# 安装依赖
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 并填写实际的API密钥：

```bash
cp .env.example .env
```

需要配置的环境变量：
- `SERPER_API_KEY`: Serper.dev API密钥
- `ANTHROPIC_API_KEY`: Claude API密钥
- `OPENAI_API_KEY`: OpenAI API密钥（可选）
- `DATABASE_URL`: PostgreSQL连接字符串
- `REDIS_URL`: Redis连接字符串

### 3. 使用Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 4. 手动部署

#### 后端服务
```bash
cd backend
python main.py
```

#### 前端服务
```bash
cd frontend
npm run dev
```

## 📊 API接口

### 获取Top3推荐
```
POST /api/v1/top3
Content-Type: application/json

{
  "keyword": "无线耳机"
}
```

### 管理后台
```
GET /admin
POST /admin/config
```

## 🎯 使用GitHub Pages部署前端

### 1. 配置Next.js静态导出

修改 `frontend/next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // 添加这一行
  // 其他配置...
}

module.exports = nextConfig
```

### 2. 构建静态站点

```bash
cd frontend
npm run build
npm run export  # 生成静态文件到 out/ 目录
```

### 3. 配置GitHub Pages

1. 在GitHub仓库设置中，进入 **Settings** > **Pages**
2. 选择 **Source** 为 **GitHub Actions**
3. 创建 `.github/workflows/pages.yml` 文件：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Build
        run: |
          cd frontend
          npm run build
          npm run export

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/out
```

### 4. 配置自定义域名（可选）

在 `frontend/public/` 目录下创建 `CNAME` 文件：

```
your-domain.com
```

## 🔧 开发指南

### 代码规范
- 使用ESLint和Prettier进行代码格式化
- 遵循TypeScript严格模式
- 使用Git提交规范

### 测试
```bash
# 前端测试
cd frontend && npm test

# 后端测试
cd backend && pytest
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系

如有问题，请通过GitHub Issue联系。