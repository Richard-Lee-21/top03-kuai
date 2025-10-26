#!/bin/bash

# Top03-Kuai 项目部署脚本

echo "🚀 开始部署 Top03-Kuai 项目..."

# 检查是否安装了必要的工具
check_dependencies() {
    echo "📋 检查依赖..."
    
    if ! command -v git &> /dev/null; then
        echo "❌ Git 未安装，请先安装 Git"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ Node.js/NPM 未安装，请先安装 Node.js"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装，请先安装 Python3"
        exit 1
    fi
    
    echo "✅ 依赖检查完成"
}

# 初始化 Git 仓库
init_git() {
    echo "📦 初始化 Git 仓库..."
    
    if [ ! -d ".git" ]; then
        git init
        git add .
        git commit -m "Initial commit: Top03-Kuai project setup"
        echo "✅ Git 仓库初始化完成"
    else
        echo "ℹ️  Git 仓库已存在"
    fi
}

# 安装前端依赖并构建
build_frontend() {
    echo "🏗️ 构建前端应用..."
    
    cd frontend
    
    # 安装依赖
    if [ ! -d "node_modules" ]; then
        echo "📦 安装前端依赖..."
        npm install
    fi
    
    # 构建静态文件
    echo "🔨 构建静态文件..."
    npm run build
    npm run export
    
    if [ -d "out" ]; then
        echo "✅ 前端构建完成，静态文件位于 out/ 目录"
    else
        echo "❌ 前端构建失败"
        exit 1
    fi
    
    cd ..
}

# 配置 GitHub Pages
setup_github_pages() {
    echo "🌐 配置 GitHub Pages..."
    
    # 确保有 GitHub Actions 工作流
    if [ ! -f ".github/workflows/pages.yml" ]; then
        echo "❌ GitHub Actions 工作流文件不存在"
        exit 1
    fi
    
    echo "✅ GitHub Pages 配置完成"
}

# 显示部署说明
show_instructions() {
    echo ""
    echo "🎉 部署准备完成！"
    echo ""
    echo "下一步操作："
    echo "1. 创建 GitHub 仓库"
    echo "2. 添加远程仓库：git remote add origin <your-repo-url>"
    echo "3. 推送到 GitHub：git push -u origin main"
    echo "4. 在 GitHub 仓库设置中启用 Pages"
    echo "5. 等待 GitHub Actions 完成部署"
    echo ""
    echo "📖 详细说明请查看 README.md"
    echo ""
    echo "🔗 部署完成后，您的网站将可以通过以下方式访问："
    echo "   - GitHub Pages: https://<username>.github.io/<repository>/"
    echo "   - 自定义域名: https://your-domain.com (如果配置了)"
}

# 主函数
main() {
    check_dependencies
    init_git
    build_frontend
    setup_github_pages
    show_instructions
}

# 运行主函数
main "$@"