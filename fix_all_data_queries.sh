#!/bin/bash

# 批量修复所有 data-queries.md 文件中的常见错误

echo "开始批量修复 data-queries.md 文件..."

# 1. 修复所有过时的日期（2024 → 2026）
echo "1. 修复过时日期..."
find skills -name "data-queries.md" -type f -exec sed -i.bak \
  -e 's/"date": "2024-[0-9][0-9]-[0-9][0-9]"/"date": "2026-02-24"/g' \
  -e 's/"startDate": "2024-[0-9][0-9]-[0-9][0-9]"/"startDate": "2026-01-01"/g' \
  -e 's/"endDate": "2024-[0-9][0-9]-[0-9][0-9]"/"endDate": "2026-02-24"/g' \
  {} \;

# 2. 为所有没有 --limit 的查询添加 --limit 20
echo "2. 添加 --limit 参数..."
find skills -name "data-queries.md" -type f -exec sed -i.bak \
  -e '/query_tool.py/,/^```/ { /--limit/! { /^```/i\  --limit 20
  } }' \
  {} \;

# 3. 修复 API 路径中的点号为斜杠（但保留 metricsList 中的点号）
echo "3. 修复 API 路径格式..."
find skills -name "data-queries.md" -type f -exec sed -i.bak \
  -e 's|--suffix "cn\.company\.|--suffix "cn/company/|g' \
  -e 's|--suffix "cn\.index\.|--suffix "cn/index/|g' \
  -e 's|--suffix "cn\.industry\.|--suffix "cn/industry/|g' \
  -e 's|--suffix "hk\.company\.|--suffix "hk/company/|g' \
  -e 's|--suffix "hk\.index\.|--suffix "hk/index/|g' \
  -e 's|--suffix "us\.company\.|--suffix "us/company/|g' \
  -e 's|--suffix "us\.index\.|--suffix "us/index/|g' \
  -e 's|--suffix "macro\.|--suffix "macro/|g' \
  {} \;

# 4. 清理备份文件
echo "4. 清理备份文件..."
find skills -name "data-queries.md.bak" -type f -delete

echo "✅ 批量修复完成！"
echo ""
echo "修复内容："
echo "- 更新所有 2024 年日期为 2026 年"
echo "- 为缺少 --limit 的查询添加 --limit 20"
echo "- 修复 API 路径中的点号为斜杠"
