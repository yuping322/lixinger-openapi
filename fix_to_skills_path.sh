#!/bin/bash

# 将所有路径统一改为 skills/lixinger-data-query（从项目根目录执行）

echo "开始统一路径为 skills/lixinger-data-query..."

# 修复 .claude/skills/analysis-market/ 目录下的文件
find .claude/skills/analysis-market -name "*.md" -type f | while read file; do
    if grep -q '\.claude/skills/lixinger-data-query' "$file"; then
        echo "修复: $file"
        sed -i '' 's|\.claude/skills/lixinger-data-query|skills/lixinger-data-query|g' "$file"
    fi
done

echo "完成！"
