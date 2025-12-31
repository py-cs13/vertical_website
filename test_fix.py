#!/usr/bin/env python3
"""
测试脚本，用于验证前端是否已清除所有测试相关的标题
"""

import os
import re

def search_for_test_terms(directory):
    """搜索目录中所有包含测试字样的文件"""
    test_terms = ["测试文章", "测试工具包", "测试"]
    found_matches = []
    
    for root, dirs, files in os.walk(directory):
        # 跳过node_modules和其他不需要的目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'build']]
        
        for file in files:
            if file.endswith(('.vue', '.js', '.html')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        for term in test_terms:
                            matches = re.finditer(term, content)
                            for match in matches:
                                # 获取匹配行的上下文
                                lines = content.split('\n')
                                line_num = content[:match.start()].count('\n') + 1
                                line_content = lines[line_num - 1].strip()
                                
                                # 忽略注释和日志中的测试字样
                                if not (line_content.startswith('//') or line_content.startswith('/*') or line_content.startswith('*')):
                                    found_matches.append({
                                        'file': file_path,
                                        'line': line_num,
                                        'content': line_content,
                                        'term': term
                                    })
                except Exception as e:
                    print(f"无法读取文件 {file_path}: {e}")
    
    return found_matches

def main():
    # 搜索前端目录
    frontend_dir = '/Users/shucui/Desktop/vertical_website/frontend/src'
    print(f"搜索前端目录: {frontend_dir}")
    
    matches = search_for_test_terms(frontend_dir)
    
    if matches:
        print("发现以下测试相关的内容:")
        for match in matches:
            print(f"文件: {match['file']}")
            print(f"行号: {match['line']}")
            print(f"内容: {match['content']}")
            print(f"匹配项: {match['term']}")
            print("-" * 50)
    else:
        print("✅ 前端目录中未发现测试相关的标题")
        print("修复成功！")

if __name__ == "__main__":
    main()