from database import SessionLocal
from models import Content
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建数据库会话
db = SessionLocal()

try:
    # 查找所有带有工具包字样的内容
    toolkits = []
    all_contents = db.query(Content).all()
    
    for content in all_contents:
        # 根据标题或内容判断是否为工具包
        if '工具包' in content.title or 'Toolkit' in content.title or 'toolkit' in content.title:
            toolkits.append(content)
    
    logger.info(f'找到 {len(toolkits)} 个工具包内容')
    
    if toolkits:
        logger.info('工具包内容详情:')
        for toolkit in toolkits:
            logger.info(f'  ID: {toolkit.id}, 标题: {toolkit.title}, 分类: {toolkit.category}, 发布状态: {toolkit.is_published}')
        
        # 确认删除
        confirm = input('\n确认要删除这些工具包吗？(y/n): ')
        if confirm.lower() == 'y':
            # 执行删除
            for toolkit in toolkits:
                db.delete(toolkit)
                logger.info(f'已删除工具包: {toolkit.title} (ID: {toolkit.id})')
            
            # 提交更改
            db.commit()
            logger.info(f'共删除了 {len(toolkits)} 个工具包')
        else:
            logger.info('取消删除操作')
    else:
        logger.info('未找到工具包内容')
        
finally:
    # 关闭数据库会话
    db.close()
