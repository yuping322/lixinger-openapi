#!/usr/bin/env python3
"""
批量运行前10个 screener URL
结果保存到指定目录
"""

import json
import os
import subprocess
from datetime import datetime


def extract_unique_screener_urls(file_path, limit=10):
    """提取前N个唯一的 screener URL"""
    urls = []
    seen_ids = set()
    
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
                    # 提取 screener-id
                    import re
                    match = re.search(r'screener-id=([a-zA-Z0-9]+)', url)
                    if match:
                        screener_id = match.group(1)
                        if screener_id not in seen_ids:
                            seen_ids.add(screener_id)
                            urls.append({
                                'url': url,
                                'screener_id': screener_id,
                                'status': data.get('status', 'unknown')
                            })
                            if len(urls) >= limit:
                                break
            except json.JSONDecodeError:
                continue
    
    return urls


def run_screener(url_info, output_dir, skill_dir):
    """运行单个 screener 并保存结果"""
    screener_id = url_info['screener_id']
    url = url_info['url']
    
    # 构建命令 - 使用 table-json 格式以便保存完整数据
    cmd = [
        'node', 'request/fetch-lixinger-screener.js',
        '--url', url,
        '--output', 'table-json'
    ]
    
    # 输出文件名
    safe_id = screener_id[:20]  # 截短避免文件名过长
    output_file = os.path.join(output_dir, f"screener_{safe_id}.json")
    markdown_file = os.path.join(output_dir, f"screener_{safe_id}.md")
    
    try:
        # 执行命令获取 JSON 结果
        result = subprocess.run(
            cmd,
            cwd=skill_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # 保存 JSON 结果
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            # 同时获取 markdown 格式便于阅读
            cmd_md = [
                'node', 'request/fetch-lixinger-screener.js',
                '--url', url,
                '--output', 'markdown'
            ]
            result_md = subprocess.run(
                cmd_md,
                cwd=skill_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result_md.returncode == 0:
                with open(markdown_file, 'w', encoding='utf-8') as f:
                    f.write(result_md.stdout)
            
            # 解析结果获取统计信息
            try:
                data = json.loads(result.stdout)
                total = data.get('total', 0)
                screener_name = data.get('screenerName', 'Unknown')
                return {
                    'success': True,
                    'screener_id': screener_id,
                    'url': url,
                    'total': total,
                    'screener_name': screener_name,
                    'json_file': os.path.basename(output_file),
                    'markdown_file': os.path.basename(markdown_file)
                }
            except:
                return {
                    'success': True,
                    'screener_id': screener_id,
                    'url': url,
                    'json_file': os.path.basename(output_file),
                    'markdown_file': os.path.basename(markdown_file)
                }
        else:
            # 保存错误信息
            error_file = os.path.join(output_dir, f"screener_{safe_id}_error.txt")
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"Error: {result.stderr}\n")
            
            return {
                'success': False,
                'screener_id': screener_id,
                'url': url,
                'error': result.stderr[:200],
                'error_file': os.path.basename(error_file)
            }
            
    except subprocess.TimeoutExpired:
        error_file = os.path.join(output_dir, f"screener_{safe_id}_error.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Error: Timeout\n")
        
        return {
            'success': False,
            'screener_id': screener_id,
            'url': url,
            'error': 'Timeout',
            'error_file': os.path.basename(error_file)
        }
    except Exception as e:
        error_file = os.path.join(output_dir, f"screener_{safe_id}_error.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Error: {str(e)}\n")
        
        return {
            'success': False,
            'screener_id': screener_id,
            'url': url,
            'error': str(e)[:200],
            'error_file': os.path.basename(error_file)
        }


def main():
    # 配置
    links_file = '/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt'
    skill_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener'
    output_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/url_results'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输出目录: {output_dir}")
    
    # 提取前10个唯一的 screener URL
    print(f"\n正在从 {links_file} 提取前10个 screener...")
    screener_urls = extract_unique_screener_urls(links_file, limit=10)
    print(f"找到 {len(screener_urls)} 个 screener\n")
    
    # 打印将要处理的 URL
    print("将要处理的 screener:")
    for i, info in enumerate(screener_urls, 1):
        print(f"  {i}. {info['url'][:80]}...")
    print()
    
    # 批量运行
    success_count = 0
    fail_count = 0
    results_summary = []
    
    for i, url_info in enumerate(screener_urls, 1):
        print(f"[{i}/{len(screener_urls)}] 正在处理: {url_info['screener_id'][:20]}...")
        
        result = run_screener(url_info, output_dir, skill_dir)
        
        if result['success']:
            success_count += 1
            total = result.get('total', 'N/A')
            name = result.get('screener_name', 'Unknown')
            print(f"  ✓ 成功 | 名称: {name[:30] if name else 'N/A'}... | 结果数: {total}")
        else:
            fail_count += 1
            print(f"  ✗ 失败: {result.get('error', 'Unknown')[:80]}")
        
        results_summary.append(result)
    
    # 保存汇总结果
    summary_file = os.path.join(output_dir, '_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(screener_urls),
            'success': success_count,
            'failed': fail_count,
            'results': results_summary
        }, f, ensure_ascii=False, indent=2)
    
    # 同时保存一个易读的 markdown 汇总
    summary_md = os.path.join(output_dir, '_summary.md')
    with open(summary_md, 'w', encoding='utf-8') as f:
        f.write(f"# Screener 批量获取结果\n\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"总计: {len(screener_urls)} | 成功: {success_count} | 失败: {fail_count}\n\n")
        f.write("## 详细结果\n\n")
        f.write("| # | 状态 | Screener ID | 名称 | 结果数 | 文件 |\n")
        f.write("|---|------|-------------|------|--------|------|\n")
        for i, r in enumerate(results_summary, 1):
            status = "✓" if r['success'] else "✗"
            name = r.get('screener_name', 'N/A')[:20] if r.get('screener_name') else 'N/A'
            total = r.get('total', 'N/A')
            file_link = r.get('json_file', r.get('error_file', 'N/A'))
            f.write(f"| {i} | {status} | {r['screener_id'][:16]}... | {name} | {total} | {file_link} |\n")
    
    # 打印汇总
    print(f"\n{'='*60}")
    print(f"完成!")
    print(f"总 screener 数: {len(screener_urls)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"结果保存在: {output_dir}")
    print(f"汇总文件: {summary_file}")


if __name__ == '__main__':
    main()
