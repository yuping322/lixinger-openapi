import os
import glob
import re

base_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query/resources/apis'

generic_return_fields = """
## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `{id_field}` | string | {id_desc} |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |
"""

k_line_return_fields = """
## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `{id_field}` | string | {id_desc} |
| `open` | number | 开盘价 |
| `close` | number | 收盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `volume` | number | 成交量 |
| `amount` | number | 成交额 |
| `change` | number | 涨跌幅 |
| `to_r` | number | 换手率 |
"""

def update_files(pattern):
    for filepath in glob.glob(pattern, recursive=True):
        if not os.path.isfile(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '## 返回字段' in content: continue

        # Determine id field
        if 'macro' in filepath:
            id_field = 'areaCode'
            id_desc = '地域代码'
        else:
            id_field = 'stockCode'
            id_desc = '代码'
            
        fields_to_add = k_line_return_fields if 'k_line' in filepath else generic_return_fields
        append_text = fields_to_add.format(id_field=id_field, id_desc=id_desc)
        
        # Insert before "## 调用示例"
        if '## 调用示例' in content:
            new_content = content.replace('## 调用示例', append_text.strip() + '\n\n## 调用示例')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
        else:
            print(f"Skipped {filepath} (no 调用示例 found)")

# Update hk, us, macro
update_files(f"{base_dir}/hk/*.md")
update_files(f"{base_dir}/us/*.md")
update_files(f"{base_dir}/macro/*.md")

# Also fix any remaining cn files
update_files(f"{base_dir}/cn/*.md")
