# 检查远程数据库中的工具包记录
# 用于验证生产环境数据库中的工具包数据

from database import get_db, engine
from models import Content
from sqlalchemy.orm import Session
from sqlalchemy import text

print("开始检查远程数据库中的工具包记录...")
print(f"使用的数据库URL: {engine.url}")

try:
    db: Session = next(get_db())
    
    # 测试直接查询
    print("\n测试直接SQL查询:")
    result = db.execute(text("SELECT id, title, category, is_published FROM contents WHERE category = 'toolkit'"))
    toolkit_records = result.fetchall()
    print(f"直接SQL查询到的工具包记录 (共{len(toolkit_records)}条):")
    for record in toolkit_records:
        print(f"ID: {record.id}, 标题: {record.title}, 分类: {record.category}, 状态: {record.is_published}")
    
    # 获取所有内容记录
    all_contents = db.query(Content).all()
    print(f"\n所有内容记录 (共{len(all_contents)}条):")
    for content in all_contents:
        print(f"ID: {content.id}, 标题: {content.title}, 分类: {content.category}, 状态: {content.is_published}")
    
    # 获取所有工具包记录
    toolkits = db.query(Content).filter(Content.category == "toolkit").all()
    print(f"\n所有工具包记录 (共{len(toolkits)}条):")
    for toolkit in toolkits:
        print(f"ID: {toolkit.id}, 标题: {toolkit.title}, 发布状态: {toolkit.is_published}")
    
    db.close()
except Exception as e:
    print(f"查询失败: {str(e)}")

print("\n检查完成!")
