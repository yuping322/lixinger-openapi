# Findata Service

统一的金融数据服务 API，基于理杏仁数据源。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的理杏仁 Token
```

### 3. 启动服务

```bash
python server.py
```

服务将在 `http://localhost:8000` 启动。

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 中国市场

- `GET /api/cn/stock/{symbol}/basic` - 股票基础信息
- `GET /api/cn/stock/{symbol}/history` - 历史行情
- `GET /api/cn/stock/{symbol}/realtime` - 实时行情
- `GET /api/cn/stock/{symbol}/financial` - 财务数据
- `GET /api/cn/market/overview` - 市场概览
- `GET /api/cn/macro/lpr` - LPR利率
- `GET /api/cn/macro/cpi` - CPI数据

## 测试

```bash
# 测试股票历史数据
curl "http://localhost:8000/api/cn/stock/600519/history?start_date=2024-01-01&end_date=2024-12-31"

# 测试市场概览
curl "http://localhost:8000/api/cn/market/overview"
```

## 许可证

MIT License
