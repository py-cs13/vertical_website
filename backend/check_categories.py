from database import SessionLocal
from models import Content

# 创建数据库会话
db = SessionLocal()

try:
    # 获取所有分类
    categories = set(c.category for c in db.query(Content).all())
    print('所有分类:', categories)
    
    print('\n每个分类的数量:')
    for cat in categories:
        count = db.query(Content).filter(Content.category == cat).count()
        print(f'  {cat}: {count}')
        
    # 查看每个分类的具体内容
    print('\n每个分类的具体内容:')
    for cat in categories:
        print(f'\n=== {cat} ===')
        contents = db.query(Content).filter(Content.category == cat).all()
        for content in contents[:5]:  # 只显示前5个
            print(f'  ID: {content.id}, 标题: {content.title}, 发布状态: {content.is_published}')
        if len(contents) > 5:
            print(f'  ... 还有 {len(contents) - 5} 个内容')
            
finally:
    # 关闭数据库会话
    db.close()
