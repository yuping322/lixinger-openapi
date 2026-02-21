# Findata Service 快速启动指南

## 项目结构

```
findata-service/
├── server.py              # FastAPI 服务入口
├── client.py              # 示例客户端
├── test_api.py            # API 测试脚本
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
├── config/
│   ├── __init__.py
│   └── settings.py       # 配置管理
├── models/
│   ├── __init__.py
│   └── responses.py      # 响应模型
├── providers/
│   ├── __init__.py
│   └── lixinger.py       # 理杏仁数据源
└── routes/
    └── cn/
        ├── __init__.py
        ├── stock.py      # 股票接口
        ├── market.py     # 市场接口
        └── macro.py      # 宏观接口
```

## 快速启动

### 1. 配置环境变量

```bash
cd findata-service
cp .env.example .env
# 编辑 .env 文件，填入理杏仁 Token
```

### 2. 安装依赖

```bash
# 创建虚拟环境（可选）
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 启动服务

```bash
# 方式一：直接运行
python server.py

# 方式二：使用 uvicorn（推荐开发环境）
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口列表

### 股票接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/cn/stock/{symbol}/basic` | GET | 股票基础信息 |
| `/api/cn/stock/{symbol}/history` | GET | 历史行情 |
| `/api/cn/stock/{symbol}/realtime` | GET | 实时行情 |
| `/api/cn/stock/{symbol}/financial` | GET | 财务数据 |
| `/api/cn/stock/{symbol}/valuation` | GET | 估值指标 |

### 市场接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/cn/market/overview` | GET | 市场概览 |

### 宏观接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/cn/macro/lpr` | GET | LPR利率 |
| `/api/cn/macro/cpi` | GET | CPI数据 |
| `/api/cn/macro/ppi` | GET | PPI数据 |
| `/api/cn/macro/pmi` | GET | PMI数据 |
| `/api/cn/macro/m2` | GET | M2货币供应 |

## 测试接口

### 方式一：使用测试脚本

```bash
# 确保服务已启动
python test_api.py
```

### 方式二：使用客户端

```bash
python client.py
```

### 方式三：使用 curl

```bash
# 测试股票基础信息
curl "http://localhost:8000/api/cn/stock/600519/basic"

# 测试历史行情
curl "http://localhost:8000/api/cn/stock/600519/history?start_date=2024-01-01&end_date=2024-01-31"

# 测试市场概览
curl "http://localhost:8000/api/cn/market/overview"

# 测试LPR数据
curl "http://localhost:8000/api/cn/macro/lpr"
```

## 使用示例

### Python 客户端

```python
from client import FindataClient

# 初始化客户端
client = FindataClient(base_url="http://localhost:8000")

# 获取股票基础信息
result = client.get_stock_basic("600519")
print(result)

# 获取历史行情
result = client.get_stock_history(
    symbol="600519",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
print(result)

# 获取市场概览
result = client.get_market_overview()
print(result)
```

### 响应格式

所有接口返回统一格式：

```json
{
  "code": 1,
  "message": "success",
  "data": [...],
  "meta": {
    "source": "lixinger",
    "cached": true,
    "timestamp": "2026-02-19T10:30:00Z",
    "count": 100
  },
  "warnings": [],
  "errors": []
}
```

## 已实现功能

- ✅ 股票基础信息查询
- ✅ 股票历史行情（支持日/周/月线）
- ✅ 股票实时行情
- ✅ 财务数据（资产负债表/利润表/现金流量表）
- ✅ 估值指标（PE/PB/PS/PCF）
- ✅ 市场概览（主要指数）
- ✅ 宏观数据（LPR/CPI/PPI/PMI/M2）
- ✅ 智能缓存（实时数据1小时，日线数据24小时，财务数据7天）
- ✅ 统一响应格式
- ✅ 自动 API 文档生成

## 下一步计划

- [ ] 添加资金流向接口
- [ ] 添加龙虎榜接口
- [ ] 添加大宗交易接口
- [ ] 添加北向资金接口
- [ ] 支持 US/HK 市场
- [ ] 添加数据库持久化
- [ ] 添加认证和权限控制
- [ ] 性能优化和监控

## 常见问题

### 1. 启动失败：LIXINGER_TOKEN is required

**解决**：确保 .env 文件中已配置 LIXINGER_TOKEN

### 2. 接口返回 404

**解决**：检查服务是否启动，端口是否正确

### 3. 数据返回为空

**解决**：
- 检查理杏仁 Token 是否有效
- 检查股票代码是否正确
- 查看服务日志了解详细错误

## 技术支持

- 设计文档：`/docs/FINDATA_SERVICE_DESIGN.md`
- API 文档：http://localhost:8000/docs
- 问题反馈：创建 GitHub Issue
