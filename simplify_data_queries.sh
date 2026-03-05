#!/bin/bash

# 简化所有 data-queries.md 文件，移除冗余的 grep 和 cat 命令说明

echo "开始简化 data-queries.md 文件..."

find .claude/skills -name "data-queries.md" -type f | while read file; do
    # 检查文件是否包含 "查找更多 API" 部分
    if grep -q "查找更多 API" "$file"; then
        echo "简化: $file"
        
        # 使用 sed 删除 "查找更多 API" 部分，替换为简单的引用
        # 创建临时文件
        temp_file="${file}.tmp"
        
        # 读取文件直到 "查找更多 API" 部分，然后替换
        awk '
        /^## 查找更多 API/ {
            print "## 查找更多 API\n"
            print "详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`\n"
            # 跳过直到文件结束或下一个主要部分
            while (getline > 0) {
                if (/^## / && !/^## 查找更多 API/) {
                    print
                    break
                }
            }
            next
        }
        { print }
        ' "$file" > "$temp_file"
        
        # 替换原文件
        mv "$temp_file" "$file"
    fi
done

echo "完成！"
