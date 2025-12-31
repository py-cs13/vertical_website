import sys
import os
sys.path.append('/Users/shucui/Desktop/vertical_website/backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import User
from database import DATABASE_URL

def check_all_users():
    print("正在连接数据库...")
    print(f"使用的数据库URL: {DATABASE_URL}")
    
    # 创建引擎和会话
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 查询所有用户
        users = db.query(User).all()
        
        print(f"\n数据库中共有 {len(users)} 个用户:")
        print("-" * 50)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"邮箱: {user.email}")
            print(f"用户名: {user.username}")
            print(f"是否活跃: {user.is_active}")
            print(f"是否管理员: {user.is_admin}")
            print(f"注册时间: {user.created_at}")
            print(f"更新时间: {user.updated_at}")
            print(f"头像: {user.avatar}")
            print(f"性别: {user.gender}")
            print("-" * 50)
            
    except Exception as e:
        print(f"查询用户时发生错误: {e}")
    finally:
        db.close()

def check_database_tables():
    print("\n检查数据库表结构...")
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 查询所有表
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            
            print(f"数据库中的表: {tables}")
            
    except Exception as e:
        print(f"检查表结构时发生错误: {e}")

if __name__ == "__main__":
    check_database_tables()
    check_all_users()