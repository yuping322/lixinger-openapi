#!/bin/bash

# 快速启动指南

echo "==================================="
echo "Findata Service 快速启动"
echo "==================================="
echo ""

# 1. 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，正在创建..."
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填入你的理杏仁 Token："
    echo "   LIXINGER_TOKEN=your_token_here"
    echo ""
    read -p "按回车键继续..."
fi

# 2. 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
    echo "✓ 虚拟环境创建完成"
fi

# 3. 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 4. 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "✓ 安装完成！"
echo "==================================="
echo ""
echo "启动服务："
echo "  python server.py"
echo ""
echo "或使用 uvicorn："
echo "  uvicorn server:app --reload"
echo ""
echo "API 文档："
echo "  http://localhost:8000/docs"
echo ""
