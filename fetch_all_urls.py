#!/usr/bin/env python3
"""
从 links.txt 中提取 URL 并用 requests 批量获取内容
结果保存到指定文件夹
"""

import json
import os
import re
import time
from urllib.parse import urlparse
import requests
from datetime import datetime


def sanitize_filename(url):
    """将 URL 转换为安全的文件名"""
    # 移除协议
    url = re.sub(r'^https?://', '', url)
    # 替换特殊字符
    url = re.sub(r'[<>:"/\\|?*]', '_', url)
    # 限制长度
    if len(url) > 200:
        url = url[:200]
    return url


def extract_urls_from_links(file_path):
    """从 links.txt 中提取 URL"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if 'url' in data:
                    urls.append(data['url'])
            except json.JSONDecodeError:
                # 如果不是 JSON，尝试直接作为 URL
                if line.startswith('http'):
                    urls.append(line)
    return urls


def fetch_url(url, headers=None, timeout=30):
    """获取单个 URL 的内容"""
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(url, headers=default_headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        return {
            'success': True,
            'status_code': response.status_code,
            'url': response.url,
            'content_type': response.headers.get('Content-Type', 'unknown'),
            'content_length': len(response.content),
            'text': response.text,
            'encoding': response.encoding
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }


def main():
    # 配置
    links_file = '/Users/fengzhi/Downloads/git/lixinger-openapi/links.txt'
    output_dir = '/Users/fengzhi/Downloads/git/lixinger-openapi/url_results'
    
    # 创建输出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_folder = os.path.join(output_dir, f'fetch_results_{timestamp}')
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"输出目录: {output_folder}")
    
    # 提取 URL
    print(f"正在从 {links_file} 提取 URL...")
    urls = extract_urls_from_links(links_file)
    print(f"找到 {len(urls)} 个 URL")
    
    # 统计
    success_count = 0
    fail_count = 0
    results_summary = []
    
    # 批量获取
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] 正在获取: {url[:80]}...")
        
        result = fetch_url(url)
        
        # 生成文件名
        safe_name = sanitize_filename(url)
        if len(safe_name) < 10:
            safe_name = f"url_{i:04d}_{safe_name}"
        
        # 保存结果
        if result['success']:
            success_count += 1
            
            # 根据内容类型决定文件扩展名
            content_type = result.get('content_type', '')
            if 'json' in content_type:
                ext = 'json'
            elif 'html' in content_type:
                ext = 'html'
            elif 'text' in content_type:
                ext = 'txt'
            else:
                ext = 'txt'
            
            filename = f"{safe_name}.{ext}"
            filepath = os.path.join(output_folder, filename)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            
            print(f"  ✓ 成功保存到: {filename}")
            
            results_summary.append({
                'index': i,
                'url': url,
                'status': 'success',
                'status_code': result['status_code'],
                'final_url': result['url'],
                'content_type': result['content_type'],
                'content_length': result['content_length'],
                'filename': filename
            })
        else:
            fail_count += 1
            print(f"  ✗ 失败: {result['error']}")
            
            # 保存错误信息
            filename = f"{safe_name}_error.txt"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"Error: {result['error']}\n")
            
            results_summary.append({
                'index': i,
                'url': url,
                'status': 'failed',
                'error': result['error'],
                'filename': filename
            })
        
        # 添加延迟，避免请求过快
        time.sleep(0.5)
    
    # 保存汇总结果
    summary_file = os.path.join(output_folder, '_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(urls),
            'success': success_count,
            'failed': fail_count,
            'results': results_summary
        }, f, ensure_ascii=False, indent=2)
    
    # 打印汇总
    print(f"\n{'='*60}")
    print(f"完成!")
    print(f"总 URL 数: {len(urls)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"结果保存在: {output_folder}")
    print(f"汇总文件: {summary_file}")


if __name__ == '__main__':
    main()
