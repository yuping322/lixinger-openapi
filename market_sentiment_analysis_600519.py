#!/usr/bin/env python3
"""
市场热度排名与情绪监控 - 贵州茅台(600519)
使用可用数据进行情绪分析的替代方案
"""

from lixinger_openapi.query import query_json
from lixinger_openapi.token import set_token
from datetime import datetime, timedelta
import json

# 设置token
set_token('ffad9101-8689-4b5d-bd79-763c58522a95', write_token=False)

def get_kline_data(stock_code, days=90):
    """获取K线数据用于成交量和价格分析"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    result = query_json("cn/company/candlestick", {
        "stockCode": stock_code,
        "type": "ex_rights",
        "startDate": start_date,
        "endDate": end_date
    })
    return result

def get_shareholder_count(stock_code):
    """获取股东人数变化（筹码集中度指标）"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    result = query_json("cn/company/shareholders-num", {
        "stockCode": stock_code,
        "startDate": start_date,
        "endDate": end_date
    })
    return result

def get_announcements(stock_code, limit=20):
    """获取公告数据（关注度代理指标）"""
    result = query_json("cn/company/announcement", {
        "stockCode": stock_code,
        "limit": limit
    })
    return result

def analyze_volume_sentiment(kline_data):
    """分析成交量情绪"""
    if kline_data.get('code') != 1:
        return None
    
    data = kline_data.get('data', [])
    if len(data) < 20:
        return None
    
    # 最近5天平均成交量
    recent_5d = data[-5:]
    recent_vol = sum(d.get('volume', 0) for d in recent_5d) / 5
    
    # 最近20天平均成交量
    recent_20d = data[-20:]
    avg_vol_20d = sum(d.get('volume', 0) for d in recent_20d) / 20
    
    # 最近60天平均成交量
    avg_vol_60d = sum(d.get('volume', 0) for d in data) / len(data)
    
    # 计算成交量变化率
    vol_change_5d_vs_20d = (recent_vol / avg_vol_20d - 1) * 100 if avg_vol_20d > 0 else 0
    vol_change_20d_vs_60d = (avg_vol_20d / avg_vol_60d - 1) * 100 if avg_vol_60d > 0 else 0
    
    # 计算价格波动率（情绪强度指标）
    recent_prices = [d.get('close', 0) for d in recent_20d]
    price_volatility = (max(recent_prices) / min(recent_prices) - 1) * 100 if min(recent_prices) > 0 else 0
    
    return {
        'recent_5d_avg_volume': recent_vol,
        'recent_20d_avg_volume': avg_vol_20d,
        'recent_60d_avg_volume': avg_vol_60d,
        'vol_change_5d_vs_20d': vol_change_5d_vs_20d,
        'vol_change_20d_vs_60d': vol_change_20d_vs_60d,
        'price_volatility_20d': price_volatility,
        'latest_close': data[-1].get('close', 0),
        'latest_volume': data[-1].get('volume', 0),
        'latest_date': data[-1].get('date', '')
    }

def analyze_shareholder_sentiment(shareholder_data):
    """分析股东人数变化（筹码集中度）"""
    if shareholder_data.get('code') != 1:
        return None
    
    data = shareholder_data.get('data', [])
    if len(data) < 2:
        return None
    
    # 最新数据
    latest = data[-1]
    previous = data[-2] if len(data) > 1 else None
    
    return {
        'latest_date': latest.get('date', ''),
        'shareholder_count': latest.get('num', 0),
        'change_rate': latest.get('shareholdersNumberChangeRate', 0) * 100,
        'previous_count': previous.get('num', 0) if previous else 0,
        'trend': '增加' if latest.get('shareholdersNumberChangeRate', 0) > 0 else '减少'
    }

