# 理杏仁API限制说明

## 测试结果总结

**测试时间**: 2026-02-21  
**测试股票**: 600519 (贵州茅台)  
**Token**: 免费版

---

## ✅ 可用接口（5个）

### 1. 公司基本信息
- **接口**: `cn/company`
- **状态**: ✅ 可用
- **数据**: 完整

### 2. 公司概况
- **接口**: `cn/company/profile`
- **状态**: ✅ 可用
- **数据**: 完整（包含大量历史数据）

### 3. K线数据
- **接口**: `cn/company/candlestick`
- **状态**: ✅ 可用
- **数据**: 完整

### 4. 股东人数
- **接口**: `cn/company/shareholders-num`
- **状态**: ✅ 可用
- **数据**: 季度数据

### 5. 公告
- **接口**: `cn/company/announcement`
- **状态**: ✅ 可用
- **数据**: 完整

---

## ❌ 不可用接口（14个）

以下接口在免费版Token下不可用（返回码0）：

### 股东相关（3个）
1. **股东信息** - `cn/company/shareholders`
2. **高管增减持** - `cn/company/executive-shareholding`
3. **大股东增减持** - `cn/company/major-shareholder-change`

### 特殊数据（3个）
4. **龙虎榜** - `cn/company/trading-abnormal`
5. **大宗交易** - `cn/company/block-trade`
6. **股权质押** - `cn/company/equity-pledge`

### 财务相关（3个）
7. **分红送配** - `cn/company/dividend-allotment`
8. **营收构成** - `cn/company/revenue-structure`
9. **经营数据** - `cn/company/operation-data`

### 关系数据（2个）
10. **所属行业** - `cn/company/related-industry`
11. **所属指数** - `cn/company/related-index`

### 其他（3个）
12. **热度数据** - `cn/company/hot-data`
13. **资金流向** - `cn/company/fund-flow`
14. **股本变动** - `cn/company/share-change`

---

## 💡 解决方案

### 方案1: 升级理杏仁订阅
- 访问 https://www.lixinger.com/open/api
- 查看付费套餐，可能包含更多数据接口

### 方案2: 使用替代数据源
对于不可用的接口，可以考虑：
- **AKShare**: 免费的Python金融数据接口
- **TuShare**: 需要积分的金融数据平台
- **东方财富/同花顺**: 爬虫获取（需注意合规性）

### 方案3: 返回友好提示
在findata-service中，对不可用的接口返回明确的提示信息，告知用户数据限制。

---

## 📊 可用性统计

| 类别 | 总数 | 可用 | 不可用 | 可用率 |
|------|------|------|--------|--------|
| 全部接口 | 19 | 5 | 14 | 26.3% |

---

## 🔄 建议的API设计

### 对于可用接口
- 正常返回数据
- 提供完整的功能

### 对于不可用接口
返回格式：
```json
{
  "code": 0,
  "message": "此接口在当前理杏仁订阅下不可用",
  "data": [],
  "meta": {
    "source": "lixinger",
    "limitation": "free_tier",
    "alternatives": [
      "升级理杏仁订阅",
      "使用AKShare等替代数据源"
    ]
  },
  "warnings": ["该数据类型需要付费订阅或理杏仁不提供"],
  "errors": []
}
```

---

## 📝 更新建议

1. **更新API文档**: 明确标注哪些接口可用
2. **更新测试**: 只测试可用的接口
3. **友好提示**: 对不可用接口返回清晰的说明
4. **替代方案**: 考虑集成其他免费数据源

---

**结论**: 理杏仁免费版API功能有限，建议：
1. 使用可用的5个接口
2. 对不可用接口提供清晰说明
3. 考虑集成其他数据源补充
