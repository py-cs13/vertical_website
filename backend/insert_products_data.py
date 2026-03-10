#!/usr/bin/env python3
# 为8大分类配置对应的商品数据

import logging
from logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

from database import SessionLocal
from models import Product

# 8大分类商品数据
PRODUCTS_DATA = [
    # 孕期指南
    {
        'name': '孕妇装春秋季套装',
        'description': '舒适透气，适合孕期穿着，宽松设计不勒肚子',
        'image_url': 'https://img.alicdn.com/imgextra/i3/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 199.00,
        'category': '孕期指南'
    },
    {
        'name': '叶酸片 孕期必备',
        'description': '预防胎儿神经管畸形，孕期必备营养补充剂',
        'image_url': 'https://img.alicdn.com/imgextra/i2/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 89.00,
        'category': '孕期指南'
    },
    {
        'name': '孕妇枕 侧睡枕',
        'description': '缓解孕期腰酸背痛，帮助孕妇舒适睡眠',
        'image_url': 'https://img.alicdn.com/imgextra/i3/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 129.00,
        'category': '孕期指南'
    },
    
    # 新生照顾
    {
        'name': '新生儿奶瓶 玻璃材质',
        'description': '安全无毒，耐高温消毒，新生儿喂养必备',
        'image_url': 'https://img.alicdn.com/imgextra/i4/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 79.00,
        'category': '新生照顾'
    },
    {
        'name': '新生儿纸尿裤',
        'description': '超薄透气，吸水性强，新生儿专用纸尿裤',
        'image_url': 'https://img.alicdn.com/imgextra/i5/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 159.00,
        'category': '新生照顾'
    },
    {
        'name': '婴儿洗澡盆 新生儿',
        'description': '大容量设计，材质安全，新生儿洗澡专用',
        'image_url': 'https://img.alicdn.com/imgextra/i6/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 49.00,
        'category': '新生照顾'
    },
    
    # 幼儿发展
    {
        'name': '幼儿早教益智玩具',
        'description': '开发智力，培养动手能力，1-3岁幼儿适用',
        'image_url': 'https://img.alicdn.com/imgextra/i7/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 299.00,
        'category': '幼儿发展'
    },
    {
        'name': '幼儿绘本故事书',
        'description': '精美插画，培养阅读习惯，适合2-5岁幼儿',
        'image_url': 'https://img.alicdn.com/imgextra/i8/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 188.00,
        'category': '幼儿发展'
    },
    {
        'name': '幼儿平衡车',
        'description': '锻炼平衡能力，促进大脑发育，2-6岁适用',
        'image_url': 'https://img.alicdn.com/imgextra/i9/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 259.00,
        'category': '幼儿发展'
    },
    
    # 亲子互动
    {
        'name': '亲子游戏套装',
        'description': '增进亲子关系，开发宝宝智力，全家一起玩',
        'image_url': 'https://img.alicdn.com/imgextra/i10/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 169.00,
        'category': '亲子互动'
    },
    {
        'name': '亲子绘本共读套装',
        'description': '精美插画，培养阅读习惯，增进亲子感情',
        'image_url': 'https://img.alicdn.com/imgextra/i11/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 229.00,
        'category': '亲子互动'
    },
    {
        'name': '亲子手工DIY套装',
        'description': '培养动手能力，增进亲子互动，安全材质',
        'image_url': 'https://img.alicdn.com/imgextra/i12/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 199.00,
        'category': '亲子互动'
    },
    
    # 早期教育
    {
        'name': '幼儿英语启蒙教材',
        'description': '专业英语启蒙，培养语感，0-6岁适用',
        'image_url': 'https://img.alicdn.com/imgextra/i13/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 359.00,
        'category': '早期教育'
    },
    {
        'name': '幼儿数学启蒙玩具',
        'description': '趣味数学学习，培养逻辑思维，3-6岁适用',
        'image_url': 'https://img.alicdn.com/imgextra/i14/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 289.00,
        'category': '早期教育'
    },
    {
        'name': '幼儿音乐启蒙乐器',
        'description': '培养音乐天赋，开发右脑，适合各年龄段',
        'image_url': 'https://img.alicdn.com/imgextra/i15/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 329.00,
        'category': '早期教育'
    },
    
    # 营养健康
    {
        'name': '儿童营养辅食',
        'description': '科学配方，营养均衡，6-12个月适用',
        'image_url': 'https://img.alicdn.com/imgextra/i16/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 199.00,
        'category': '营养健康'
    },
    {
        'name': '儿童维生素滴剂',
        'description': '补充维生素，增强免疫力，儿童专用',
        'image_url': 'https://img.alicdn.com/imgextra/i17/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 129.00,
        'category': '营养健康'
    },
    {
        'name': '儿童钙片',
        'description': '促进骨骼发育，补充钙质，儿童专用',
        'image_url': 'https://img.alicdn.com/imgextra/i18/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 99.00,
        'category': '营养健康'
    },
    
    # 产后恢复
    {
        'name': '产后恢复瑜伽垫',
        'description': '防滑材质，加厚设计，产后恢复专用',
        'image_url': 'https://img.alicdn.com/imgextra/i19/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 159.00,
        'category': '产后恢复'
    },
    {
        'name': '产后恢复营养品',
        'description': '科学配方，补充营养，产后恢复专用',
        'image_url': 'https://img.alicdn.com/imgextra/i20/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 299.00,
        'category': '产后恢复'
    },
    {
        'name': '产后恢复塑身衣',
        'description': '收腹塑身，舒适透气，产后恢复专用',
        'image_url': 'https://img.alicdn.com/imgextra/i21/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 259.00,
        'category': '产后恢复'
    },
    
    # 育儿用品
    {
        'name': '婴儿推车 轻便型',
        'description': '轻便折叠，避震设计，适合0-3岁',
        'image_url': 'https://img.alicdn.com/imgextra/i22/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 899.00,
        'category': '育儿用品'
    },
    {
        'name': '婴儿安全座椅',
        'description': '安全认证，舒适设计，0-4岁适用',
        'image_url': 'https://img.alicdn.com/imgextra/i23/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 1299.00,
        'category': '育儿用品'
    },
    {
        'name': '婴儿床 多功能',
        'description': '可调节高度，安全护栏，0-3岁适用',
        'image_url': 'https://img.alicdn.com/imgextra/i24/O1CN01X7xq1b7b3b9e1a6_!!6000000000000-0-tps-600_600.jpg',
        'link_url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D1%26a%3D100%26k%3D1%26i%3D1%26c%3D1%26l%3De%26pid%3Dmm_123456789_0_0_0%26u%3D1%26w%3D1%26t%3D1%26b%3D1%26f%3D1%26q%3D1%26d%3D1%26k%3D1%26n%3D1%26h%3D1%26m%3D1%26s%3D1%26v%3D1%26p%3D1',
        'price': 1599.00,
        'category': '育儿用品'
    }
]

def main():
    db = SessionLocal()
    
    try:
        logger.info("开始插入商品数据...")
        
        inserted_count = 0
        for product_data in PRODUCTS_DATA:
            product = Product(**product_data)
            db.add(product)
            inserted_count += 1
            logger.info(f"插入商品: {product_data['name']} - {product_data['category']}")
        
        db.commit()
        logger.info(f"商品数据插入完成，共插入 {inserted_count} 条记录")
        
    except Exception as e:
        logger.error(f"插入商品数据失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()