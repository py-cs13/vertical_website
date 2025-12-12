# 重置用户密码脚本
from database import get_db
from models import User
from auth import get_password_hash

def reset_user_password(email: str, new_password: str):
    """
    重置指定用户的密码
    
    Args:
        email: 用户邮箱
        new_password: 新密码
    """
    db = next(get_db())
    
    # 查找用户
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"用户 {email} 不存在")
        return False
    
    # 重置密码
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    
    print(f"用户 {email} 的密码已重置为: {new_password}")
    return True

if __name__ == "__main__":
    # 重置 cs@163.com 用户的密码
    reset_user_password("cs@163.com", "password123")
    
    # 重置 test@example.com 用户的密码
    reset_user_password("test@example.com", "password123")