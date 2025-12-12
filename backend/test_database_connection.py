# 测试数据库连接脚本
# 用于验证是否能成功连接到生产环境数据库

from database import engine, get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

print("开始测试数据库连接...")

# 测试直接连接
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print(f"直接连接测试成功: {result.scalar()}")
except Exception as e:
    print(f"直接连接测试失败: {str(e)}")

# 测试会话连接
try:
    db: Session = next(get_db())
    result = db.execute(text('SELECT 1'))
    print(f"会话连接测试成功: {result.scalar()}")
    db.close()
except Exception as e:
    print(f"会话连接测试失败: {str(e)}")

# 测试创建表（如果不存在）
try:
    from database import Base
    from models import *  # 导入所有模型
    
    # 检查是否有表
    inspector = Base.metadata.reflect(engine)
    table_names = Base.metadata.tables.keys()
    print(f"数据库中已存在的表: {list(table_names)}")
    
    # 如果没有表，创建表
    if not table_names:
        print("没有发现表，正在创建...")
        Base.metadata.create_all(bind=engine)
        print("表创建成功")
        # 重新获取表名
        Base.metadata.reflect(engine)
        new_table_names = Base.metadata.tables.keys()
        print(f"创建的表: {list(new_table_names)}")

except Exception as e:
    print(f"表操作测试失败: {str(e)}")

print("数据库连接测试完成!")
