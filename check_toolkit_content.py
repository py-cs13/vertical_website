import psycopg2
import json
import sys

# 连接数据库
try:
    conn = psycopg2.connect(
        database='vertical_website',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    
    # 查询工具包内容
    cursor.execute('SELECT id, title, content, price FROM contents WHERE category = %s LIMIT 2;', ('toolkit',))
    toolkits = cursor.fetchall()
    
    # 输出结果
    for tk in toolkits:
        print(f'\n=== 工具包ID: {tk[0]} ===')
        print(f'标题: {tk[1]}')
        print(f'价格: {tk[3]}元')
        print(f'内容长度: {len(tk[2])}字符')
        print('\n前500字符内容:')
        print(tk[2][:500] + '...')
    
    conn.close()
    
except Exception as e:
    print(f'数据库查询错误: {e}')
    sys.exit(1)
