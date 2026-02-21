#!/bin/bash
# 标记不支持的 Skills - 添加后缀 _UNSUPPORTED

cd /Users/fengzhi/Downloads/git/lixinger-openapi

echo "开始标记不支持的 Skills..."
echo "========================================"

# 定义不支持的 skills 列表
unsupported_skills=(
  "northbound-flow-analyzer"
  "hsgt-holdings-monitor"
  "ab-ah-premium-monitor"
  "concept-board-analyzer"
  "esg-screener"
  "share-repurchase-monitor"
  "st-delist-risk-scanner"
  "margin-risk-monitor"
  "ipo-lockup-risk-monitor"
  "goodwill-risk-monitor"
  "limit-up-pool-analyzer"
  "limit-up-limit-down-risk-checker"
)

# 遍历所有市场
for market in "China-market" "US-market" "HK-market"; do
  if [ -d "skills/$market" ]; then
    echo ""
    echo "处理 $market:"
    echo "----------------------------------------"

    for skill in "${unsupported_skills[@]}"; do
      skill_path="skills/$market/$skill"

      if [ -d "$skill_path" ]; then
        # 检查是否已经标记
        if [[ "$skill" == *"_UNSUPPORTED"* ]]; then
          echo "✓ 已标记: $skill"
        else
          # 添加后缀
          new_name="${skill}_UNSUPPORTED"
          new_path="skills/$market/$new_name"

          if [ ! -d "$new_path" ]; then
            mv "$skill_path" "$new_path"
            echo "✓ 标记: $skill -> $new_name"
          else
            echo "⚠ 目标已存在: $new_name"
          fi
        fi
      fi
    done
  fi
done

echo ""
echo "========================================"
echo "标记完成！"
echo ""
echo "不支持的 Skills 总计: ${#unsupported_skills[@]} 个"
echo ""
echo "原因："
echo "  - 北向资金、港股通数据：理杏仁不支持"
echo "  - 概念板块：理杏仁只有行业板块"
echo "  - 融资融券、限售解禁：理杏仁不支持"
echo "  - 涨跌停池：理杏仁无直接接口"
echo "  - ESG评级、回购数据：理杏仁不支持"
echo "  - ST股票列表：理杏仁无直接接口"
echo ""
