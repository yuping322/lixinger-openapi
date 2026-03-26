#!/usr/bin/env python3
"""
批量运行 company-fundamental 类型的 screener
结果保存到指定目录
"""

import json
import os
import subprocess
from datetime import datetime


def extract_company_fundamental_urls(file_path, limit=30):
    """提取 company-fundamental 类型的 screener URL"""
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
                # 只保留 company-fundamental 类型
                if 'company-fundamental/' in url and 'screener-id=' in url:
                    match = __import__('re').search(r'screener-id=([a-zA-Z0-9]+)', url)
                    if match:
                        sid = match.group(1)
                        if sid not in seen:
                            seen.add(sid)
                            # 提取区域代码
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
                            if len(urls) >= limit:
                                break
            except json.JSONDecodeError:
                continue
    
    return urls


def run_screener(url_info, output_dir, skill_dir):
    """运行单个 screener 并保存结果"""
    screener_id = url_info['screener_id']
    url = url_info['url']
    area = url_info['area']
    
    # 构建命令
    cmd = [
        'node', 'request/fetch-lixinger-screener.js',
        '--url', url,
        '--output', 'table-json'
    ]
    
    # 输出文件名
    safe_id = screener_id[:20]
    json_file = os.path.join(output_dir, f"screener_{area}_{safe_id}.json")
    md_file = os.path.join(output_dir, f"screener_{area}_{safe_id}.md")
    
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
            with open(json_file, 'w', encoding='utf-8') as f:
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
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(result_md.stdout)
            
            # 解析结果获取统计信息
            try:
                data = json.loads(result.stdout)
                return {
                    'success': True,
                    'screener_id': screener_id,
                    'area': area,
                    'url': url,
                    'total': data.get('total', 0),
                    'screener_name': data.get('screenerName', 'Unknown'),
                    'screener_description': data.get('screenerDescription'),
                    'json_file': os.path.basename(json_file),
                    'md_file': os.path.basename(md_file)
                }
            except:
                return {
                    'success': True,
                    'screener_id': screener_id,
                    'area': area,
                    'url': url,
                    'json_file': os.path.basename(json_file),
                    'md_file': os.path.basename(md_file)
                }
        else:
            # 保存错误信息
            error_file = os.path.join(output_dir, f"screener_{area}_{safe_id}_error.txt")
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"Error: {result.stderr}\n")
            
            return {
                'success': False,
                'screener_id': screener_id,
                'area': area,
                'url': url,
                'error': result.stderr[:200],
                'error_file': os.path.basename(error_file)
            }
            
    except subprocess.TimeoutExpired:
        error_file = os.path.join(output_dir, f"screener_{area}_{safe_id}_error.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Error: Timeout\n")
        
        return {
            'success': False,
            'screener_id': screener_id,
            'area': area,
            'url': url,
            'error': 'Timeout',
            'error_file': os.path.basename(error_file)
        }
    except Exception as e:
        error_file = os.path.join(output_dir, f"screener_{area}_{safe_id}_error.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Error: {str(e)}\n")
        
        return {
            'success': False,
            'screener_id': screener_id,
            'area': area,
            'url': url,
            'error': str(e)[:200],
            'error_file': os.path.basename(error_file)
        }


def main():
    # 配置
    links_file = '/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt'
    skill_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-screener'
    output_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/url_results'
    limit = 30  # 只跑30个
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输出目录: {output_dir}")
    print(f"计划处理: {limit} 个 company-fundamental 筛选器\n")
    
    # 提取 URL
    print(f"正在从 {links_file} 提取 company-fundamental 筛选器...")
    screener_urls = extract_company_fundamental_urls(links_file, limit=limit)
    print(f"找到 {len(screener_urls)} 个筛选器\n")
    
    # 统计
    cn_count = sum(1 for u in screener_urls if u['area'] == 'cn')
    hk_count = sum(1 for u in screener_urls if u['area'] == 'hk')
    print(f"  - A股 (cn): {cn_count}")
    print(f"  - 港股 (hk): {hk_count}")
    print()
    
    # 批量运行
    success_count = 0
    fail_count = 0
    results_summary = []
    
    for i, url_info in enumerate(screener_urls, 1):
        print(f"[{i}/{len(screener_urls)}] 正在处理: {url_info['screener_id'][:20]}... [{url_info['area']}]")
        
        result = run_screener(url_info, output_dir, skill_dir)
        
        if result['success']:
            success_count += 1
            total = result.get('total', 'N/A')
            name = result.get('screener_name', 'Unknown')
            desc = result.get('screener_description', '')
            if desc:
                desc_short = desc[:40] + '...' if len(desc) > 40 else desc
            else:
                desc_short = 'N/A'
            print(f"  ✓ 成功 | 结果数: {total:4d} | {name[:30] if name else 'N/A'}...")
        else:
            fail_count += 1
            print(f"  ✗ 失败: {result.get('error', 'Unknown')[:80]}")
        
        results_summary.append(result)
    
    # 保存汇总结果
    summary_file = os.path.join(output_dir, '_summary_30.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(screener_urls),
            'success': success_count,
            'failed': fail_count,
            'results': results_summary
        }, f, ensure_ascii=False, indent=2)
    
    # 同时保存一个易读的 markdown 汇总
    summary_md = os.path.join(output_dir, '_summary_30.md')
    with open(summary_md, 'w', encoding='utf-8') as f:
        f.write(f"# Company Fundamental Screener 批量获取结果\n\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"总计: {len(screener_urls)} | 成功: {success_count} | 失败: {fail_count}\n\n")
        f.write("## 详细结果\n\n")
        f.write("| # | 区域 | Screener ID | 名称 | 结果数 | 文件 |\n")
        f.write("|---|------|-------------|------|--------|------|\n")
        for i, r in enumerate(results_summary, 1):
            status = "✓" if r['success'] else "✗"
            name = r.get('screener_name', 'N/A')[:25] if r.get('screener_name') else 'N/A'
            total = r.get('total', 'N/A')
            area = r.get('area', 'cn')
            file_link = r.get('json_file', r.get('error_file', 'N/A'))
            f.write(f"| {i} | {area} | {r['screener_id'][:16]}... | {name} | {total} | {file_link} |\n")
        
        # 添加统计信息
        f.write(f"\n## 统计\n\n")
        f.write(f"- 有结果的筛选器 (>0): {sum(1 for r in results_summary if r.get('success') and r.get('total', 0) > 0)}\n")
        f.write(f"- 结果数为0的筛选器: {sum(1 for r in results_summary if r.get('success') and r.get('total', 0) == 0)}\n")
        total_stocks = sum(r.get('total', 0) for r in results_summary if r.get('success'))
        f.write(f"- 总股票数: {total_stocks}\n")
    
    # 打印汇总
    print(f"\n{'='*60}")
    print(f"完成!")
    print(f"总筛选器数: {len(screener_urls)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"有结果的筛选器: {sum(1 for r in results_summary if r.get('success') and r.get('total', 0) > 0)}")
    print(f"结果数为0的筛选器: {sum(1 for r in results_summary if r.get('success') and r.get('total', 0) == 0)}")
    total_stocks = sum(r.get('total', 0) for r in results_summary if r.get('success'))
    print(f"总股票数: {total_stocks}")
    print(f"结果保存在: {output_dir}")
    print(f"汇总文件: {summary_md}")


if __name__ == '__main__':
    main()
