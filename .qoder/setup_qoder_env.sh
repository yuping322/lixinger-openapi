#!/bin/bash
# Qoder环境配置脚本 for lixinger-openapi skills

echo "🔧 正在配置Qoder环境..."

# 设置工作目录
cd /Users/fengzhi/Downloads/git/lixinger-openapi/skills

# 激活虚拟环境
if [ -d "../.venv" ]; then
    source ../.venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
fi

# 设置环境变量
export PYTHONPATH=/Users/fengzhi/Downloads/git/lixinger-openapi
export FINSKILLS_CACHE_DIR=/tmp/finskills-cache

# 检查token配置
if [ -f "/Users/fengzhi/Downloads/git/lixinger-openapi/token.cfg" ]; then
    export LIXINGER_TOKEN=$(cat /Users/fengzhi/Downloads/git/lixinger-openapi/token.cfg)
    echo "✅ Token配置已加载"
else
    echo "❌ 未找到token配置文件"
fi

echo "📊 当前工作目录: $(pwd)"
echo "🐍 Python路径: $PYTHONPATH"
echo "📂 缓存目录: $FINSKILLS_CACHE_DIR"

# 显示可用的技能目录
echo -e "\n📚 可用的技能包:"
echo "   - China-market (57个技能)"
echo "   - US-market (36个技能)" 
echo "   - HK-market (14个技能)"
echo "   - lixinger-data-query (核心查询技能)"

echo -e "\n🚀 Qoder环境配置完成！"
echo "💡 使用方法："
echo "   toolkit-cn --help    # 查看A股工具帮助"
echo "   toolkit-us --help    # 查看美股工具帮助" 
echo "   toolkit-hk --help    # 查看港股工具帮助"
echo "   query-data --help    # 查看数据查询帮助"

# 保持环境激活
exec $SHELL