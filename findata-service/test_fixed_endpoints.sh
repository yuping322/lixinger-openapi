#!/bin/bash
# 测试修复后的接口

echo "=========================================="
echo "测试修复后的接口"
echo "=========================================="

BASE_URL="http://localhost:8000"
SYMBOL="600519"

echo ""
echo "1. 测试实时行情接口"
echo "URL: $BASE_URL/api/cn/stock/$SYMBOL/realtime"
curl -s "$BASE_URL/api/cn/stock/$SYMBOL/realtime" | python3 -m json.tool

echo ""
echo ""
echo "2. 测试估值指标接口"
echo "URL: $BASE_URL/api/cn/stock/$SYMBOL/valuation"
curl -s "$BASE_URL/api/cn/stock/$SYMBOL/valuation" | python3 -m json.tool

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