def analyze_announcement_frequency(announcement_data):
    """分析公告频率（关注度代理）"""
    if announcement_data.get('code') != 1:
        return None
    
    data = announcement_data.get('data', [])
    if not data:
        return None
    
    # 统计最近30天的公告数量
    now = datetime.now()
    recent_30d = [a for a in data if (now - datetime.fromisoformat(a.get('date', '').replace('+08:00', ''))).days <= 30]
    
    # 按类型分类
    announcement_types = {}
    for ann in recent_30d:
        types = ann.get('types', [])
        for t in types:
            announcement_types[t] = announcement_types.get(t, 0) + 1
    
    return {
        'total_announcements': len(data),
        'recent_30d_count': len(recent_30d),
        'announcement_types': announcement_types,
        'latest_announcement': data[0] if data else None
    }

def generate_sentiment_score(volume_analysis, shareholder_analysis, announcement_analysis):
    """综合情绪评分（0-100）"""
    score = 50  # 基准分
    
    if volume_analysis:
        # 成交量活跃度 (+/- 20分)
        if volume_analysis['vol_change_5d_vs_20d'] > 20:
            score += 15
        elif volume_analysis['vol_change_5d_vs_20d'] > 0:
            score += 5
        elif volume_analysis['vol_change_5d_vs_20d'] < -20:
            score -= 15
        else:
            score -= 5
        
        # 波动率（情绪强度）(+/- 10分)
        if volume_analysis['price_volatility_20d'] > 15:
            score += 10  # 高波动=高关注
        elif volume_analysis['price_volatility_20d'] < 5:
            score -= 10  # 低波动=低关注
    
    if shareholder_analysis:
        # 股东人数变化 (+/- 15分)
        change_rate = shareholder_analysis['change_rate']
        if change_rate > 10:
            score -= 10  # 股东增加=筹码分散=散户进入
        elif change_rate > 5:
            score -= 5
        elif change_rate < -10:
            score += 10  # 股东减少=筹码集中=机构吸筹
        elif change_rate < -5:
            score += 5
    
    if announcement_analysis:
        # 公告频率 (+/- 5分)
        if announcement_analysis['recent_30d_count'] > 5:
            score += 5  # 公告频繁=关注度高
    
    return max(0, min(100, score))

