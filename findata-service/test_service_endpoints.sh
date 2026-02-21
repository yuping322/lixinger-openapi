#!/bin/bash
# 测试findata-service的所有可用接口

echo "=========================================="
echo "Findata Service 接口测试"
echo "测试股票: 600519 (贵州茅台)"
echo "=========================================="

BASE_URL="http://localhost:8000"

echo ""
echo "1. 测试公司基本信息"
curl -s "$BASE_URL/api/cn/stock/600519/basic" | python3 -m json.tool | head -20

echo ""
echo "2. 测试公司概况"
curl -s "$BASE_URL/api/cn/stock/600519/profile" | python3 -m json.tool | head -20

echo ""
echo "3. 测试K线数据"
curl -s "$BASE_URL/api/cn/stock/600519/history?start_date=2026-01-01&end_date=2026-02-21" | python3 -m json.tool | head -30

echo ""
echo "4. 测试股东人数"
curl -s "$BASE_URL/api/cn/shareholder/600519/count" | python3 -m json.tool | head -30

echo ""
echo "5. 测试分红送配"
curl -s "$BASE_URL/api/cn/dividend/600519" | python3 -m json.tool | head -30

echo ""
echo "6. 测试股本变动"
curl -s "$BASE_URL/api/cn/shareholder/600519/equity-change" | python3 -m json.tool | head -30

echo ""
echo "7. 测试公告"
curl -s "$BASE_URL/api/cn/stock/600519/announcement" | python3 -m json.tool | head -30

echo ""
echo "8. 测试龙虎榜 (可能无数据)"
curl -s "$BASE_URL/api/cn/special/dragon-tiger/600519" | python3 -m json.tool | head -20

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
