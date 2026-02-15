# 理杏仁股票信息API文档

## 股票信息API

**简要描述:** 获取股票详细信息。

**请求URL:** 
```
https://open.lixinger.com/api/cn/company
```

**请求方式:** POST

## 参数说明

| 参数名称 | 必选 | 数据类型 | 说明 |
|----------|------|----------|------|
| token | Yes | String | 我的Token页有用户专属且唯一的Token。[我的Token](/open/api/token)页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 股票代码数组。默认值为所有股票代码。格式如下：["300750","600519","600157"]。请参考[股票信息API](/open/api/detail?api-key=cn/company)获取合法的stockCode。 |
| fsTableType | No | String | 财报类型，比如，'bank'。<br>当前支持:<br>非金融: non_financial<br>银行: bank<br>保险: insurance<br>证券: security<br>其他金融: other_financial |
| mutualMarkets | No | Array | 互联互通类型，比如：'[ha]'。<br>当前支持: 陆股通: ha |
| includeDelisted | No | Boolean | 是否包含退市股。默认值是false。 |
| pageIndex | Yes | Number | 页面索引。默认值是0。 |

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
|----------|----------|------|
| total | Number | 公司总数 |
| name | String | 公司名称 |
| stockCode | String | 股票代码 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
| fsTableType | String | 财报类型 |
| mutualMarkets | String | 互联互通 |
| mutualMarketFlag | Boolean | 是否是互联互通标的 |
| marginTradingAndSecuritiesLendingFlag | Boolean | 是否是融资融券标的 |
| ipoDate | Date | 上市时间 |
| delistedDate | Date | 退市时间 |

## API试用
- 剩余访问次数: 987
- 示例请求:
```json
{
  "token": "ffad9101-8689-4b5d-bd79-763c58522a95",
  "pageIndex": 0
}
```

---
*文档生成时间: 2026-02-15*
*API页面: https://www.lixinger.com/open/api/doc?api-key=cn/company*