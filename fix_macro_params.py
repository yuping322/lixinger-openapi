import glob

macro_files = glob.glob('/Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query/resources/apis/macro/*.md')

for filepath in macro_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace stockCodes description
    if 'stockCodes' in content and '股票代码列表' in content:
        content = content.replace('| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |', 
                                  '| `areaCode` | string | 是 | 地域代码，如 `"cn"`, `"us"` |')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Fixed parameters in {len(macro_files)} macro files.")
