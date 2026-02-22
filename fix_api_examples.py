#!/usr/bin/env python3
"""
批量修正 API 文档中的调用示例
"""
import os
import re
from pathlib import Path

# 定义正确的示例参数
EXAMPLES = {
    # CN - Company APIs
    'cn/company/basic-info': '{"stockCodes": ["600519"]}',
    'cn/company/announcement': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/block-trade': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/client-supplier': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/dividend-allotment': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/equity-pledge': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/executive-shareholding': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/financial-statement': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/fund-flow': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/fundamental-non-financial': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/fundamental-other-finance': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/hot-data': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/k-line': '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/major-shareholder-change': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/operation-data': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/profile': '{"stockCodes": ["600519"]}',
    'cn/company/regulatory-info': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/related-index': '{"stockCodes": ["600519"]}',
    'cn/company/related-industry': '{"stockCodes": ["600519"]}',
    'cn/company/revenue-structure': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/share-change': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/company/shareholders-count': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/shareholders': '{"stockCodes": ["600519"], "date": "2024-12-31"}',
    'cn/company/trading-abnormal': '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    
    # CN - Fund APIs
    'cn/fund/basic-info': '{"stockCodes": ["501018"]}',
    'cn/fund/dividend': '{"stockCodes": ["501018"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/fund/holdings': '{"stockCodes": ["501018"], "date": "2024-12-31"}',
    'cn/fund/hot-data': '{"stockCodes": ["501018"], "date": "2024-12-31"}',
    'cn/fund/k-line': '{"stockCode": "501018", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/fund/net-value': '{"stockCodes": ["501018"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/fund/rating': '{"stockCodes": ["501018"], "date": "2024-12-31"}',
    
    # CN - Index APIs
    'cn/index/basic-info': '{"stockCodes": ["000300"]}',
    'cn/index/constituents': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    'cn/index/financial': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    'cn/index/fund-flow': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    'cn/index/fundamental': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    'cn/index/hot-data': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    'cn/index/k-line': '{"stockCode": "000300", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/index/valuation': '{"stockCodes": ["000300"], "date": "2024-12-31"}',
    
    # CN - Industry APIs
    'cn/industry/basic-info': '{"stockCodes": ["801780"]}',
    'cn/industry/constituents': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    'cn/industry/financial': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    'cn/industry/fund-flow': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    'cn/industry/fundamental': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    'cn/industry/hot-data': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    'cn/industry/k-line': '{"stockCode": "801780", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'cn/industry/valuation': '{"stockCodes": ["801780"], "date": "2024-12-31"}',
    
    # HK - Company APIs
    'hk/company/announcement': '{"stockCodes": ["00700"], "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'hk/company/basic-info': '{"stockCodes": ["00700"]}',
    'hk/company/financial-statement': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/company/fundamental': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/company/hot-data': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/company/k-line': '{"stockCode": "00700", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'hk/company/profile': '{"stockCodes": ["00700"]}',
    
    # HK - Index APIs
    'hk/index/basic-info': '{"stockCodes": ["HSI"]}',
    'hk/index/constituents': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/index/fundamental': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/index/hot-data': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/index/k-line': '{"stockCode": "HSI", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    
    # US - Company APIs
    'us/company/basic-info': '{"stockCodes": ["AAPL"]}',
    'us/company/financial-statement': '{"stockCodes": ["AAPL"], "date": "2024-12-31"}',
    'us/company/fundamental': '{"stockCodes": ["AAPL"], "date": "2024-12-31"}',
    'us/company/hot-data': '{"stockCodes": ["AAPL"], "date": "2024-12-31"}',
    'us/company/k-line': '{"stockCode": "AAPL", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'us/company/profile': '{"stockCodes": ["AAPL"]}',
    
    # US - Index APIs
    'us/index/basic-info': '{"stockCodes": ["SPX"]}',
    'us/index/constituents': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/fundamental': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/hot-data': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/k-line': '{"stockCode": "SPX", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    
    # Macro APIs - 宏观数据不需要 stockCodes
    'macro/balance-of-payments': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/central-bank-balance-sheet': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/commodities': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/credit-security-account': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/dollar-index': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/domestic-bonds': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/energy': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/exchange-rate': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/fixed-asset-investment': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/foreign-assets': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/foreign-trade': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/gdp': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/government-bond': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/industrial': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/industrial-production': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/interest-rate': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/investor': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/leverage-ratio': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/money-supply': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/official-reserve-assets': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/oil': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/pmi': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/population': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/price-index': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/real-estate': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/reserve-requirement-ratio': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/retail-sales': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/rmb-deposit-loan': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/rmb-index': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/social-consumer-retail': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/social-financing': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/stamp-duty': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/transportation': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'macro/unemployment-rate': '{"startDate": "2024-01-01", "endDate": "2024-12-31"}',
    
    # HK 补充
    'hk/company/financial-statement': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/company/fund-flow': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/company/shareholders': '{"stockCodes": ["00700"], "date": "2024-12-31"}',
    'hk/index/financial': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/index/fund-flow': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/index/valuation': '{"stockCodes": ["HSI"], "date": "2024-12-31"}',
    'hk/industry/basic-info': '{"stockCodes": ["HK_IND_001"]}',
    'hk/industry/constituents': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    'hk/industry/financial': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    'hk/industry/fund-flow': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    'hk/industry/fundamental': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    'hk/industry/hot-data': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    'hk/industry/k-line': '{"stockCode": "HK_IND_001", "startDate": "2024-01-01", "endDate": "2024-12-31"}',
    'hk/industry/valuation': '{"stockCodes": ["HK_IND_001"], "date": "2024-12-31"}',
    
    # US 补充
    'us/index/drawdown': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/financial': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/fund-flow': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/hot-cp': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/hot-ifet-sni': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/tracking-fund': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
    'us/index/valuation': '{"stockCodes": ["SPX"], "date": "2024-12-31"}',
}

def fix_file(file_path: Path):
    """修正单个文件的调用示例"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从文件路径提取 API suffix
    # 例如: skills/lixinger-data-query/resources/apis/cn/cn_company_basic_info.md
    # 提取: cn/company/basic-info
    parts = file_path.stem.split('_')  # ['cn', 'company', 'basic', 'info']
    
    # 特殊处理一些文件
    if file_path.stem in ['company', 'index_fundamental']:
        print(f"⏭️  跳过特殊文件: {file_path.name}")
        return False
    
    if len(parts) >= 2:
        # 重构 suffix - 将所有下划线替换为连字符，然后按规则分段
        # cn_company_basic_info -> cn/company/basic-info
        # macro_dollar_index -> macro/dollar-index
        market = parts[0]  # cn, hk, us, macro
        
        # 对于宏观数据，可能是 macro_xxx_yyy 格式
        if market == 'macro' and len(parts) >= 2:
            # macro_dollar_index -> macro/dollar-index
            suffix = market + '/' + '-'.join(parts[1:])
        else:
            # cn_company_basic_info -> cn/company/basic-info
            category = parts[1] if len(parts) > 1 else ''
            detail = '-'.join(parts[2:]) if len(parts) > 2 else ''
            suffix = f"{market}/{category}/{detail}" if detail else f"{market}/{category}"
        
        # 获取正确的参数
        params = EXAMPLES.get(suffix)
        if not params:
            print(f"⚠️  未找到 {suffix} 的示例参数，跳过 {file_path.name}")
            return False
        
        # 构建新的调用示例
        new_example = f'''## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "{suffix}" --params '{params}'
```'''
        
        # 替换调用示例部分
        pattern = r'## 调用示例\s*```bash\s*.*?```'
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_example, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 已修正: {file_path.name}")
                return True
            else:
                print(f"⏭️  无需修改: {file_path.name}")
                return False
        else:
            print(f"⚠️  未找到调用示例部分: {file_path.name}")
            return False
    else:
        print(f"⚠️  无法解析文件名: {file_path.name}")
        return False

def main():
    """批量处理所有 API 文档"""
    base_dir = Path("skills/lixinger-data-query/resources/apis")
    
    if not base_dir.exists():
        print(f"❌ 目录不存在: {base_dir}")
        return
    
    total = 0
    fixed = 0
    
    # 遍历所有子目录
    for subdir in ['cn', 'hk', 'us', 'macro']:
        subdir_path = base_dir / subdir
        if not subdir_path.exists():
            continue
        
        print(f"\n📁 处理目录: {subdir}/")
        print("=" * 60)
        
        # 处理该目录下的所有 .md 文件
        for md_file in sorted(subdir_path.glob("*.md")):
            total += 1
            if fix_file(md_file):
                fixed += 1
    
    print("\n" + "=" * 60)
    print(f"✨ 完成！共处理 {total} 个文件，修正 {fixed} 个文件")

if __name__ == "__main__":
    main()
