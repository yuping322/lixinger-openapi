# 理杏仁API综合文档

## 概述

本文档汇总了理杏仁开放平台的所有API端点。由于API文档需要登录后才能访问，以下内容基于URL结构和已获取的API信息整理而成。

## API分类结构

### 1. 大陆 (cn)

#### 1.1 公司接口 (company)

- **基础信息**
  - URL: `https://open.lixinger.com/api/cn/company/basic-info`
  - 类型: POST
  - 描述: 获取公司基础信息数据

- **公司概况**
  - URL: `https://open.lixinger.com/api/cn/company/profile`
  - 类型: POST
  - 描述: 获取公司概况数据

- **股本变动**
  - URL: `https://open.lixinger.com/api/cn/company/share-change`
  - 类型: POST
  - 描述: 获取公司股本变动数据

- **K线数据**
  - URL: `https://open.lixinger.com/api/cn/company/k-line`
  - 类型: POST
  - 描述: 获取公司K线数据

- **股东人数**
  - URL: `https://open.lixinger.com/api/cn/company/shareholders-count`
  - 类型: POST
  - 描述: 获取公司股东人数数据

- **高管增减持**
  - URL: `https://open.lixinger.com/api/cn/company/executive-shareholding`
  - 类型: POST
  - 描述: 获取高管增减持数据

- **大股东增减持**
  - URL: `https://open.lixinger.com/api/cn/company/major-shareholder-change`
  - 类型: POST
  - 描述: 获取大股东增减持数据

- **龙虎榜**
  - URL: `https://open.lixinger.com/api/cn/company/trading-abnormal`
  - 类型: POST
  - 描述: 获取龙虎榜数据

- **大宗交易**
  - URL: `https://open.lixinger.com/api/cn/company/block-trade`
  - 类型: POST
  - 描述: 获取大宗交易数据

- **股权质押**
  - URL: `https://open.lixinger.com/api/cn/company/equity-pledge`
  - 类型: POST
  - 描述: 获取股权质押数据

- **营收构成**
  - URL: `https://open.lixinger.com/api/cn/company/revenue-structure`
  - 类型: POST
  - 描述: 获取营收构成数据

- **经营数据**
  - URL: `https://open.lixinger.com/api/cn/company/operation-data`
  - 类型: POST
  - 描述: 获取经营数据

- **股票所属指数**
  - URL: `https://open.lixinger.com/api/cn/company/related-index`
  - 类型: POST
  - 描述: 获取股票所属指数数据

- **股票所属行业**
  - URL: `https://open.lixinger.com/api/cn/company/related-industry`
  - 类型: POST
  - 描述: 获取股票所属行业数据

- **公告**
  - URL: `https://open.lixinger.com/api/cn/company/announcement`
  - 类型: POST
  - 描述: 获取公告数据

- **监管信息**
  - URL: `https://open.lixinger.com/api/cn/company/regulatory-info`
  - 类型: POST
  - 描述: 获取监管信息数据

- **股东**
  - URL: `https://open.lixinger.com/api/cn/company/shareholders`
  - 类型: POST
  - 描述: 获取股东数据

- **分红送配**
  - URL: `https://open.lixinger.com/api/cn/company/dividend-allotment`
  - 类型: POST
  - 描述: 获取分红送配数据

- **客户及供应商**
  - URL: `https://open.lixinger.com/api/cn/company/client-supplier`
  - 类型: POST
  - 描述: 获取客户及供应商数据

- **基本面数据**
  - **非金融**:
    - URL: `https://open.lixinger.com/api/cn/company/fundamental/non_financial`
    - 类型: POST
    - 描述: 获取非金融公司基本面数据
    - [详细文档](./理杏仁_API_基本面数据.md)

  - **银行**:
    - URL: `https://open.lixinger.com/api/cn/company/fundamental/bank`
    - 类型: POST
    - 描述: 获取银行基本面数据

  - **证券**:
    - URL: `https://open.lixinger.com/api/cn/company/fundamental/securities`
    - 类型: POST
    - 描述: 获取证券公司基本面数据

  - **保险**:
    - URL: `https://open.lixinger.com/api/cn/company/fundamental/insurance`
    - 类型: POST
    - 描述: 获取保险公司基本面数据

  - **其他金融**:
    - URL: `https://open.lixinger.com/api/cn/company/fundamental/other_finance`
    - 类型: POST
    - 描述: 获取其他金融机构基本面数据

