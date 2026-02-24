import os
import glob
import re
import subprocess

docs_dir = 'skills/lixinger-data-query/resources/apis'
md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)

empty_examples = []
success_count = 0

print(f"Checking {len(md_files)} documentation files for empty results...")

for filepath in md_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?)\n```', content, re.DOTALL)
    if match:
        command = match.group(1).strip()
        
        try:
            # Run the command with json format to parse easily
            json_command = command + " --format json"
            res = subprocess.run(json_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            import json
            try:
                data = json.loads(res.stdout)
                # check if data is empty
                is_empty = False
                if 'data' in data:
                    if isinstance(data['data'], list) and len(data['data']) == 0:
                        is_empty = True
                    elif isinstance(data['data'], dict) and not data['data']:
                        is_empty = True
                else: 
                    # list might be at root if not encapsulated
                    if isinstance(data, list) and len(data) == 0:
                        is_empty = True
                        
                if is_empty:
                    print(f"[{filepath}] -> EMPTY RESULT")
                    empty_examples.append(filepath)
                else:
                    # print(f"[{filepath}] -> HAS DATA")
                    success_count += 1
            except Exception as e:
                print(f"[{filepath}] -> FAILED TO PARSE JSON: {e}")
        except subprocess.CalledProcessError as e:
            # In case some are still failing (should not be as per previous fixes)
            print(f"[{filepath}] -> FAILED TO RUN: {e.stderr.strip()}")

print("\n" + "="*50)
print(f"Summary: {success_count} with data, {len(empty_examples)} empty.")
if empty_examples:
    print("\nEmpty Example Files:")
    for f in empty_examples:
        print(f" - {f}")