def main():
    stock_code = "600519"
    print(f"=" * 80)
    print(f"市场热度排名与情绪监控 - 贵州茅台({stock_code})")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=" * 80)
    print()
    
    # 数据可用性说明
    print("📊 数据可用性说明")
    print("-" * 80)
    print("⚠️  理杏仁免费版不提供以下数据:")
    print("   - 热度数据 (hot-data): API不可用")
    print("   - 资金流向 (fund-flow): API不可用")
    print()
    print("✅ 使用替代指标进行情绪分析:")
    print("   - 成交量变化 → 市场活跃度")
    print("   - 股东人数变化 → 筹码集中度")
    print("   - 公告频率 → 关注度代理")
    print("   - 价格波动率 → 情绪强度")
    print()
    
    # 获取数据
    print("🔍 正在获取数据...")
    kline_data = get_kline_data(stock_code)
    shareholder_data = get_shareholder_count(stock_code)
    announcement_data = get_announcements(stock_code)
    
    # 分析
    volume_analysis = analyze_volume_sentiment(kline_data)
    shareholder_analysis = analyze_shareholder_sentiment(shareholder_data)
    announcement_analysis = analyze_announcement_frequency(announcement_data)
    
    # 输出分析结果
    print()
    print("=" * 80)
    print("📈 成交量情绪分析")
    print("=" * 80)
    if volume_analysis:
        print(f"最新日期: {volume_analysis['latest_date']}")
        print(f"最新收盘价: ¥{volume_analysis['latest_close']:.2f}")
        print(f"最新成交量: {volume_analysis['latest_volume']:,.0f} 股")
        print()
        print(f"近5日平均成交量:  {volume_analysis['recent_5d_avg_volume']:,.0f} 股")
        print(f"近20日平均成交量: {volume_analysis['recent_20d_avg_volume']:,.0f} 股")
        print(f"近60日平均成交量: {volume_analysis['recent_60d_avg_volume']:,.0f} 股")
        print()
        print(f"成交量变化 (5日 vs 20日): {volume_analysis['vol_change_5d_vs_20d']:+.2f}%")
        print(f"成交量变化 (20日 vs 60日): {volume_analysis['vol_change_20d_vs_60d']:+.2f}%")
        print(f"近20日价格波动率: {volume_analysis['price_volatility_20d']:.2f}%")
        print()
        
        # 情绪判断
        if volume_analysis['vol_change_5d_vs_20d'] > 20:
            print("💡 情绪判断: 🔥 成交活跃度显著上升，市场关注度提高")
        elif volume_analysis['vol_change_5d_vs_20d'] > 0:
            print("💡 情绪判断: ↗️  成交活跃度温和上升")
        elif volume_analysis['vol_change_5d_vs_20d'] < -20:
            print("💡 情绪判断: ❄️  成交活跃度显著下降，市场关注度降低")
        else:
            print("💡 情绪判断: ↘️  成交活跃度温和下降")
    else:
        print("❌ 无法获取成交量数据")
    
    print()
    print("=" * 80)
    print("👥 股东结构情绪分析")
    print("=" * 80)
    if shareholder_analysis:
        print(f"最新日期: {shareholder_analysis['latest_date']}")
        print(f"股东人数: {shareholder_analysis['shareholder_count']:,} 户")
        print(f"变化率: {shareholder_analysis['change_rate']:+.2f}%")
        print(f"趋势: {shareholder_analysis['trend']}")
        print()
        
        # 筹码集中度判断
        if shareholder_analysis['change_rate'] > 10:
            print("💡 筹码判断: 📈 股东人数大幅增加，筹码分散，散户进入")
            print("   ⚠️  风险提示: 散户追高可能是顶部信号")
        elif shareholder_analysis['change_rate'] > 5:
            print("💡 筹码判断: ↗️  股东人数温和增加，筹码略有分散")
        elif shareholder_analysis['change_rate'] < -10:
            print("💡 筹码判断: 📉 股东人数大幅减少，筹码集中，可能机构吸筹")
            print("   ✅ 积极信号: 筹码集中通常是积极信号")
        elif shareholder_analysis['change_rate'] < -5:
            print("💡 筹码判断: ↘️  股东人数温和减少，筹码略有集中")
        else:
            print("💡 筹码判断: ➡️  股东人数基本稳定")
    else:
        print("❌ 无法获取股东人数数据")
    
    print()
    print("=" * 80)
    print("📢 公告频率分析（关注度代理）")
    print("=" * 80)
    if announcement_analysis:
        print(f"总公告数: {announcement_analysis['total_announcements']} 条")
        print(f"近30天公告数: {announcement_analysis['recent_30d_count']} 条")
        print()
        
        if announcement_analysis['announcement_types']:
            print("公告类型分布:")
            for ann_type, count in sorted(announcement_analysis['announcement_types'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"  - {ann_type}: {count} 条")
        print()
        
        if announcement_analysis['latest_announcement']:
            latest = announcement_analysis['latest_announcement']
            print(f"最新公告:")
            print(f"  日期: {latest.get('date', '')}")
            print(f"  标题: {latest.get('linkText', '')}")
            print(f"  类型: {', '.join(latest.get('types', []))}")
        print()
        
        # 关注度判断
        if announcement_analysis['recent_30d_count'] > 5:
            print("💡 关注度判断: 📣 公告频繁，公司动作较多，市场关注度较高")
        elif announcement_analysis['recent_30d_count'] > 2:
            print("💡 关注度判断: ➡️  公告频率正常")
        else:
            print("💡 关注度判断: 🔇 公告较少，市场关注度一般")
    else:
        print("❌ 无法获取公告数据")
    
    # 综合情绪评分
    print()
    print("=" * 80)
    print("🎯 综合情绪评分")
    print("=" * 80)
    sentiment_score = generate_sentiment_score(volume_analysis, shareholder_analysis, announcement_analysis)
    print(f"情绪评分: {sentiment_score}/100")
    print()
    
    if sentiment_score >= 70:
        print("📊 情绪状态: 🔥 热度高涨")
        print("   市场关注度高，交易活跃，情绪偏乐观")
    elif sentiment_score >= 55:
        print("📊 情绪状态: ↗️  温和积极")
        print("   市场关注度正常，情绪略偏积极")
    elif sentiment_score >= 45:
        print("📊 情绪状态: ➡️  中性平稳")
        print("   市场关注度一般，情绪中性")
    elif sentiment_score >= 30:
        print("📊 情绪状态: ↘️  温和消极")
        print("   市场关注度下降，情绪略偏消极")
    else:
        print("📊 情绪状态: ❄️  冷淡低迷")
        print("   市场关注度低，交易清淡，情绪偏悲观")
    
    # 交叉验证与矛盾分析
    print()
    print("=" * 80)
    print("🔍 交叉验证与矛盾分析")
    print("=" * 80)
    
    if volume_analysis and shareholder_analysis:
        vol_trend = "上升" if volume_analysis['vol_change_5d_vs_20d'] > 0 else "下降"
        shareholder_trend = shareholder_analysis['trend']
        
        print(f"成交量趋势: {vol_trend}")
        print(f"股东人数趋势: {shareholder_trend}")
        print()
        
        # 矛盾分析
        if vol_trend == "下降" and shareholder_trend == "增加":
            print("⚠️  发现矛盾: 成交量下降但股东人数增加")
            print("   可能解释:")
            print("   1. 散户小额买入，但大户/机构减仓")
            print("   2. 市场分歧加大，换手率下降")
            print("   3. 需要关注后续资金流向验证")
        elif vol_trend == "上升" and shareholder_trend == "减少":
            print("✅ 积极信号: 成交量上升且股东人数减少")
            print("   可能解释:")
            print("   1. 机构/大户吸筹，筹码集中")
            print("   2. 散户离场，主力进场")
            print("   3. 通常是积极信号，但需关注价格走势")
        elif vol_trend == "上升" and shareholder_trend == "增加":
            print("⚠️  警惕信号: 成交量上升且股东人数增加")
            print("   可能解释:")
            print("   1. 散户追高，可能是顶部信号")
            print("   2. 市场情绪过热")
            print("   3. 建议谨慎，关注是否出现放量滞涨")
        else:
            print("➡️  趋势一致: 成交量和股东人数同步下降")
            print("   可能解释:")
            print("   1. 市场关注度整体下降")
            print("   2. 进入盘整期")
            print("   3. 等待新的催化剂")
    
    # 建议与监控要点
    print()
    print("=" * 80)
    print("💡 建议与监控要点")
    print("=" * 80)
    print()
    print("1. 数据限制应对:")
    print("   - 理杏仁免费版不提供热度和资金流向数据")
    print("   - 建议使用AKShare等开源工具补充数据")
    print("   - 或考虑升级理杏仁订阅获取完整数据")
    print()
    print("2. 持续监控指标:")
    print("   - 成交量变化趋势（每日）")
    print("   - 股东人数变化（每季度）")
    print("   - 公告频率与类型（实时）")
    print("   - 价格波动率（每周）")
    print()
    print("3. 风险提示:")
    print("   - 情绪指标仅供参考，不构成投资建议")
    print("   - 需结合基本面、技术面综合判断")
    print("   - 注意A股T+1、涨跌停等交易限制")
    print()
    print("4. 下一步行动:")
    print("   - 如需完整热度数据，建议集成AKShare")
    print("   - 可使用 $fund-flow-monitor 技能获取资金流向")
    print("   - 可使用 $dragon-tiger-list-analyzer 分析龙虎榜")
    print()
    
    print("=" * 80)
    print("分析完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
