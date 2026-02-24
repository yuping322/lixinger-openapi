import os
import glob
import re
import json
import subprocess

docs_dir = 'skills/lixinger-data-query/resources/apis'
md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)

def update_payload_in_md(filepath, modifier_func):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?--params\s+\'(.*?)\'.*?)\n```', content, re.DOTALL)
    if match:
        full_command = match.group(1)
        params_str = match.group(2)
        try:
            payload = json.loads(params_str)
            new_payload = modifier_func(payload)
            new_params_str = json.dumps(new_payload, ensure_ascii=False)
            new_command = full_command.replace(f"'{params_str}'", f"'{new_params_str}'")
            new_content = content.replace(full_command, new_command)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return new_command
        except Exception as e:
            print(f"Error updating payload in {filepath}: {e}")
    return None

def test_and_fix():
    for filepath in md_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'```bash\s*\n(python skills/lixinger-data-query/scripts/query_tool\.py.*?)\n```', content, re.DOTALL)
        if not match: continue
        
        command = match.group(1).strip()
        
        for _ in range(3): # Max 3 attempts
            try:
                res = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"[{filepath}] -> SUCCESS")
                break # Success!
            except subprocess.CalledProcessError as e:
                err_out = e.stderr.strip() or e.stdout.strip()
                if "api is not found" in err_out or "Api was not found" in err_out:
                    print(f"[{filepath}] -> DEAD API")
                    break
                
                # print(f"[{filepath}] -> ERROR: {err_out}")
                
                fixed = False
                
                # Fixes based on error signatures
                if 'conflict with forbidden peer' in err_out:
                    def mod_conflict(p):
                        if 'date' in p and 'startDate' in p:
                            del p['startDate']
                            if 'endDate' in p: del p['endDate']
                        return p
                    command = update_payload_in_md(filepath, mod_conflict) or command
                    fixed = True
                    
                elif '"limit" must be a number' in err_out:
                    command = update_payload_in_md(filepath, lambda p: {**p, 'limit': 10}) or command
                    fixed = True
                    
                elif '"type" is required' in err_out:
                    command = update_payload_in_md(filepath, lambda p: {**p, 'type': 'normal'}) or command
                    fixed = True

                elif '"granularity" must be one of' in err_out or '"granularity" is required' in err_out:
                    command = update_payload_in_md(filepath, lambda p: {**p, 'granularity': 'q'}) or command
                    fixed = True
                    
                elif '"fsTableType" must be one of' in err_out:
                    command = update_payload_in_md(filepath, lambda p: {**p, 'fsTableType': 'non_financial'}) or command
                    fixed = True
                    
                elif '"stockCode" is required' in err_out:
                    def mod_sc(p):
                        # Use first item of stockCodes or a default
                        sc = p.get('stockCodes', ['600519'])[0]
                        p['stockCode'] = sc
                        return p
                    command = update_payload_in_md(filepath, mod_sc) or command
                    fixed = True

                elif '"stockCodes" is required' in err_out:
                    def mod_scs(p):
                        if 'stockCode' in p: p['stockCodes'] = [p['stockCode']]
                        else: p['stockCodes'] = ['600519']
                        return p
                    command = update_payload_in_md(filepath, mod_scs) or command
                    fixed = True

                elif 'invalid price metrics' in err_out or 'invalid fs metrics' in err_out:
                    # just try removing metricsList
                    def mod_metrics(p):
                        if 'metricsList' in p: del p['metricsList']
                        return p
                    command = update_payload_in_md(filepath, mod_metrics) or command
                    fixed = True

                elif '"metricsList" is required' in err_out:
                    # just try removing metricsList
                    command = update_payload_in_md(filepath, lambda p: {**p, 'metricsList': ['pe_ttm']}) or command
                    fixed = True
                    
                if not fixed:
                    print(f"[{filepath}] -> UNFIXABLE ERROR: {err_out}")
                    break

test_and_fix()
