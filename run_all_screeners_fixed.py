#!/usr/bin/env python3
"""
批量运行所有 company-fundamental 筛选器（修复版）
正确处理已存在的截断ID文件
"""

import json
import os
import subprocess
import re
import time
from datetime import datetime
from glob import glob


def extract_all_urls(file_path):
    """提取所有 company-fundamental URL（完整ID）"""
    urls = []
    seen = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                url = data.get('url', '')
                if 'company-fundamental/' in url and 'screener-id=' in url:
                    match = re.search(r'screener-id=([a-zA-Z0-9]+)', url)
                    if match:
                        sid = match.group(1)  # 完整24字符ID
                        if sid not in seen:
                            seen.add(sid)
                            area = 'cn'
                            if '/hk' in url:
                                area = 'hk'
                            elif '/us' in url:
                                area = 'us'
                            urls.append({
                                'url': url,
                                'screener_id': sid,
                                'area': area
                            })
            except json.JSONDecodeError:
                continue
    
    return urls


def get_existing_ids(output_dir):
    """获取已存在的screener ID（包括截断的）"""
    existing = set()
    for filepath in glob(os.path.join(output_dir, 'screener_*.json')):
        filename = os.path.basename(filepath)
        # 匹配 screener_{area}_{id}.json
        match = re.search(r'screener_[a-z]+_([a-f0-9]+)\.json$', filename)
        if match:
            sid = match.group(1)
            existing.add(sid)
            # 同时添加完整ID的前缀（如果是截断的）
            if len(sid) == 20:
                existing.add(sid)  # 20字符截断ID
    return existing


def run_screener(url_info, output_dir, skill_dir):
    """运行单个 screener"""
    screener_id = url_info['screener_id']  # 完整24字符
    url = url_info['url']
    area = url_info['area']
    
    # 使用完整ID作为文件名
    json_file = os.path.join(output_dir, f"screener_{area}_{screener_id}.json")
    md_file = os.path.join(output_dir, f"screener_{area}_{screener_id}.md")
    
    cmd = [
        'node', 'request/fetch-lixinger-screener.js',
        '--url', url,
        '--output', 'table-json'
    ]
    
    try:
        result = subprocess.run(cmd, cwd=skill_dir, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            with open(json_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            # 同时获取 markdown
            cmd_md = ['node', 'request/fetch-lixinger-screener.js', '--url', url, '--output', 'markdown']
            result_md = subprocess.run(cmd_md, cwd=skill_dir, capture_output=True, text=True, timeout=60)
            if result_md.returncode == 0:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(result_md.stdout)
            
            try:
                data = json.loads(result.stdout)
                return {
                    'success': True,
                    'screener_id': screener_id,
                    'area': area,
                    'total': data.get('total', 0),
                    'screener_name': data.get('screenerName', 'Unknown'),
                }
            except:
                return {'success': True, 'screener_id': screener_id, 'area': area, 'total': 0}
        else:
            error_file = os.path.join(output_dir, f"screener_{area}_{screener_id}_error.txt")
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\nError: {result.stderr}\n")
            return {'success': False, 'screener_id': screener_id, 'area': area, 'error': result.stderr[:100]}
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'screener_id': screener_id, 'area': area, 'error': 'Timeout'}
    except Exception as e:
        return {'success': False, 'screener_id': screener_id, 'area': area, 'error': str(e)[:100]}


def main():
    # 配置
    links_file = '/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt'
    skill_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener'
    output_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/url_results'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取已存在的ID
    existing_ids = get_existing_ids(output_dir)
    print(f"已存在: {len(existing_ids)} 个")
    
    # 提取所有URL
    all_urls = extract_all_urls(links_file)
    print(f"总共: {len(all_urls)} 个")
    
    # 过滤已存在的（检查完整ID或前20字符）
    urls_todo = []
    for u in all_urls:
        sid = u['screener_id']
        if sid not in existing_ids and sid[:20] not in existing_ids:
            urls_todo.append(u)
    
    print(f"待处理: {len(urls_todo)} 个\n")
    
    if len(urls_todo) == 0:
        print("✓ 所有筛选器都已处理完成!")
        return
    
    # 每批处理数量
    BATCH_SIZE = 3
    batch = urls_todo[:BATCH_SIZE]
    remaining = len(urls_todo) - len(batch)
    
    print(f"本批次: {len(batch)} 个 | 剩余: {remaining} 个")
    print(f"{'='*60}\n")
    
    # 运行
    success = 0
    failed = 0
    total_stocks = 0
    
    for i, url_info in enumerate(batch, 1):
        print(f"[{i}/{len(batch)}] {url_info['screener_id']} [{url_info['area']}] ", end='', flush=True)
        
        result = run_screener(url_info, output_dir, skill_dir)
        
        if result['success']:
            success += 1
            total = result.get('total', 0)
            total_stocks += total
            name = result.get('screener_name', 'Unknown')
            print(f"✓ {total} | {name[:30] if name else 'N/A'}...")
        else:
            failed += 1
            print(f"✗ {result.get('error', 'Unknown')[:50]}")
        
        # 延迟
        if i < len(batch):
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"成功: {success} | 失败: {failed}")
    print(f"股票数: {total_stocks}")
    print(f"剩余: {remaining} 个")
    
    if remaining > 0:
        print(f"\n提示: 再次运行继续处理剩余 {remaining} 个")


if __name__ == '__main__':
    main()