- **财务报表**
  - URL: `https://open.lixinger.com/api/cn/company/financial-statement`
  - 类型: POST
  - 描述: 获取财务报表数据

- **热度数据**
  - URL: `https://open.lixinger.com/api/cn/company/hot-data`
  - 类型: POST
  - 描述: 获取热度数据

- **资金流向**
  - URL: `https://open.lixinger.com/api/cn/company/fund-flow`
  - 类型: POST
  - 描述: 获取资金流向数据

#### 1.2 指数接口 (index)

- **指数基本信息**
  - URL: `https://open.lixinger.com/api/cn/index/basic-info`
  - 类型: POST
  - 描述: 获取指数基本信息数据

- **指数K线数据**
  - URL: `https://open.lixinger.com/api/cn/index/k-line`
  - 类型: POST
  - 描述: 获取指数K线数据

- **指数成分股**
  - URL: `https://open.lixinger.com/api/cn/index/constituents`
  - 类型: POST
  - 描述: 获取指数成分股数据

- **指数基本面数据**
  - URL: `https://open.lixinger.com/api/cn/index/fundamental`
  - 类型: POST
  - 描述: 获取指数基本面数据

- **指数财务数据**
  - URL: `https://open.lixinger.com/api/cn/index/financial`
  - 类型: POST
  - 描述: 获取指数财务数据

- **指数估值数据**
  - URL: `https://open.lixinger.com/api/cn/index/valuation`
  - 类型: POST
  - 描述: 获取指数估值数据

- **指数热度数据**
  - URL: `https://open.lixinger.com/api/cn/index/hot-data`
  - 类型: POST
  - 描述: 获取指数热度数据

- **指数资金流向**
  - URL: `https://open.lixinger.com/api/cn/index/fund-flow`
  - 类型: POST
  - 描述: 获取指数资金流向数据

#### 1.3 行业接口 (industry)

- **行业基本信息**
  - URL: `https://open.lixinger.com/api/cn/industry/basic-info`
  - 类型: POST
  - 描述: 获取行业基本信息数据

- **行业K线数据**
  - URL: `https://open.lixinger.com/api/cn/industry/k-line`
  - 类型: POST
  - 描述: 获取行业K线数据

- **行业成分股**
  - URL: `https://open.lixinger.com/api/cn/industry/constituents`
  - 类型: POST
  - 描述: 获取行业成分股数据

- **行业基本面数据**
  - URL: `https://open.lixinger.com/api/cn/industry/fundamental`
  - 类型: POST
  - 描述: 获取行业基本面数据

- **行业财务数据**
  - URL: `https://open.lixinger.com/api/cn/industry/financial`
  - 类型: POST
  - 描述: 获取行业财务数据

- **行业估值数据**
  - URL: `https://open.lixinger.com/api/cn/industry/valuation`
  - 类型: POST
  - 描述: 获取行业估值数据

- **行业热度数据**
  - URL: `https://open.lixinger.com/api/cn/industry/hot-data`
  - 类型: POST
  - 描述: 获取行业热度数据

- **行业资金流向**
  - URL: `https://open.lixinger.com/api/cn/industry/fund-flow`
  - 类型: POST
  - 描述: 获取行业资金流向数据

#### 1.4 基金接口 (fund)

- **基金基本信息**
  - URL: `https://open.lixinger.com/api/cn/fund/basic-info`
  - 类型: POST
  - 描述: 获取基金基本信息数据

- **基金K线数据**
  - URL: `https://open.lixinger.com/api/cn/fund/k-line`
  - 类型: POST
  - 描述: 获取基金K线数据

- **基金持仓**
  - URL: `https://open.lixinger.com/api/cn/fund/holdings`
  - 类型: POST
  - 描述: 获取基金持仓数据

