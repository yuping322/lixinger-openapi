import os
import glob
import re
import json

docs_dir = 'skills/lixinger-data-query/resources/apis'
md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)

defaults = {
    'cn': {'stockCode': '600519', 'stockCodes': ['600519'], 'areaCode': 'cn', 'source': 'sw'},
    'hk': {'stockCode': '00700', 'stockCodes': ['00700'], 'areaCode': 'hk', 'source': 'sw'},
    'us': {'stockCode': '.INX', 'stockCodes': ['.INX'], 'areaCode': 'us', 'source': 'sw'},
    'macro': {'areaCode': 'cn', 'country': 'cn'}
}

common_defaults = {
    'date': '2024-12-31',
    'startDate': '2020-01-01',
    'endDate': '2024-12-31',
    'metricsList': ['pe_ttm'],
    'type': 'normal',
    'source': 'sw',
    'granularity': 'daily'
}

for filepath in md_files:
    region = 'cn'
    if '/hk/' in filepath: region = 'hk'
    elif '/us/' in filepath: region = 'us'
    elif '/macro/' in filepath: region = 'macro'

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        suffix_match = re.search(r'\-\s*\*\*URL 后缀\*\*\s*:\s*[`]([^`]+)[`]', content)
        if not suffix_match:
            continue
        correct_suffix = suffix_match.group(1).strip()

        all_params = set()
        in_table = False
        for line in content.split('\n'):
            if '## 查询参数' in line:
                in_table = True
            elif '## 返回字段' in line or '## 调用示例' in line:
                in_table = False
            
            if in_table and line.startswith('|') and not line.startswith('| 参数名') and not line.startswith('| :---'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:
                    param_name_raw = parts[1]
                    param_name_match = re.search(r'`([^`]+)`', param_name_raw)
                    if param_name_match:
                        param_name = param_name_match.group(1)
                        if param_name != 'token':
                            all_params.add(param_name)

        payload = {}
        # Force inject default values for any known parameter mentioned in the docs
        for param in all_params:
            if param in defaults[region]:
                payload[param] = defaults[region][param]
            elif param in common_defaults:
                payload[param] = common_defaults[param]
            else:
                payload[param] = 'example_value'
        
        # Additional safeguards based on test output
        if 'startDate' not in payload and 'endDate' not in payload and 'date' not in payload:
            if 'date' in all_params: payload['date'] = '2024-12-31'
            elif 'startDate' in all_params: 
                payload['startDate'] = '2020-01-01'
                payload['endDate'] = '2024-12-31'
                
        # API requires stockCodes or stockCode for most things if not macro
        if region != 'macro':
            if 'stockCode' in all_params and 'stockCode' not in payload: payload['stockCode'] = defaults[region]['stockCode']
            if 'stockCodes' in all_params and 'stockCodes' not in payload: payload['stockCodes'] = defaults[region]['stockCodes']

        payload_str = json.dumps(payload, ensure_ascii=False)
        
        example_block = f"""```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "{correct_suffix}" --params '{payload_str}'
```"""
        
        new_content = re.sub(r'```bash\s*\n.*?\n```', example_block, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        pass
