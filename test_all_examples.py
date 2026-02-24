import os
import glob
import re
import subprocess

docs_dir = 'skills/lixinger-data-query/resources/apis'
md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)

success_count = 0
fail_count = 0
failed_examples = []

print(f"Found {len(md_files)} documentation files to check.")

for filepath in md_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the bash example:
    # ```bash
    # python skills/lixinger-data-query/scripts/query_tool.py ...
    # ```
    match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?)\n```', content, re.DOTALL)
    if match:
        command = match.group(1).strip()
        print(f"\n[{filepath}]: Running example...")
        # print(f"Command: {command}")
        
        try:
            # Run the command, capture output
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(" -> SUCCESS")
            # print(result.stdout[:200] + "...") # Print limited output for verification
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(" -> FAILED")
            print(f"Error output:\n{e.stderr.strip() or e.stdout.strip()}")
            failed_examples.append({
                "file": filepath,
                "command": command,
                "error": e.stderr.strip() or e.stdout.strip()
            })
            fail_count += 1
    else:
        print(f"\n[{filepath}]: No valid python example found.")

print("\n" + "="*50)
print(f"Summary: {success_count} success, {fail_count} failed out of {success_count + fail_count} examples.")

if fail_count > 0:
    print("\nFailed examples:")
    for ext in failed_examples:
        print(f"- {ext['file']}")
        print(f"  Command: {ext['command']}")
        print(f"  Error: {ext['error']}")
