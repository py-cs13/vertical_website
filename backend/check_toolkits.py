from database import get_db
from models import Content

# 获取数据库会话
db = next(get_db())

# 查询所有工具包
toolkits = db.query(Content).filter(Content.category == 'toolkit').all()

print('数据库中的工具包:')
for t in toolkits:
    print(f'ID: {t.id}, 标题: {t.title}, 已发布: {t.is_published}, 分类: {t.category}')
