#!/usr/bin/env python3
# 修复空内容问题的脚本
import sys
sys.path.insert(0, '.')
from database import SessionLocal
from models import Content

db = SessionLocal()
try:
    # 查询所有内容，检查哪些字段为空或太短
    contents = db.query(Content).all()
    print(f'总内容数: {len(contents)}')
    print()
    
    problem_contents = []
    for content in contents:
        title_len = len(content.title) if content.title else 0
        summary_len = len(content.summary) if content.summary else 0
        content_len = len(content.content) if content.content else 0
        
        if title_len < 5 or summary_len < 5 or content_len < 1:
            problem_contents.append({
                'id': content.id,
                'title': content.title,
                'title_len': title_len,
                'summary_len': summary_len,
                'content_len': content_len
            })
    
    if problem_contents:
        print(f'发现 {len(problem_contents)} 个问题内容:')
        for pc in problem_contents:
            print(f"  ID={pc['id']}, 标题长度={pc['title_len']}, 摘要长度={pc['summary_len']}, 内容长度={pc['content_len']}")
            print(f"    标题内容: '{pc['title']}'")
        
        print()
        print('开始删除问题内容...')
        
        for pc in problem_contents:
            content_to_delete = db.query(Content).filter(Content.id == pc['id']).first()
            if content_to_delete:
                db.delete(content_to_delete)
                print(f"  已删除内容 ID={pc['id']}")
        
        db.commit()
        print()
        print('问题内容已删除！')
    else:
        print('没有发现问题的内容')
        
finally:
    db.close()
