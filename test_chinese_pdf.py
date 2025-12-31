#!/usr/bin/env python3
"""
测试中文PDF生成功能
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.pdf_generator import PDFGenerator

def test_chinese_pdf_generation():
    """测试中文PDF生成"""
    print("开始测试中文PDF生成功能...")
    
    # 创建测试内容（包含中文）
    test_content = {
        "title": "母婴护理工具包",
        "content": "# 母婴护理工具包\n\n## 一、新生儿护理指南\n\n### 1. 日常护理\n\n- 每天给宝宝洗澡1-2次\n- 使用温和的婴儿洗发水和沐浴露\n- 保持宝宝皮肤清洁干燥\n\n### 2. 喂养建议\n\n- 母乳喂养最好持续6个月以上\n- 配方奶喂养要按照说明配比\n- 按需喂养，不要强迫宝宝进食\n\n## 二、育儿工具推荐\n\n1. 婴儿体温计\n2. 奶瓶消毒器\n3. 婴儿抚触油\n4. 防溢乳垫\n\n## 三、常见问题解答\n\nQ: 宝宝晚上哭闹怎么办？\nA: 可能是饥饿、尿布湿了或者需要安抚，可以尝试喂奶、更换尿布或轻拍安抚。\n\nQ: 如何判断宝宝是否吃饱？\nA: 观察宝宝的体重增长、尿量和排便情况，吃饱的宝宝通常会自动停止吸吮。\n"
    }
    
    try:
        # 创建PDF生成器实例
        pdf_gen = PDFGenerator()
        
        # 生成PDF
        print("正在生成PDF...")
        pdf_buffer = pdf_gen.generate_toolkit_pdf(test_content)
        
        # 保存为文件
        output_path = "test_chinese_pdf.pdf"
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print(f"✅ 中文PDF生成成功！文件保存为: {output_path}")
        print("请打开文件检查中文是否正常显示。")
        
        return True
    except Exception as e:
        print(f"❌ 中文PDF生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_chinese_pdf_generation()