- **基金净值**
  - URL: `https://open.lixinger.com/api/cn/fund/net-value`
  - 类型: POST
  - 描述: 获取基金净值数据

- **基金分红**
  - URL: `https://open.lixinger.com/api/cn/fund/dividend`
  - 类型: POST
  - 描述: 获取基金分红数据

- **基金评级**
  - URL: `https://open.lixinger.com/api/cn/fund/rating`
  - 类型: POST
  - 描述: 获取基金评级数据

- **基金热度数据**
  - URL: `https://open.lixinger.com/api/cn/fund/hot-data`
  - 类型: POST
  - 描述: 获取基金热度数据

### 2. 香港 (hk)

#### 2.1 公司接口 (company)

- **港股基本信息**
  - URL: `https://open.lixinger.com/api/hk/company/basic-info`
  - 类型: POST
  - 描述: 获取港股基本信息数据

- **港股K线数据**
  - URL: `https://open.lixinger.com/api/hk/company/k-line`
  - 类型: POST
  - 描述: 获取港股K线数据

- **港股基本面数据**
  - URL: `https://open.lixinger.com/api/hk/company/fundamental`
  - 类型: POST
  - 描述: 获取港股基本面数据

- **港股财务数据**
  - URL: `https://open.lixinger.com/api/hk/company/financial`
  - 类型: POST
  - 描述: 获取港股财务数据

- **港股股东**
  - URL: `https://open.lixinger.com/api/hk/company/shareholders`
  - 类型: POST
  - 描述: 获取港股股东数据

- **港股公告**
  - URL: `https://open.lixinger.com/api/hk/company/announcement`
  - 类型: POST
  - 描述: 获取港股公告数据

- **港股资金流向**
  - URL: `https://open.lixinger.com/api/hk/company/fund-flow`
  - 类型: POST
  - 描述: 获取港股资金流向数据

- **港股热度数据**
  - URL: `https://open.lixinger.com/api/hk/company/hot-data`
  - 类型: POST
  - 描述: 获取港股热度数据

#### 2.2 指数接口 (index)

- **港股指数基本信息**
  - URL: `https://open.lixinger.com/api/hk/index/basic-info`
  - 类型: POST
  - 描述: 获取港股指数基本信息数据

- **港股指数K线数据**
  - URL: `https://open.lixinger.com/api/hk/index/k-line`
  - 类型: POST
  - 描述: 获取港股指数K线数据

- **港股指数成分股**
  - URL: `https://open.lixinger.com/api/hk/index/constituents`
  - 类型: POST
  - 描述: 获取港股指数成分股数据

- **港股指数基本面数据**
  - URL: `https://open.lixinger.com/api/hk/index/fundamental`
  - 类型: POST
  - 描述: 获取港股指数基本面数据

- **港股指数财务数据**
  - URL: `https://open.lixinger.com/api/hk/index/financial`
  - 类型: POST
  - 描述: 获取港股指数财务数据

- **港股指数估值数据**
  - URL: `https://open.lixinger.com/api/hk/index/valuation`
  - 类型: POST
  - 描述: 获取港股指数估值数据

- **港股指数热度数据**
  - URL: `https://open.lixinger.com/api/hk/index/hot-data`
  - 类型: POST
  - 描述: 获取港股指数热度数据

- **港股指数资金流向**
  - URL: `https://open.lixinger.com/api/hk/index/fund-flow`
  - 类型: POST
  - 描述: 获取港股指数资金流向数据

#### 2.3 行业接口 (industry)

- **港股行业基本信息**
  - URL: `https://open.lixinger.com/api/hk/industry/basic-info`
  - 类型: POST
  - 描述: 获取港股行业基本信息数据

- **港股行业K线数据**
  - URL: `https://open.lixinger.com/api/hk/industry/k-line`
  - 类型: POST
  - 描述: 获取港股行业K线数据

- **港股行业成分股**
  - URL: `https://open.lixinger.com/api/hk/industry/constituents`
  - 类型: POST
  - 描述: 获取港股行业成分股数据

- **港股行业基本面数据**
  - URL: `https://open.lixinger.com/api/hk/industry/fundamental`
  - 类型: POST
  - 描述: 获取港股行业基本面数据

