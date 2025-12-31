#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复ID为19的工具包的标题和摘要
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import Content

def fix_toolkit_title():
    """修复ID为19的工具包的标题和摘要"""
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 查询ID为19的工具包
        toolkit = db.query(Content).filter(Content.id == 19).first()
        
        if not toolkit:
            print("未找到ID为19的工具包")
            return
        
        # 为工具包添加适当的标题和摘要
        toolkit.title = "👶新生儿护理技能工具包｜新手爸妈必备护理指南"
        toolkit.summary = "专为新手爸妈打造的新生儿护理技能工具包，包含6大核心工具、详细操作指南和真实案例分享。从脐带护理到婴儿抚触，全面覆盖新生儿日常护理的各个方面，让每位新手爸妈都能从容应对。"
        
        # 保存修改
        db.commit()
        db.refresh(toolkit)
        
        print(f"✅ 成功修复ID为19的工具包")
        print(f"   标题: {toolkit.title}")
        print(f"   摘要: {toolkit.summary[:150]}...")
        
    except Exception as e:
        print(f"修复工具包时发生错误: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_toolkit_title()