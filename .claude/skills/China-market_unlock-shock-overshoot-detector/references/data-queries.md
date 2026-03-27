# 数据获取指南：解禁冲击错杀机会

> 说明：本文件给出“应获取的数据类型与字段建议”。具体 suffix 以当前理杏仁 API 文档为准。

## 1) 限售解禁数据

目标字段建议：
- stockCode, stockName
- unlockDate
- unlockShares, unlockMarketValue
- floatShares, freeFloatMarketValue
- holderType / holderName

用途：
- 计算解禁压力（解禁股数/流通股本）
- 区分股东类型，识别潜在抛压来源

## 2) 大宗交易数据

目标字段建议：
- tradeDate
- blockDealAmount, blockDealVolume
- blockDealPrice, closePrice
- discountRate（可自行计算）
- buyerType, sellerType（若可得）

用途：
- 判断是否存在机构承接
- 观察折价率扩张或收敛

## 3) 股东减持数据

目标字段建议：
- announceDate, startDate, endDate
- holderName, holderRole
- plannedReductionShares
- actualReductionShares
- progressStatus

用途：
- 区分预期抛压（计划）与真实抛压（实施）
- 计算减持兑现率

## 4) 资金流与成交结构

目标字段建议：
- date
- mainNetInflow / institutionNetInflow
- northboundNetInflow（如适用）
- turnover, turnoverRate
- amplitude, volatility

用途：
- 验证承接能力是否改善
- 判断“放量下跌”还是“放量企稳”

## 5) 价格与基准数据

目标字段建议：
- open, high, low, close
- adjClose（前复权）
- benchmarkReturn（中证全指/行业指数）

用途：
- 估算超额回撤和相对修复

## 6) 最小可用数据集（MVP）

若数据受限，至少保证：
- 解禁日期与规模
- 减持计划与实施进度
- 价格序列（T-20~T+60）
- 资金净流方向（至少主力净流）

缺少大宗交易时，可用“成交额+换手率+价格弹性”替代承接判断。
