#!/usr/bin/env python3
"""
验证分类数量的脚本，直接从后端API获取数据并统计分类数量
"""

import requests
import json

# API地址
API_URL = 'http://localhost:8000/api/articles'

def verify_category_counts():
    """验证分类数量"""
    print('🔍 开始验证分类数量...')
    
    try:
        # 发送API请求
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        
        # 处理不同的数据格式
        data = response.json()
        if isinstance(data, dict) and 'data' in data:
            articles = data['data']
        elif isinstance(data, list):
            articles = data
        else:
            articles = []
        
        print(f'✅ 成功获取到 {len(articles)} 篇文章')
        
        # 统计分类数量
        category_counts = {}
        for article in articles:
            category = article['category']
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
        
        # 显示分类统计结果
        print('\n📊 分类统计结果:')
        for category, count in sorted(category_counts.items()):
            print(f'   {category}: {count} 篇')
        
        print(f'\n✨ 共有 {len(category_counts)} 个分类')
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f'❌ API请求失败: {e}')
        return False
    except json.JSONDecodeError as e:
        print(f'❌ JSON解析失败: {e}')
        return False
    except Exception as e:
        print(f'❌ 其他错误: {e}')
        return False

if __name__ == '__main__':
    verify_category_counts()
