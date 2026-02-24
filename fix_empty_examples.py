import os
import glob
import re
import json
import subprocess

empty_files = [
    "skills/lixinger-data-query/resources/apis/hk/hk_index_basic_info.md",
    "skills/lixinger-data-query/resources/apis/hk/hk_index_constituents.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_fund_basic_info.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_fund_dividend.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_trading_abnormal.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_fund_net_value.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_operation_data.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_executive_shareholding.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_index_constituents.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_index_basic_info.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_industry_basic_info.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_equity_pledge.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_block_trade.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_investor.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_official_reserve_assets.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_real_estate.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_energy.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_gdp.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_central_bank_balance_sheet.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_population.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_foreign_trade.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_money_supply.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_foreign_assets.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_unemployment_rate.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_social_financing.md",
    "skills/lixinger-data-query/resources/apis/macro/macro_price_index.md"
]

def update_payload_in_md(filepath, modifier_func):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?--params\s+\'(.*?)\'.*?)\n```', content, re.DOTALL)
    if match:
        full_command = match.group(1)
        params_str = match.group(2)
        try:
            payload = json.loads(params_str)
            new_payload = modifier_func(payload, filepath)
            new_params_str = json.dumps(new_payload, ensure_ascii=False)
            new_command = full_command.replace(f"'{params_str}'", f"'{new_params_str}'")
            new_content = content.replace(full_command, new_command)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return new_command
        except Exception as e:
            print(f"Error updating payload in {filepath}: {e}")
    return None

def mod_payload(payload, filepath):
    # 1. Correct the stock/index/fund codes based on the domain
    if 'cn_fund' in filepath:
        if 'stockCode' in payload: payload['stockCode'] = '510300'
        if 'stockCodes' in payload: payload['stockCodes'] = ['510300']
    elif 'cn_index' in filepath:
        if 'stockCode' in payload: payload['stockCode'] = '000300'
        if 'stockCodes' in payload: payload['stockCodes'] = ['000300']
    elif 'hk_index' in filepath:
        if 'stockCode' in payload: payload['stockCode'] = 'HSI'
        if 'stockCodes' in payload: payload['stockCodes'] = ['HSI']
    elif 'cn_industry' in filepath:
        if 'stockCode' in payload: payload['stockCode'] = '801000' # Default SW industry
        if 'stockCodes' in payload: payload['stockCodes'] = ['801000']
        
    # 2. Broaden date ranges significantly to ensure events (like pledges or block trades) are captured
    if 'date' in payload:
        # If it only supports date, move it to 2023-12-31.
        payload['date'] = '2023-12-31'
    if 'startDate' in payload:
        payload['startDate'] = '2015-01-01'
    
    # 3. Handle Macro specific quirks
    if 'macro' in filepath:
        # Macro data points are sparse. A broad range is best.
        if 'startDate' in payload: payload['startDate'] = '2010-01-01'
        if 'date' in payload: 
            # some macro APIs only take date, some take startDate/endDate. 
            pass 
            
    return payload

for fp in empty_files:
    if os.path.exists(fp):
        update_payload_in_md(fp, mod_payload)

print("Updated parameters to fix empty data results.")