- **港股行业财务数据**
  - URL: `https://open.lixinger.com/api/hk/industry/financial`
  - 类型: POST
  - 描述: 获取港股行业财务数据

- **港股行业估值数据**
  - URL: `https://open.lixinger.com/api/hk/industry/valuation`
  - 类型: POST
  - 描述: 获取港股行业估值数据

- **港股行业热度数据**
  - URL: `https://open.lixinger.com/api/hk/industry/hot-data`
  - 类型: POST
  - 描述: 获取港股行业热度数据

- **港股行业资金流向**
  - URL: `https://open.lixinger.com/api/hk/industry/fund-flow`
  - 类型: POST
  - 描述: 获取港股行业资金流向数据

### 3. 美国 (us)

#### 3.1 指数接口 (index)

- **美股指数基本信息**
  - URL: `https://open.lixinger.com/api/us/index/basic-info`
  - 类型: POST
  - 描述: 获取美股指数基本信息数据

- **美股指数K线数据**
  - URL: `https://open.lixinger.com/api/us/index/k-line`
  - 类型: POST
  - 描述: 获取美股指数K线数据

- **美股指数成分股**
  - URL: `https://open.lixinger.com/api/us/index/constituents`
  - 类型: POST
  - 描述: 获取美股指数成分股数据

- **美股指数基本面数据**
  - URL: `https://open.lixinger.com/api/us/index/fundamental`
  - 类型: POST
  - 描述: 获取美股指数基本面数据

- **美股指数财务数据**
  - URL: `https://open.lixinger.com/api/us/index/financial`
  - 类型: POST
  - 描述: 获取美股指数财务数据

- **美股指数估值数据**
  - URL: `https://open.lixinger.com/api/us/index/valuation`
  - 类型: POST
  - 描述: 获取美股指数估值数据

- **美股指数热度数据**
  - URL: `https://open.lixinger.com/api/us/index/hot-data`
  - 类型: POST
  - 描述: 获取美股指数热度数据

- **美股指数资金流向**
  - URL: `https://open.lixinger.com/api/us/index/fund-flow`
  - 类型: POST
  - 描述: 获取美股指数资金流向数据

### 4. 宏观 (macro)

- **投资者**
  - URL: `https://open.lixinger.com/api/macro/investor`
  - 类型: POST
  - 描述: 获取投资者数据

- **信用证券账户**
  - URL: `https://open.lixinger.com/api/macro/credit-security-account`
  - 类型: POST
  - 描述: 获取信用证券账户数据

- **印花税**
  - URL: `https://open.lixinger.com/api/macro/stamp-duty`
  - 类型: POST
  - 描述: 获取印花税数据

- **价格指数**
  - URL: `https://open.lixinger.com/api/macro/price-index`
  - 类型: POST
  - 描述: 获取价格指数数据

- **存款准备金率**
  - URL: `https://open.lixinger.com/api/macro/reserve-requirement-ratio`
  - 类型: POST
  - 描述: 获取存款准备金率数据

- **货币供应**
  - URL: `https://open.lixinger.com/api/macro/money-supply`
  - 类型: POST
  - 描述: 获取货币供应数据

- **国债**
  - URL: `https://open.lixinger.com/api/macro/government-bond`
  - 类型: POST
  - 描述: 获取国债数据

- **利率**
  - URL: `https://open.lixinger.com/api/macro/interest-rate`
  - 类型: POST
  - 描述: 获取利率数据

- **社会融资**
  - URL: `https://open.lixinger.com/api/macro/social-financing`
  - 类型: POST
  - 描述: 获取社会融资数据

- **人民币存贷款**
  - URL: `https://open.lixinger.com/api/macro/rmb-deposit-loan`
  - 类型: POST
  - 描述: 获取人民币存贷款数据

- **央行资产负债表**
  - URL: `https://open.lixinger.com/api/macro/central-bank-balance-sheet`
  - 类型: POST
  - 描述: 获取央行资产负债表数据

