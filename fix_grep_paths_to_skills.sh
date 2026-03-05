#!/bin/bash

# 将 grep/cat 命令中的相对路径改为从项目根目录执行的路径

echo "开始修复 grep/cat 命令路径..."

# 修复 .claude/skills/analysis-market/ 目录下的文件
find .claude/skills/analysis-market -name "*.md" -type f | while read file; do
    if grep -q '\.\./lixinger-data-query' "$file"; then
        echo "修复: $file"
        sed -i '' 's|\.\./lixinger-data-query|.claude/skills/lixinger-data-query|g' "$file"
    fi
done

echo "完成！"
