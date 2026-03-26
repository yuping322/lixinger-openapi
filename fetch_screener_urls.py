#!/usr/bin/env python3
"""
从 links.txt 中提取理杏仁 screener URL
并用 fetch-lixinger-screener.js 的 request 版本获取数据
"""

import json
import os
import re
import subprocess
from urllib.parse import urlparse, parse_qs
from datetime import datetime


def extract_screener_urls(file_path):
    """提取带有 screener-id 的 URL"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                url = data.get('url', '')
                # 只保留带有 screener-id 的 screener URL
                if 'screener' in url and 'screener-id=' in url:
                    urls.append({
                        'url': url,
                        'status': data.get('status', 'unknown'),
                        'addedAt': data.get('addedAt'),
                        'fetchedAt': data.get('fetchedAt')
                    })
            except json.JSONDecodeError:
                continue
    return urls


def extract_screener_info(url):
    """从 URL 提取 screener-id 和区域代码"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    screener_id = params.get('screener-id', [None])[0]
    
    # 从路径提取区域代码 (cn, hk, us)
    path_parts = parsed.path.split('/')
    area_code = 'cn'  # 默认
    for part in path_parts:
        if part in ['cn', 'hk', 'us']:
            area_code = part
            break
    
    return {
        'screener_id': screener_id,
        'area_code': area_code,
        'full_url': url
    }


def run_fetch_screener(screener_info, output_dir, skill_dir):
    """使用 fetch-lixinger-screener.js 获取数据"""
    screener_id = screener_info['screener_id']
    area_code = screener_info['area_code']
    
    # 构建 URL
    base_url = f"https://www.lixinger.com/analytics/screener/company-fundamental/{area_code}"
    full_url = f"{base_url}?screener-id={screener_id}"
    
    # 输出文件名
    safe_id = re.sub(r'[^a-zA-Z0-9]', '_', screener_id)
    output_file = os.path.join(output_dir, f"screener_{safe_id}.json")
    
    # 构建命令
    cmd = [
        'node', 'request/fetch-lixinger-screener.js',
        '--url', full_url,
        '--output', 'table-json'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=skill_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # 保存结果
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            return {
                'success': True,
                'screener_id': screener_id,
                'output_file': output_file,
                'url': full_url
            }
        else:
            return {
                'success': False,
                'screener_id': screener_id,
                'error': result.stderr,
                'url': full_url
            }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'screener_id': screener_id,
            'error': 'Timeout',
            'url': full_url
        }
    except Exception as e:
        return {
            'success': False,
            'screener_id': screener_id,
            'error': str(e),
            'url': full_url
        }


def main():
    # 配置
    links_file = '/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt'
    skill_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener'
    output_base = '/Users/fengzhi/Downloads/git/lixinger-openapi/screener_results'
    
    # 创建输出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(output_base, f'screener_fetch_{timestamp}')
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输出目录: {output_dir}")
    
    # 提取 screener URL
    print(f"正在从 {links_file} 提取 screener URL...")
    screener_urls = extract_screener_urls(links_file)
    print(f"找到 {len(screener_urls)} 个 screener URL")
    
    # 去重（基于 screener-id）
    seen_ids = set()
    unique_urls = []
    for item in screener_urls:
        info = extract_screener_info(item['url'])
        if info['screener_id'] and info['screener_id'] not in seen_ids:
            seen_ids.add(info['screener_id'])
            unique_urls.append(info)
    
    print(f"去重后: {len(unique_urls)} 个唯一 screener")
    
    # 限制处理数量（避免太多）
    max_to_process = 50  # 可以先处理前50个测试
    urls_to_process = unique_urls[:max_to_process]
    print(f"将处理前 {len(urls_to_process)} 个 screener")
    
    # 批量获取
    success_count = 0
    fail_count = 0
    results_summary = []
    
    for i, screener_info in enumerate(urls_to_process, 1):
        print(f"\n[{i}/{len(urls_to_process)}] 正在获取 screener: {screener_info['screener_id'][:20]}...")
        print(f"  URL: {screener_info['full_url'][:80]}...")
        
        result = run_fetch_screener(screener_info, output_dir, skill_dir)
        
        if result['success']:
            success_count += 1
            print(f"  ✓ 成功")
        else:
            fail_count += 1
            print(f"  ✗ 失败: {result.get('error', 'Unknown error')[:100]}")
        
        results_summary.append(result)
    
    # 保存汇总结果
    summary_file = os.path.join(output_dir, '_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(urls_to_process),
            'success': success_count,
            'failed': fail_count,
            'results': results_summary
        }, f, ensure_ascii=False, indent=2)
    
    # 打印汇总
    print(f"\n{'='*60}")
    print(f"完成!")
    print(f"总 screener 数: {len(urls_to_process)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"结果保存在: {output_dir}")
    print(f"汇总文件: {summary_file}")
    
    # 如果有失败的，保存到单独文件
    failed_results = [r for r in results_summary if not r['success']]
    if failed_results:
        failed_file = os.path.join(output_dir, '_failed.json')
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_results, f, ensure_ascii=False, indent=2)
        print(f"失败记录: {failed_file}")


if __name__ == '__main__':
    main()
