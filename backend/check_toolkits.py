from database import get_db
from models import Content

# 获取数据库会话
db = next(get_db())

# 查询所有智能体
agents = db.query(Content).filter(Content.category == 'agent').all()

print('数据库中的智能体:')
for a in agents:
    print(f'ID: {a.id}, 标题: {a.title}, 已发布: {a.is_published}, 分类: {a.category}')