- **官方储备资产**
  - URL: `https://open.lixinger.com/api/macro/official-reserve-assets`
  - 类型: POST
  - 描述: 获取官方储备资产数据

- **国外资产**
  - URL: `https://open.lixinger.com/api/macro/foreign-assets`
  - 类型: POST
  - 描述: 获取国外资产数据

- **国内各类债券**
  - URL: `https://open.lixinger.com/api/macro/domestic-bonds`
  - 类型: POST
  - 描述: 获取国内各类债券数据

- **杠杆率**
  - URL: `https://open.lixinger.com/api/macro/leverage-ratio`
  - 类型: POST
  - 描述: 获取杠杆率数据

- **人口**
  - URL: `https://open.lixinger.com/api/macro/population`
  - 类型: POST
  - 描述: 获取人口数据

- **GDP**
  - URL: `https://open.lixinger.com/api/macro/gdp`
  - 类型: POST
  - 描述: 获取GDP数据

- **失业率**
  - URL: `https://open.lixinger.com/api/macro/unemployment-rate`
  - 类型: POST
  - 描述: 获取失业率数据

- **对外贸易**
  - URL: `https://open.lixinger.com/api/macro/foreign-trade`
  - 类型: POST
  - 描述: 获取对外贸易数据

- **国际收支平衡**
  - URL: `https://open.lixinger.com/api/macro/balance-of-payments`
  - 类型: POST
  - 描述: 获取国际收支平衡数据

- **全社会固定资产投资**
  - URL: `https://open.lixinger.com/api/macro/fixed-asset-investment`
  - 类型: POST
  - 描述: 获取全社会固定资产投资数据

- **社会消费品零售**
  - URL: `https://open.lixinger.com/api/macro/social-consumer-retail`
  - 类型: POST
  - 描述: 获取社会消费品零售数据

- **交通运输**
  - URL: `https://open.lixinger.com/api/macro/transportation`
  - 类型: POST
  - 描述: 获取交通运输数据

- **房地产**
  - URL: `https://open.lixinger.com/api/macro/real-estate`
  - 类型: POST
  - 描述: 获取房地产数据

- **石油**
  - URL: `https://open.lixinger.com/api/macro/oil`
  - 类型: POST
  - 描述: 获取石油数据

- **能源**
  - URL: `https://open.lixinger.com/api/macro/energy`
  - 类型: POST
  - 描述: 获取能源数据

- **大宗商品**
  - URL: `https://open.lixinger.com/api/macro/commodities`
  - 类型: POST
  - 描述: 获取大宗商品数据

- **美元指数**
  - URL: `https://open.lixinger.com/api/macro/dollar-index`
  - 类型: POST
  - 描述: 获取美元指数数据

- **人民币指数**
  - URL: `https://open.lixinger.com/api/macro/rmb-index`
  - 类型: POST
  - 描述: 获取人民币指数数据

- **汇率**
  - URL: `https://open.lixinger.com/api/macro/exchange-rate`
  - 类型: POST
  - 描述: 获取汇率数据

- **工业**
  - URL: `https://open.lixinger.com/api/macro/industrial`
  - 类型: POST
  - 描述: 获取工业数据

## 通用API参数

大多数API遵循相似的参数结构：

- **token** (必需): 用户专属且唯一的API访问令牌
- **stockCodes** (必需): 股票代码数组，格式为["300750","600519","600157"]
- **date** (可选): 指定日期，格式为YYYY-MM-DD
- **startDate** (可选): 信息起始时间，格式为YYYY-MM-DD
- **endDate** (可选): 信息结束时间，格式为YYYY-MM-DD
- **metricsList** (必需): 指标数组，如['mc', 'pe_ttm', 'pb', 'dyr']

## 注意事项

1. 所有API都需要有效的token才能访问
2. 每个用户有API访问次数限制
3. 日期格式统一为YYYY-MM-DD
4. 股票代码需符合相应市场的格式要求
5. 部分API对请求频率有限制

## API访问限制

- 需要有效的账户和订阅
- 有每日访问次数限制
- 部分高级数据需要付费套餐

---
*文档生成时间: 2026-02-15*
*基于已知API结构和URL模式整理*