import os
import glob
import re
import json

files = [
    "skills/lixinger-data-query/resources/apis/cn/cn_company_trading_abnormal.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_operation_data.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_industry_basic_info.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_equity_pledge.md",
    "skills/lixinger-data-query/resources/apis/cn/cn_company_block_trade.md"
]

def update_payload_in_md(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?--params\s+\'(.*?)\'.*?)\n```', content, re.DOTALL)
    if match:
        full_command = match.group(1)
        params_str = match.group(2)
        try:
            payload = json.loads(params_str)
            
            # Fix industry code
            if 'cn_industry' in filepath:
                if 'stockCode' in payload: payload['stockCode'] = '801120'
                if 'stockCodes' in payload: payload['stockCodes'] = ['801120']
                
            # Fix company events
            if 'cn_company' in filepath:
                if 'stockCode' in payload: payload['stockCode'] = '000001'
                if 'stockCodes' in payload: payload['stockCodes'] = ['000001']
                payload['startDate'] = '2010-01-01'
            
            new_params_str = json.dumps(payload, ensure_ascii=False)
            new_command = full_command.replace(f"'{params_str}'", f"'{new_params_str}'")
            new_content = content.replace(full_command, new_command)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"Error updating payload in {filepath}: {e}")

for fp in files:
    update_payload_in_md(fp)
