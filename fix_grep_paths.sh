#!/bin/bash

# 批量修复所有 data-queries.md 文件中的 grep 路径

echo "开始修复 grep 路径..."

# 查找所有包含错误路径的 data-queries.md 文件
find .claude/skills -name "data-queries.md" -type f | while read file; do
    if grep -q "skills/lixinger-data-query" "$file"; then
        echo "修复: $file"
        # 使用 sed 替换路径
        sed -i '' 's|skills/lixinger-data-query/api_new/api-docs/|../../lixinger-data-query/api_new/api-docs/|g' "$file"
        sed -i '' 's|skills/lixinger-data-query/api_new/akshare_data/|../../lixinger-data-query/api_new/akshare_data/|g' "$file"
    fi
done

echo "完成！"
